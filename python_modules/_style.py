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
import json
import time
import tinycss
from datetime import datetime as dt
from handler import WebCachingWrapper as paparazzi
from handler import LoggingWrapper as log
from pytz import timezone
from tqdm import tqdm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Global
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL_RULE_NUM = 0
TOTAL_VALID_RULE_NUM = 0
TOTAL_INVALID_RULE_NUM = 0
TOTAL_UNKNOWN_RULE_NUM = 0


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def outputAsciiArt():
    u'''Output Ascii Art
     @return void
    '''
    print('===================================================================')
    print('=       ===========================================================')
    print('=  ====  ==========================================================')
    print('=  ====  ==========================================================')
    print('=  ====  ===   ===    ====   ===  =   ====   ===      ==      ==  =')
    print('=       ===  =  ==  =  ==  =  ==    =  ==  =  ======  ======  =====')
    print('=  ===========  ==  =  =====  ==  ==========  =====  ======  ===  =')
    print('=  =========    ==    ====    ==  ========    ====  ======  ====  =')
    print('=  ========  =  ==  =====  =  ==  =======  =  ===  ======  =====  =')
    print('=  =========    ==  ======    ==  ========    ==      ==      ==  =')
    print('===================================================================')


def listUpTestCases(testCaseDir):
    u'''List Up Test Case From *. json @ Test Case Directory [ ./case ]
     @param  testCaseDir - Test Case Directory
     @return Test Case List
    '''
    testCaseIdx = 1
    testCaseStack = []
    print(constant.BR)
    print('> Selecable Test Case [X]')
    for root, dirs, files in os.walk(testCaseDir):
        for file in files:
            if not file.find('_style') == -1:
                print('  [{0}] - {1}'.format(
                    testCaseIdx,
                    file.replace(
                        constant.TEST_CASE_EXT,
                        constant.EMPTY
                    ).replace(
                        constant.CASE_TEST_PREFIX,
                        constant.EMPTY
                    )
                ))
                testCaseIdx = testCaseIdx + 1
                testCaseStack.append(file)
    return testCaseStack


def selectTestCase(testCaseDir, testCaseStack):
    u'''Select Test Case via Command Line
     @param  testCaseDir   - Test Case Directory
     @param  testCaseStack - Test Case
     @return Selected Test Case Index
    '''
    testInfoJsonFlg = False
    while not testInfoJsonFlg:
        testCaseIdx = input('> Input Test Case Index ::: ')
        try:
            testRowInfo = json.load(
                open(
                    '{0}{1}{2}'.format(
                        testCaseDir,
                        os.path.sep,
                        testCaseStack[int(testCaseIdx) - 1]
                    ),
                    'r'
                )
            )
            testInfoJsonFlg = True
        except Exception as e:
            testInfoJsonFlg = False
            print('  Warning - Input Test Case Index !')
    return testRowInfo


def startAutoTest(testName):
    u'''Stack Test Start Time
     @param  testName - Test Case Name
     @return Start Time
    '''
    utcNow = dt.now(timezone('UTC'))
    print(constant.BR + '====== ' + testName + ' [ START ] ======')
    print('Date : {0}'.format(
        utcNow.astimezone(timezone('Asia/Tokyo')).strftime('%Y.%m.%d %H:%M:%S')) + constant.BR
    )
    return time.time()


def executeAutoTest(logger, testCache, testCaseInfo):
    u'''Execute Auto Test
     @param  logger       - Logger
     @param  testCache    - Cached Html
     @param  testCaseInfo - Target Styles
     @return void
    '''
    global TOTAL_RULE_NUM
    global TOTAL_VALID_RULE_NUM
    global TOTAL_INVALID_RULE_NUM
    global TOTAL_UNKNOWN_RULE_NUM
    tmpHtml = testCache.getHtml()
    for cssName in testCaseInfo:
        cssParser = tinycss.make_parser()
        css = testCache.loadRawCss(cssName)
        cssSelectors = []
        stylesheet = cssParser.parse_stylesheet(css)
        dispFileName = testCache.getDispFileName(cssName)
        for rule in stylesheet.rules:
            cssSelectors.append(
                rule.selector.as_css().replace(
                    constant.BR,
                    constant.EMPTY
                ).split(',')
            )
        cssSelectors = changeMultiToOneArray(cssSelectors)
        totalSelectorsNum = len(cssSelectors)
        TOTAL_RULE_NUM = TOTAL_RULE_NUM + totalSelectorsNum
        validSelector = []
        invalidSelector = []
        unknownSelector = []
        pbar = tqdm(total=totalSelectorsNum)
        logger.info('=== {0} ==='.format(cssName))
        logger.info('')
        for selector in cssSelectors:
            pbar.set_description('Parsing .. [ %s ] ' % dispFileName)
            tmpElmNum = 0
            tmpSelector = selector.strip()
            try:
                tmpElmNum = len(tmpHtml.select(tmpSelector))
                if tmpElmNum == 0:
                    invalidSelector.append(tmpSelector)
                    TOTAL_INVALID_RULE_NUM = TOTAL_INVALID_RULE_NUM + 1
                else:
                    validSelector.append(tmpSelector)
                    TOTAL_VALID_RULE_NUM = TOTAL_VALID_RULE_NUM + 1
            except Exception as e:
                unknownSelector.append(tmpSelector)
                TOTAL_UNKNOWN_RULE_NUM = TOTAL_UNKNOWN_RULE_NUM + 1
            logger.info('{0} - {1}'.format(tmpSelector, tmpElmNum))
            pbar.update(1)
        pbar.close()
        tmpValidSelectorNum = len(validSelector)
        tmpValidSelectorRate = (tmpValidSelectorNum / totalSelectorsNum) * 100
        tmpInvalidSelectorNum = len(invalidSelector)
        tmpInvalidSelectorRate = (tmpInvalidSelectorNum / totalSelectorsNum) * 100
        tmpUnknownSelectorNum = len(unknownSelector)
        tmpUnknownSelectorRate = (tmpUnknownSelectorNum / totalSelectorsNum) * 100
        logger.info(constant.EMPTY)
        logger.info('  {0} - {1} rules'.format(dispFileName, totalSelectorsNum))
        logger.info('    o       : {0} ( {1} % )'.format(tmpValidSelectorNum, tmpValidSelectorRate))
        logger.info('    x       : {0} ( {1} % )'.format(
            tmpInvalidSelectorNum,
            tmpInvalidSelectorRate
        ))
        logger.info('    unknown : {0} ( {1} % )'.format(
            tmpUnknownSelectorNum,
            tmpUnknownSelectorRate
        ))
        logger.info(constant.EMPTY)
        logger.info(constant.EMPTY)
    print(constant.BR)
    print('Total Rules : {0} rules'.format(TOTAL_RULE_NUM))
    print('  o       : {0} ( {1} % )'.format(
        TOTAL_VALID_RULE_NUM,
        ((TOTAL_VALID_RULE_NUM / TOTAL_RULE_NUM) * 100)
    ))
    print('  x       : {0} ( {1} % )'.format(
        TOTAL_INVALID_RULE_NUM,
        ((TOTAL_INVALID_RULE_NUM / TOTAL_RULE_NUM) * 100)
    ))
    print('  unknown : {0} ( {1} % )'.format(
        TOTAL_UNKNOWN_RULE_NUM,
        ((TOTAL_UNKNOWN_RULE_NUM / TOTAL_RULE_NUM) * 100)
    ))


def endAutoTest(testName, startTime):
    u'''Finish Auto Test
     @param  testName  - Test Case Name
     @param  startTime - Test Start Time
     @return void
    '''
    print(constant.BR + '====== ' + testName + ' [  END  ] ======')
    print('{0} sec.{1}'.format(time.time() - startTime, constant.BR))


def changeMultiToOneArray(selectorsList):
    u'''Change Multi List To Single List
     @param  selectorsList - Target Multi List
     @return Single List
    '''
    result = []
    for selectors in selectorsList:
        for selector in selectors:
            result.append(selector)
    return result


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    outputAsciiArt()
    TEST_CASE_DIR = config['test']['dir']
    TEST_CASE_STACK = listUpTestCases(TEST_CASE_DIR)
    TEST_ROW_INFO = selectTestCase(TEST_CASE_DIR, TEST_CASE_STACK)
    TEST_NAME = TEST_ROW_INFO['name']
    TEST_URL = TEST_ROW_INFO['url']
    TEST_CASE = TEST_ROW_INFO['case']
    START_TIME = startAutoTest(TEST_NAME)
    executeAutoTest(
        logger=log.LoggingWrapper(
            constant.DEFAULT_LOGGER_NAME,
            TEST_NAME + constant.LOG_EXT
        ),
        testCache=paparazzi.WebCachingWrapper(
            cacheDir=config['cache']['dir'],
            cacheName=TEST_NAME,
            url=TEST_URL
        ),
        testCaseInfo=TEST_CASE
    )
    endAutoTest(TEST_NAME, START_TIME)
