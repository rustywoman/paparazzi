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
import tools
from handler import WebDriverWrapper as paparazzi
from handler import LoggingWrapper as log
from tqdm import tqdm
from urllib.parse import urlparse


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Global
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SERVICE_LINKS = []
DUPLICATED_SERVICE_LINKS = []
UNKNOWN_SERVICE_LINKS = []
SERVICE_TMP_ID = 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def executeAutoTest(logger, testName, testCaseInfo, browserName, deviceType):
    u'''Execute Auto Test
     @param  logger       - Logger
     @param  testName     - Test Case Name
     @param  testCaseInfo - Detail Action
     @param  browserName  - Browser Name
     @param  deviceType   - Device Type
     @return void
    '''
    print('Execute Auto Test ...' + constant.BR)
    testWebDriver = paparazzi.WebDriverWrapper(
        screenshotDir=config['screenshot']['dir'],
        browser=browserName,
        device=deviceType,
        options={
            'UA': config['browserUA'][deviceType],
            'SIZE': config['browserSize'][deviceType]
        }
    )
    with tqdm(total=len(testCaseInfo)) as pbar:
        for testCase in testCaseInfo:
            testWebDriver.access(testCase['url'])
            for action in testCase['action']:
                if not action.find(constant.PHOTO_ACTION_NAME) == -1:
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    if len(actionInfo) == 2:
                        imgName = actionInfo[1]
                    else:
                        imgName = testCase['name']
                    testWebDriver.scrollToTop()
                    testWebDriver.takeFullScreenshot(
                        testDir=testName,
                        imgName=imgName
                    )
                elif action == constant.WAIT_ACTION_NAME:
                    testWebDriver.wait()
                elif not action.find(constant.SEARCH_ACTION_NAME) == -1:
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    if len(actionInfo) == 3:
                        restrictKeyword = actionInfo[1]
                        searchKeyword = actionInfo[2]
                    else:
                        restrictKeyword = None
                        searchKeyword = None
                    diveWebServiceKeyword(
                        searchLogger = log.LoggingWrapper(
                            loggerName=constant.DEFAULT_LOGGER_NAME,
                            logFineName='SEARCH_' + testName + constant.LOG_EXT
                        ),
                        testWebDriver=testWebDriver,
                        testCaseName=testCase['name'],
                        extractedLinks=testWebDriver.getLinksInfo(
                            testCase['url'],
                            restrictKeyword
                        ),
                        restrictKeyword=restrictKeyword,
                        searchKeyword=searchKeyword
                    )
                elif not action.find(constant.SCAN_ACTION_NAME) == -1:
                    global SERVICE_TMP_ID
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    if len(actionInfo) == 2:
                        restrictKeyword = actionInfo[1]
                    else:
                        restrictKeyword = None
                    SERVICE_LINKS.append(testCase['url'])
                    testWebDriver.takeFullScreenshot(
                        testDir=testCase['name'],
                        imgName=str(SERVICE_TMP_ID) + '_' + testWebDriver.getTitle()
                    )
                    SERVICE_TMP_ID = SERVICE_TMP_ID + 1
                    diveWebServiceLink(
                        testWebDriver=testWebDriver,
                        testCaseName=testCase['name'],
                        extractedLinks=testWebDriver.getLinksInfo(
                            testCase['url'],
                            restrictKeyword
                        ),
                        restrictKeyword=restrictKeyword
                    )
                    writeScanLog(
                        logger,
                        'Checked Links',
                        SERVICE_LINKS
                    )
                    writeScanLog(
                        logger,
                        'Unknown Links',
                        UNKNOWN_SERVICE_LINKS
                    )
                    writeScanLog(
                        logger,
                        'Duplicated Links',
                        list(set(DUPLICATED_SERVICE_LINKS))
                    )
                else:
                    loopFlg = False
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    tmpEvent = actionInfo[0]
                    tmpSelectorType = actionInfo[1]
                    tmpSelector = actionInfo[2]
                    try:
                        tmpOption = actionInfo[3]
                    except Exception as ex:
                        tmpOption = constant.EMPTY
                    if tmpSelectorType == 'xpath':
                        targetDom = testWebDriver.getElementByXPath(tmpSelector)
                    if tmpSelectorType == 'id':
                        targetDom = testWebDriver.getElementById(tmpSelector)
                    if tmpSelectorType == 'class':
                        targetDom = testWebDriver.getElementsByClassName(tmpSelector)
                        loopFlg = True
                    if tmpSelectorType == 'name':
                        targetDom = testWebDriver.getElementByName(tmpSelector)
                    if tmpSelectorType == 'names':
                        targetDom = testWebDriver.getElementsByName(tmpSelector)
                        loopFlg = True
                    if tmpEvent == constant.INPUT_ACTION and len(tmpOption) > 0:
                        testWebDriver.input(
                            dom=targetDom,
                            value=tmpOption,
                            loopFlg=loopFlg
                        )
                    if tmpEvent == constant.ENTER_ACTION:
                        testWebDriver.enter(
                            dom=targetDom,
                            loopFlg=loopFlg
                        )
                    if tmpEvent == constant.CLICK_ACTION:
                        testWebDriver.click(
                            dom=targetDom,
                            loopFlg=loopFlg
                        )
            pbar.update(1)
    print(constant.BR + 'Finalizing Dummy Browser ...')
    testWebDriver.done()


def writeScanLog(logger, resultType, scanResult):
    u'''Log For Scan
     @param  logger  - Logger
     @param  resultType - Log Title
     @param  scanResult - Extracted Result
     @return void
    '''
    logger.log(constant.EMPTY)
    logger.log('=== {0} ==='.format(resultType))
    serviceLinkIdx = 1
    for serviceTmpLink in scanResult:
        logger.log('[{0}] {1}'.format(serviceLinkIdx, serviceTmpLink))
        serviceLinkIdx = serviceLinkIdx + 1


def checkIsDivedLink(targetLink):
    u'''Check Link Validation
     @param  targetLink - Target Link
     @return boolean
    '''
    checkIdx = 0
    for serviceTmpLink in SERVICE_LINKS:
        if serviceTmpLink == targetLink:
            checkIdx = checkIdx + 1
        else:
            noneQueryTargetLink = targetLink.replace(
                '?' + urlparse(targetLink).query,
                constant.EMPTY
            )
            if serviceTmpLink.startswith(noneQueryTargetLink):
                checkIdx = checkIdx + 1
            noneHashTargetLink = targetLink.replace(
                '#' + urlparse(targetLink).fragment,
                constant.EMPTY
            )
            if serviceTmpLink.startswith(noneHashTargetLink):
                checkIdx = checkIdx + 1
    if checkIdx == 0:
        return True
    else:
        return False

def diveWebServiceKeyword(searchLogger, testWebDriver, testCaseName, extractedLinks, restrictKeyword, searchKeyword):
    u'''Recursive Diving - word
     @param  testWebDriver   - Web Driver
     @param  testCaseName    - Test Case Name
     @param  extractedLinks  - Extracted Links
     @param  restrictKeyword - Search Limit
     @param  searchKeyword   - Search Keywords
     @return void
    '''
    global SERVICE_TMP_ID
    for currentTmpLink in extractedLinks:
        if checkIsDivedLink(currentTmpLink):
            SERVICE_LINKS.append(currentTmpLink)
            try:
                testWebDriver.access(currentTmpLink)
                pickUpResult = testWebDriver.pickUpKeywords(currentTmpLink, searchKeyword)
                searchLogger.log(pickUpResult)
                SERVICE_TMP_ID = SERVICE_TMP_ID + 1
                diveWebServiceKeyword(
                    searchLogger=searchLogger,
                    testWebDriver=testWebDriver,
                    testCaseName=testCaseName,
                    extractedLinks=testWebDriver.getLinksInfo(
                        currentTmpLink,
                        restrictKeyword
                    ),
                    restrictKeyword=restrictKeyword,
                    searchKeyword=searchKeyword
                )
            except Exception as e:
                print('=====================================')
                print(currentTmpLink)
                print('=====================================')
                print(e)
                UNKNOWN_SERVICE_LINKS.append(currentTmpLink)
        else:
            DUPLICATED_SERVICE_LINKS.append(currentTmpLink)


def diveWebServiceLink(testWebDriver, testCaseName, extractedLinks, restrictKeyword):
    u'''Recursive Diving - link
     @param  testWebDriver   - Web Driver
     @param  testCaseName    - Test Case Name
     @param  extractedLinks  - Extracted Links
     @param  restrictKeyword - Search Limit
     @return void
    '''
    global SERVICE_TMP_ID
    for currentTmpLink in extractedLinks:
        if checkIsDivedLink(currentTmpLink):
            SERVICE_LINKS.append(currentTmpLink)
            try:
                testWebDriver.access(currentTmpLink)
                testWebDriver.takeFullScreenshot(
                    testDir=testCaseName,
                    imgName=str(SERVICE_TMP_ID) + '_' + testWebDriver.getTitle()
                )
                SERVICE_TMP_ID = SERVICE_TMP_ID + 1
                diveWebServiceLink(
                    testWebDriver=testWebDriver,
                    testCaseName=testCaseName,
                    extractedLinks=testWebDriver.getLinksInfo(
                        currentTmpLink,
                        restrictKeyword
                    ),
                    restrictKeyword=restrictKeyword
                )
            except Exception as e:
                print('=====================================')
                print(currentTmpLink)
                print('=====================================')
                print(e)
                UNKNOWN_SERVICE_LINKS.append(currentTmpLink)
        else:
            DUPLICATED_SERVICE_LINKS.append(currentTmpLink)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    tools.outputAsciiArt()
    TEST_CASE_DIR = config['test']['dir']
    TEST_CASE_STACK = tools.listUpTestCases(
        testCaseDir=TEST_CASE_DIR,
        execFileName=tools.getMainScriptFileName(__file__)
    )
    TEST_ROW_INFO = tools.selectTestCase(
        testCaseDir=TEST_CASE_DIR,
        testCaseStack=TEST_CASE_STACK
    )
    BROWSER_NAME = tools.selectBrowser()
    if BROWSER_NAME == 'edge':
        DEVICE_TYPE = 'pc'
    else:
        DEVICE_TYPE = tools.selectDeviceType()
    TEST_NAME = TEST_ROW_INFO['name']
    TEST_CASE = TEST_ROW_INFO['case']
    START_TIME = tools.startAutoTest(TEST_NAME)
    executeAutoTest(
        logger=log.LoggingWrapper(
            loggerName=constant.DEFAULT_LOGGER_NAME,
            logFineName=TEST_NAME + constant.LOG_EXT
        ),
        testName=TEST_NAME,
        testCaseInfo=TEST_CASE,
        browserName=BROWSER_NAME,
        deviceType=DEVICE_TYPE
    )
    tools.endAutoTest(
        testName=TEST_NAME,
        startTime=START_TIME
    )
