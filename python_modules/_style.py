#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import Configuration Dir.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import constant
import config
import multiprocessing as multi
import numpy as np
import re
import tools
import tinycss
import urllib.request
from datetime import datetime
from handler import WebCachingWrapper as paparazzi
from handler import LoggingWrapper as log
from multiprocessing import Pool
from tqdm import tqdm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Global
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMAGES_IN_CSS = []
EX_SELECTORS_REG_EXP = '|'.join(
    [
        ':after',
        ':active',
        ':before',
        ':focus',
        ':hover',
        ':not(.*)'
    ]
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def multiImageDownloader(testName, testURL, savedDir, imagesGroup, downloadPipeIdx):
    u'''Download Images by Parallel Pipeline
     @param testName        - Test Name
     @param testURL         - Test URL
     @param savedDir        - Directory Name for Images
     @param imagesGroup     - Target Images
     @param downloadPipeIdx - Index For Pipeline
    '''
    testCache = paparazzi.WebCachingWrapper(
        cacheDir=config['cache']['dir'],
        cacheName=testName,
        url=testURL
    )
    with tqdm(
        total=len(imagesGroup),
        desc='Image Downloading Pipeline [ {0} ] '.format(downloadPipeIdx)
    ) as pbar:
        for tagImage in imagesGroup:
            testCache.downloadImage(savedDir, testURL, tagImage)
            pbar.update(1)


def diveImageInCss(rawCss):
    u'''Collect Images in Css
     @param rawCss - Raw Css
    '''
    global IMAGES_IN_CSS
    unminifiedCss = re.sub('\{', ' {\n\r\n\r\t', rawCss)
    unminifiedCss = re.sub('\}', '\n\r\n\r}\n\r\n\r', unminifiedCss)
    unminifiedCss = re.sub(';', ';\n\r\t', unminifiedCss)
    for outerImageURL in re.findall('(url\(.+\))', unminifiedCss):
        IMAGES_IN_CSS.append(outerImageURL)


def diveCssFile(cssParser, tmpCssName, cssSelectors):
    u'''Collect Selectors in Css
     @param cssParser    - Css Parser
     @param tmpCssName   - Css File Name
     @param cssSelectors - Stack for Selectors in Css
     @return Selectors List
    '''
    try:
        rawCss = str(urllib.request.urlopen(tmpCssName).read().decode(encoding='utf-8'))
    except Exception as e:
        rawCss = str(urllib.request.urlopen(tmpCssName).read().decode(encoding='shift_jis'))
    stylesheet = cssParser.parse_stylesheet(rawCss)
    for rule in stylesheet.rules:
        try:
            filteredSelector = rule.selector.as_css().replace(
                constant.BR,
                constant.EMPTY
            ).split(',')
            cssSelectors.append(filteredSelector)
        except Exception as parseEx:
            try:
                diveCssFile(
                    cssParser,
                    testCache.changeAbsPathToRelPath(tmpCssName, rule.uri),
                    cssSelectors
                )
            except Exception as e:
                print('Selector Parse Error ---> Skip...')
                print(e)
    diveImageInCss(rawCss)
    return cssSelectors


def validateCssSelector(logger, cssSelectors, dispFileName):
    u'''Validate Selector
     @param logger       - Logger
     @param cssSelectors - Selectors in Css
     @param dispFileName - Css Name
    '''
    global TOTAL_RULE_NUM
    global TOTAL_INVALID_RULE_NUM
    global TOTAL_VALID_RULE_NUM
    global TOTAL_UNKNOWN_RULE_NUM
    totalSelectorsNum = len(cssSelectors)
    logger.log('File Name : [ {0} ] - {1} rules.'.format(dispFileName, totalSelectorsNum))
    TOTAL_RULE_NUM = TOTAL_RULE_NUM + totalSelectorsNum
    validSelector = []
    invalidSelector = []
    unknownSelector = []
    with tqdm(total=totalSelectorsNum, desc=dispFileName) as pbar:
        for selector in cssSelectors:
            tmpElmNum = 0
            tmpSelector = selector.strip()
            try:
                # Check : 議事要素はSelectorから除外 ( EX_SELECTORS_REG_EXP )
                tmpElmNum = len(tmpHtml.select(re.sub(EX_SELECTORS_REG_EXP, '', tmpSelector)))
                if tmpElmNum == 0:
                    invalidSelector.append(
                        {
                            'selector': tmpSelector,
                            'count': tmpElmNum
                        }
                    )
                    TOTAL_INVALID_RULE_NUM = TOTAL_INVALID_RULE_NUM + 1
                else:
                    validSelector.append(
                        {
                            'selector': tmpSelector,
                            'count': tmpElmNum
                        }
                    )
                    TOTAL_VALID_RULE_NUM = TOTAL_VALID_RULE_NUM + 1
            except Exception as e:
                unknownSelector.append(
                    {
                        'selector': tmpSelector,
                        'count': 0
                    }
                )
                TOTAL_UNKNOWN_RULE_NUM = TOTAL_UNKNOWN_RULE_NUM + 1
            pbar.update(1)
    tmpValidSelectorNum = len(validSelector)
    tmpValidSelectorRate = (tmpValidSelectorNum / totalSelectorsNum) * 100
    tmpInvalidSelectorNum = len(invalidSelector)
    tmpInvalidSelectorRate = (tmpInvalidSelectorNum / totalSelectorsNum) * 100
    tmpUnknownSelectorNum = len(unknownSelector)
    tmpUnknownSelectorRate = (tmpUnknownSelectorNum / totalSelectorsNum) * 100
    logger.log(constant.EMPTY)
    logger.log('  {0} - {1} rules'.format(dispFileName, totalSelectorsNum))
    logger.log('    o       : {0} ( {1} % )'.format(
        tmpValidSelectorNum,
        tmpValidSelectorRate
    ))
    for info in validSelector:
        logger.log('        {0} - {1}'.format(info['selector'], info['count']).encode(encoding='utf-8'))
    logger.log(constant.EMPTY)
    logger.log('    x       : {0} ( {1} % )'.format(
        tmpInvalidSelectorNum,
        tmpInvalidSelectorRate
    ))
    for info in invalidSelector:
        logger.log('        {0} - {1}'.format(info['selector'], info['count']).encode(encoding='utf-8'))
    logger.log(constant.EMPTY)
    logger.log('    unknown : {0} ( {1} % )'.format(
        tmpUnknownSelectorNum,
        tmpUnknownSelectorRate
    ))
    for info in unknownSelector:
        logger.log('        {0} - {1}'.format(info['selector'], info['count']).encode(encoding='utf-8'))
    logger.log(constant.EMPTY)
    logger.log(constant.EMPTY)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    helper = tools.outputHelp(
        scriptFileName=__file__,
        scriptUsage='sh style.sh',
        description='Parse and Check All Css Definitions, Collecting All Images if you need.',
        epilog=''
    )
    helper.parse_args()
    tools.outputAsciiArt()
    POOL_LIMIT = multi.cpu_count()
    TOTAL_RULE_NUM = 0
    TOTAL_VALID_RULE_NUM = 0
    TOTAL_INVALID_RULE_NUM = 0
    TOTAL_UNKNOWN_RULE_NUM = 0
    TEST_CASE_DIR = config['test']['dir']
    TEST_CASE_STACK = tools.listUpTestCases(
        testCaseDir=TEST_CASE_DIR,
        execFileName=tools.getMainScriptFileName(__file__)
    )
    TEST_ROW_INFO = tools.selectTestCase(
        testCaseDir=TEST_CASE_DIR,
        testCaseStack=TEST_CASE_STACK
    )
    TEST_NAME = TEST_ROW_INFO['name']
    TEST_URL = TEST_ROW_INFO['url']
    TEST_SAVED_IMAGES_DIR = os.path.sep.join(
        [
            config['cache']['dir'],
            TEST_NAME
        ]
    )
    if not os.path.exists(TEST_SAVED_IMAGES_DIR):
        os.makedirs(TEST_SAVED_IMAGES_DIR)
    TEST_SAVED_IMAGES_DIR = TEST_SAVED_IMAGES_DIR + os.path.sep
    START_TIME = tools.startAutoTest(TEST_NAME)
    logger = log.LoggingWrapper(
        loggerName=constant.DEFAULT_LOGGER_NAME,
        logFineName='STYLE_' + TEST_NAME + '_' + datetime.now().strftime(constant.LOG_TIMESTAMP_FORMAT) + constant.LOG_EXT
    )
    testCache = paparazzi.WebCachingWrapper(
        cacheDir=config['cache']['dir'],
        cacheName=TEST_NAME,
        url=TEST_URL
    )
    # Html情報をpickleから取得
    tmpHtml = testCache.getHtml()
    # Htmlのタイトル情報
    print('Title :')
    print('    ' + testCache.getHtmlTitle())
    print(constant.EMPTY)
    # HtmlのインラインMeta情報
    print('Metas :')
    tmpMetas = testCache.getInlineMeta()
    for meta in tmpMetas:
        print('    {0}'.format(meta))
    print(constant.EMPTY)
    # Htmlの外部Script情報
    print('Outer Scripts :')
    tmpOuterScripts = testCache.getOuterScript()
    for script in tmpOuterScripts:
        print('    {0}'.format(script))
    print(constant.EMPTY)
    # HtmlのインラインScript情報
    print('Inline Scripts :')
    tmpInlineScripts = testCache.getInlineScript(constant.BR)
    for script in tmpInlineScripts:
        print(script)
    print(constant.EMPTY)
    # Style解析機
    cssParser = tinycss.make_parser()
    # インラインスタイル化しているCssをpickleのキャッシュから取得
    inlineSelectors = []
    tmpStyles = testCache.getInlineStyle()
    for inlineStyle in tmpStyles:
        stylesheet = cssParser.parse_stylesheet(inlineStyle.text)
        for rule in stylesheet.rules:
            try:
                filteredSelector = rule.selector.as_css().replace(
                    constant.BR,
                    constant.EMPTY
                ).split(',')
                inlineSelectors.append(filteredSelector)
            except Exception as parseEx:
                try:
                    diveCssFile(
                        cssParser,
                        'https:' + rule.uri if re.match('^//', rule.uri) else rule.uri,
                        inlineSelectors
                    )
                except Exception as e:
                    print('Selector Parse Error ---> Skip...')
                    print(e)
    inlineSelectors = testCache.changeMultiToOneArray(inlineSelectors)
    if len(inlineSelectors) is not 0:
        validateCssSelector(
            logger,
            inlineSelectors,
            'inline'
        )
    # 外部ファイル化しているCssをpickleのキャッシュから取得
    for link in testCache.getOuterCss():
        tmpCssName = testCache.changeAbsPathToRelPath(TEST_URL, link['href'])
        logger.log('Absolute Path : [ {0} ]'.format(tmpCssName))
        cssSelectors = []
        cssSelectors = diveCssFile(
            cssParser,
            tmpCssName,
            cssSelectors
        )
        if len(cssSelectors) is not 0:
            validateCssSelector(
                logger,
                testCache.changeMultiToOneArray(cssSelectors),
                testCache.getDispFileName(tmpCssName)
            )
    logger.log('Total Rules : {0} rules'.format(TOTAL_RULE_NUM))
    logger.log('  o       : {0} ( {1} % )'.format(
        TOTAL_VALID_RULE_NUM,
        ((TOTAL_VALID_RULE_NUM / TOTAL_RULE_NUM) * 100)
    ))
    logger.log('  x       : {0} ( {1} % )'.format(
        TOTAL_INVALID_RULE_NUM,
        ((TOTAL_INVALID_RULE_NUM / TOTAL_RULE_NUM) * 100)
    ))
    logger.log('  unknown : {0} ( {1} % )'.format(
        TOTAL_UNKNOWN_RULE_NUM,
        ((TOTAL_UNKNOWN_RULE_NUM / TOTAL_RULE_NUM) * 100)
    ))
    # HTML, CSS内部の画像を一覧化（重複なし）後、並列ダウンロード
    downloadFlg = False
    print(constant.EMPTY)
    while not downloadFlg:
        downloadChoice = input('> Download All Images ? ( yes [y] / no [n] ) ::: ')
        downloadFlg = True
    if downloadChoice == 'yes' or downloadChoice == 'y':
        print(constant.EMPTY)
        serializedImages = []
        for tagImage in testCache.getInlineImage():
            serializedImages.append(tagImage['src'])
        serializedImages = list(set(serializedImages))
        serializedImages.extend(list(set(IMAGES_IN_CSS)))
        SPLIT_IMAGES_GROUP = np.array_split(np.array(serializedImages), POOL_LIMIT)
        POOL = Pool(POOL_LIMIT)
        DONWLOAD_PIPE_IDX = 1
        for imagesGroup in SPLIT_IMAGES_GROUP:
            POOL.apply_async(
                multiImageDownloader,
                args=(
                    TEST_NAME,
                    TEST_URL,
                    TEST_SAVED_IMAGES_DIR,
                    imagesGroup,
                    DONWLOAD_PIPE_IDX,
                )
            )
            DONWLOAD_PIPE_IDX = DONWLOAD_PIPE_IDX + 1
        POOL.close()
        POOL.join()
    tools.endAutoTest(
        testName=TEST_NAME,
        startTime=START_TIME
    )
