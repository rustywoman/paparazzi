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
import uuid
from handler import WebCachingWrapper as paparazzi
from handler import LoggingWrapper as log
from multiprocessing import Pool
from tqdm import tqdm


def multiImageDownloader(
    TEST_NAME,
    TEST_URL,
    TEST_SAVED_IMAGES_DIR,
    imagesGroup,
    imagesCategory,
    downloadPipeIdx,
    inlineFlg
):
    testCache = paparazzi.WebCachingWrapper(
        cacheDir=config['cache']['dir'],
        cacheName=TEST_NAME,
        url=TEST_URL
    )
    with tqdm(
        total=len(imagesGroup),
        desc='Downloading ... Images In {0} [ {1} ]'.format(imagesCategory, downloadPipeIdx)
    ) as pbar:
        for tagImage in imagesGroup:
            testCache.downloadImage(TEST_SAVED_IMAGES_DIR, TEST_URL, tagImage, inlineFlg)
            pbar.update(1)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    tools.outputAsciiArt()
    POOL_LIMIT = multi.cpu_count()
    TOTAL_RULE_NUM = 0
    TOTAL_VALID_RULE_NUM = 0
    TOTAL_INVALID_RULE_NUM = 0
    TOTAL_UNKNOWN_RULE_NUM = 0
    TEST_CASE_DIR = config['test']['dir']
    IMAGES_IN_CSS = []
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
        logFineName='STYLE_' + TEST_NAME + constant.LOG_EXT
    )
    testCache = paparazzi.WebCachingWrapper(
        cacheDir=config['cache']['dir'],
        cacheName=TEST_NAME,
        url=TEST_URL
    )
    # Html情報をpickleから取得
    tmpHtml = testCache.getHtml()
    # 外部ファイル化しているCssをpickleのキャッシュから取得
    for link in testCache.getOuterCss():
        tmpCssName = testCache.changeAbsPathToRelPath(TEST_URL, link['href'])
        try:
            rawCss = str(urllib.request.urlopen(tmpCssName).read().decode(encoding='utf-8'))
        except Exception as e:
            rawCss = str(urllib.request.urlopen(tmpCssName).read().decode(encoding='shift_jis'))
        cssParser = tinycss.make_parser()
        cssSelectors = []
        stylesheet = cssParser.parse_stylesheet(rawCss)
        for rule in stylesheet.rules:
            try:
                filteredSelector = rule.selector.as_css().replace(
                    constant.BR,
                    constant.EMPTY
                ).split(',')
                cssSelectors.append(filteredSelector)
            except Exception as e:
                # ToDo - Imported CSS
                print('Import CSS ---> Skip...')
                # print(rule)
        if len(cssSelectors) is not 0:
            cssSelectors = testCache.changeMultiToOneArray(cssSelectors)
            totalSelectorsNum = len(cssSelectors)
            dispFileName = testCache.getDispFileName(tmpCssName)
            logger.log('[ {0} ] - {1} rules.'.format(dispFileName, totalSelectorsNum))
            TOTAL_RULE_NUM = TOTAL_RULE_NUM + totalSelectorsNum
            validSelector = []
            invalidSelector = []
            unknownSelector = []
            with tqdm(total=totalSelectorsNum, desc=dispFileName) as pbar:
                for selector in cssSelectors:
                    tmpElmNum = 0
                    tmpSelector = selector.strip()
                    try:
                        tmpElmNum = len(tmpHtml.select(tmpSelector))
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
                logger.log('        {0} - {1}'.format(info['selector'], info['count']))
            logger.log(constant.EMPTY)
            logger.log('    x       : {0} ( {1} % )'.format(
                tmpInvalidSelectorNum,
                tmpInvalidSelectorRate
            ))
            for info in invalidSelector:
                logger.log('        {0} - {1}'.format(info['selector'], info['count']))
            logger.log(constant.EMPTY)
            logger.log('    unknown : {0} ( {1} % )'.format(
                tmpUnknownSelectorNum,
                tmpUnknownSelectorRate
            ))
            for info in unknownSelector:
                logger.log('        {0} - {1}'.format(info['selector'], info['count']))
            logger.log(constant.EMPTY)
            logger.log(constant.EMPTY)
            unminifiedCss = re.sub('\{', ' {\n\r\n\r\t', rawCss)
            unminifiedCss = re.sub('\}', '\n\r\n\r}\n\r\n\r', unminifiedCss)
            unminifiedCss = re.sub(';', ';\n\r\t', unminifiedCss)
            for outerImageURL in re.findall('(url\(.+\))', unminifiedCss):
                IMAGES_IN_CSS.append(outerImageURL)
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
    # Html内の画像をローカルにダウンロード
    serializedImages = []
    for tagImage in testCache.getInlineImage():
        serializedImages.append(tagImage['src'])
    serializedImages = list(set(serializedImages))
    SPLIT_IMAGES_GROUP = np.array_split(np.array(serializedImages), POOL_LIMIT)
    POOL = Pool(POOL_LIMIT)
    DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_HTML = 1
    for imagesGroup in SPLIT_IMAGES_GROUP:
        POOL.apply_async(
            multiImageDownloader,
            args=(
                TEST_NAME,
                TEST_URL,
                TEST_SAVED_IMAGES_DIR,
                imagesGroup,
                'HTML',
                DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_HTML,
                True,
            )
        )
        DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_HTML = DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_HTML + 1
    POOL.close()
    POOL.join()
    # Css内の画像をローカルにダウンロード
    serializedImages = list(set(IMAGES_IN_CSS))
    logger.log(serializedImages)
    SPLIT_IMAGES_GROUP = np.array_split(np.array(serializedImages), POOL_LIMIT)
    POOL = Pool(POOL_LIMIT)
    DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_CSS = 1
    for imagesGroup in SPLIT_IMAGES_GROUP:
        POOL.apply_async(
            multiImageDownloader,
            args=(
                TEST_NAME,
                TEST_URL,
                TEST_SAVED_IMAGES_DIR,
                imagesGroup,
                'CSS',
                DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_CSS,
                False,
            )
        )
        DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_CSS = DONWLOAD_PIPE_IDX_FOR_IMAGES_IN_CSS + 1
    POOL.close()
    POOL.join()
    tools.endAutoTest(
        testName=TEST_NAME,
        startTime=START_TIME
    )
