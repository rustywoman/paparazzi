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
from datetime import datetime as dt
from handler import WebDriverWrapper as paparazzi
from handler import LoggingWrapper as log
from pytz import timezone
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
            if file.find('_style') == -1:
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
    print('Initializing Dummy Browser ...')
    return time.time()


def executeAutoTest(testName, testCaseInfo):
    u'''Execute Auto Test
     @param  testName     - Test Case Name
     @param  testCaseInfo - Detail Action
     @return void
    '''
    print('Execute Auto Test ...' + constant.BR)
    testWebDriver = paparazzi.WebDriverWrapper(
        screenshotDir=config['screenshot']['dir']
    )
    logForTestWebDriver = log.LoggingWrapper(
        constant.DEFAULT_LOGGER_NAME,
        testName + constant.LOG_EXT
    )
    testWebDriver.maximumWindow()
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
                        logForTestWebDriver,
                        'Checked Links',
                        SERVICE_LINKS
                    )
                    writeScanLog(
                        logForTestWebDriver,
                        'Unknown Links',
                        UNKNOWN_SERVICE_LINKS
                    )
                    writeScanLog(
                        logForTestWebDriver,
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


def endAutoTest(testName, startTime):
    u'''Finish Auto Test
     @param  testName  - Test Case Name
     @param  startTime - Test Start Time
     @return void
    '''
    print(constant.BR + '====== ' + testName + ' [  END  ] ======')
    print('{0} sec.{1}'.format(time.time() - startTime, constant.BR))


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


def diveWebServiceLink(testWebDriver, testCaseName, extractedLinks, restrictKeyword):
    u'''Recursive Diving
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
    outputAsciiArt()
    TEST_CASE_DIR = config['test']['dir']
    TEST_CASE_STACK = listUpTestCases(TEST_CASE_DIR)
    TEST_ROW_INFO = selectTestCase(TEST_CASE_DIR, TEST_CASE_STACK)
    TEST_NAME = TEST_ROW_INFO['name']
    TEST_CASE = TEST_ROW_INFO['case']
    START_TIME = startAutoTest(TEST_NAME)
    executeAutoTest(TEST_NAME, TEST_CASE)
    endAutoTest(TEST_NAME, START_TIME)
