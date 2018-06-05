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
import argparse
import constant
import config
import json
import time
# ---
from datetime import datetime as dt
from handler import ConsoleWrapper as deco
from handler import WebDriverWrapper as paparazzi
from handler import LoggingWrapper as log
from pytz import timezone
# Check : Colored Problem
from tqdm import tqdm
from urllib.parse import urlparse


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Global
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SERVICE_LINKS = []
DUPLICATED_SERVICE_LINKS = []
UNKNOWN_SERVICE_LINKS = []
SERVICE_TMP_ID = 1
console = deco.ConsoleWrapper()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def outputHelp(scriptFileName, scriptUsage, description, epilog):
    u'''Output Help
     @param  scriptFileName - File Name
     @param  scriptUsage    - Sample Command
     @param  description    - Description
     @param  epilog         - Epi. Message
     @return Argument parser
    '''
    parser = argparse.ArgumentParser(
        prog=scriptFileName,
        usage=scriptUsage,
        description=description,
        epilog=epilog,
        add_help=True
    )
    return parser


def outputAsciiArt():
    u'''Output Ascii Art
     @return void
    '''
    asciiInfo = [
        '-------------------------------------------------------------------',
        '-       -----------------------------------------------------------',
        '-  ----  ----------------------------------------------------------',
        '-  ----  ----------------------------------------------------------',
        '-  ----  ---   ---    ----   ---  -   ----   ---      --      --  -',
        '-       ---  -  --  -  --  -  --    -  --  -  ------  ------  -----',
        '-  -----------  --  -  -----  --  ----------  -----  ------  ---  -',
        '-  ---------    --    ----    --  --------    ----  ------  ----  -',
        '-  --------  -  --  -----  -  --  -------  -  ---  ------  -----  -',
        '-  ---------    --  ------    --  --------    --      --      --  -',
        '-------------------------------------------------------------------',
    ]
    for asciiStr in asciiInfo:
        print(console.STR_BLUE + asciiStr + console.END_CODE)


def getMainScriptFileName(fileName):
    u'''Get Main Script Name
     @param  fileName - __filename__
     @return Main Script File Name without python extension
    '''
    return os.path.basename(fileName).replace(constant.PYTHON_EXT, constant.EMPTY)


def getTimeFromEpoc(epocTime):
    return dt(*time.localtime(epocTime)[:6]).strftime(constant.REPORT_TIMESTAMP_FORMAT)


def selectDeviceType():
    u'''Select Device Type
     @return Selected Device Type
    '''
    testDeviceTypeFlg = False
    deviceTypeList = ['pc', 'tablet', 'sp']
    print(console.UNDERLINE + console.STR_CYAN + 'Selectable Device [X]' + console.END_CODE)
    for deviceTypeIdx in range(len(deviceTypeList)):
        print(constant.TAB + '[{0}] - {1}'.format(deviceTypeIdx + 1, deviceTypeList[deviceTypeIdx]))
    while not testDeviceTypeFlg:
        testDeviceTypeIdx = input(console.STR_CYAN + '> Input Device Type Index ::: ' + console.END_CODE)
        try:
            testDeviceTypeIdx = deviceTypeList[int(testDeviceTypeIdx) - 1]
            testDeviceTypeFlg = True
        except Exception as e:
            testDeviceTypeFlg = False
            console.error(constant.TAB + 'Warning - Device is required. Re-Input, please.')
    return testDeviceTypeIdx


def selectBrowser(multiFlg=False):
    u'''Select Browser
     @return Selected Browser Type
    '''
    testBrowserFlg = False
    if multiFlg is True:
        # Check : Edgeは、multi-sessionに対応していないので、複数プロセスでEdgeを同時操作は不可 @ 2018.05.04
        browserList = ['chrome', 'firefox']
    else:
        browserList = ['chrome', 'firefox', 'edge']
    print(console.UNDERLINE + console.STR_CYAN + 'Selectable Browser [X]' + console.END_CODE)
    for browserIdx in range(len(browserList)):
        print(constant.TAB + '[{0}] - {1}'.format(browserIdx + 1, browserList[browserIdx]))
    while not testBrowserFlg:
        testBrowserTypeIdx = input(console.STR_CYAN + '> Input Browser Index ::: ' + console.END_CODE)
        try:
            testBrowserTypeIdx = browserList[int(testBrowserTypeIdx) - 1]
            testBrowserFlg = True
        except Exception as e:
            testBrowserFlg = False
            console.error(constant.TAB + 'Warning - Browser is required. Re-Input, please.')
    return testBrowserTypeIdx


def listUpTestCases(testCaseDir, execFileName):
    u'''List Up Test Case From *. json @ Test Case Directory [ ./case ]
     @param  testCaseDir - Test Case Directory
     @return Test Case List
    '''
    testCaseIdx = 1
    testCaseStack = []
    print(console.UNDERLINE + console.STR_CYAN + 'Selectable Test Cases [X]' + console.END_CODE)
    for root, dirs, files in os.walk(testCaseDir):
        for file in files:
            if not file.find(execFileName) == -1:
                print(constant.TAB + '[{0}] - {1}'.format(
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
        testCaseIdx = input(console.STR_CYAN + '> Input Test Case Index ::: ' + console.END_CODE)
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
            console.error(constant.TAB + 'Warning - Test Case Index is required. Re-Input, please.')
    return testRowInfo


def startAutoTest(testName):
    u'''Stack Test Start Time
     @param  testName - Test Case Name
     @return Start Time
    '''
    utcNow = dt.now(timezone('UTC'))
    print(constant.BR + '====== ' + testName + ' [ START ] ======' + constant.BR)
    print('Date : {0}'.format(utcNow.astimezone(timezone('Asia/Tokyo')).strftime(constant.REPORT_TIMESTAMP_FORMAT)))
    print(constant.BR)
    return time.time()


def executeAutoTest(logger, testName, testCaseInfo, browserName, deviceType):
    u'''Execute Auto Test
     @param  logger       - Logger
     @param  testName     - Test Case Name
     @param  testCaseInfo - Detail Action
     @param  browserName  - Browser Name
     @param  deviceType   - Device Type
     @return void
    '''
    testWebDriver = paparazzi.WebDriverWrapper(
        screenshotDir=config['screenshot']['dir'],
        browser=browserName,
        device=deviceType,
        options={
            'UA': config['browserUA'][deviceType],
            'SIZE': config['browserSize'][deviceType]
        }
    )
    tmpDataDir = os.path.sep.join(
        [
            config['report']['tmp-dir']
        ]
    ) + os.path.sep
    reportConfigStream = open(
        tmpDataDir + testName + constant.TEST_CASE_EXT,
        'w'
    )
    testResult = {
        'name' : testName,
        'general' : {
            'browser' : browserName,
            'device' : deviceType,
            'ua' : config['browserUA'][deviceType]
        },
        'detail' : []
    }
    with tqdm(total=len(testCaseInfo), desc=testName) as pbar:
        for testCase in testCaseInfo:
            tmpTestResult = {
                'url' : testCase['url'],
                'actions' : []
            }
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
                    tmpTestResult['actions'].append(
                        {
                            'name' : constant.PHOTO_ACTION_NAME.lower(),
                            'status' : 1,
                            'data' : imgName
                        }
                    )
                elif action == constant.WAIT_ACTION_NAME:
                    testWebDriver.wait()
                    tmpTestResult['actions'].append(
                        {
                            'name' : constant.WAIT_ACTION_NAME.lower(),
                            'status' : 1,
                            'data' : ''
                        }
                    )
                elif not action.find(constant.SEARCH_ACTION_NAME) == -1:
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    if len(actionInfo) == 3:
                        restrictKeyword = actionInfo[1]
                        tmpSearchKeyword = actionInfo[2].split(',')
                        if len(tmpSearchKeyword) is 1:
                            searchKeyword = [actionInfo[2]]
                        else:
                            searchKeyword = tmpSearchKeyword
                        tmpTestResult['restrict'] = restrictKeyword
                        tmpTestResult['keyword'] = searchKeyword.sort()
                    else:
                        restrictKeyword = None
                        searchKeyword = None
                    diveWebServiceKeyword(
                        searchLogger=logger,
                        testWebDriver=testWebDriver,
                        testCaseName=testCase['name'],
                        extractedLinks=testWebDriver.getLinksInfo(
                            testCase['url'],
                            restrictKeyword
                        ),
                        restrictKeyword=restrictKeyword,
                        searchKeyword=searchKeyword,
                        testResult=tmpTestResult
                    )
                elif not action.find(constant.SCAN_ACTION_NAME) == -1:
                    global SERVICE_TMP_ID
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    if len(actionInfo) == 2:
                        restrictKeyword = actionInfo[1]
                        tmpTestResult['restrict'] = restrictKeyword
                    else:
                        restrictKeyword = None
                    SERVICE_LINKS.append(testCase['url'])
                    testWebDriver.takeFullScreenshot(
                        testDir=testCase['name'],
                        imgName=str(SERVICE_TMP_ID)
                    )
                    tmpTestResult['actions'].append(
                        {
                            'name' : constant.SCAN_ACTION_NAME.lower(),
                            'status' : 1,
                            'data' : {
                                'target' : testCase['url'],
                                'value' : str(SERVICE_TMP_ID)
                            }
                        }
                    )
                    SERVICE_TMP_ID = SERVICE_TMP_ID + 1
                    diveWebServiceLink(
                        testWebDriver=testWebDriver,
                        testCaseName=testCase['name'],
                        extractedLinks=testWebDriver.getLinksInfo(
                            testCase['url'],
                            restrictKeyword
                        ),
                        restrictKeyword=restrictKeyword,
                        testResult=tmpTestResult
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
                        tmpTestResult['actions'].append(
                            {
                                'name' : constant.INPUT_ACTION.lower(),
                                'status' : 1,
                                'data' : {
                                    'target' : tmpSelector,
                                    'value' : tmpOption
                                }
                            }
                        )
                    if tmpEvent == constant.ENTER_ACTION:
                        testWebDriver.enter(
                            dom=targetDom,
                            loopFlg=loopFlg
                        )
                        tmpTestResult['actions'].append(
                            {
                                'name' : constant.ENTER_ACTION.lower(),
                                'status' : 1,
                                'data' : {
                                    'target' : tmpSelector,
                                    'value' : ''
                                }
                            }
                        )
                    if tmpEvent == constant.CLICK_ACTION:
                        testWebDriver.click(
                            dom=targetDom,
                            loopFlg=loopFlg
                        )
                        tmpTestResult['actions'].append(
                            {
                                'name' : constant.CLICK_ACTION.lower(),
                                'status' : 1,
                                'data' : {
                                    'target' : tmpSelector,
                                    'value' : ''
                                }
                            }
                        )
            testResult['detail'].append(tmpTestResult)
            pbar.update(1)
    json.dump(testResult, reportConfigStream, indent=2)
    reportConfigStream.close()
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


def diveWebServiceKeyword(searchLogger, testWebDriver, testCaseName, extractedLinks, restrictKeyword, searchKeyword, testResult):
    u'''Recursive Diving - word
     @param  testWebDriver   - Web Driver
     @param  testCaseName    - Test Case Name
     @param  extractedLinks  - Extracted Links
     @param  restrictKeyword - Search Limit
     @param  searchKeyword   - Search Keywords
     @param  testResult      - Test Result
     @return void
    '''
    global SERVICE_TMP_ID
    for currentTmpLink in extractedLinks:
        if checkIsDivedLink(currentTmpLink):
            SERVICE_LINKS.append(currentTmpLink)
            try:
                testWebDriver.access(currentTmpLink)
                pickUpResult = testWebDriver.pickUpKeywords(currentTmpLink, searchKeyword)
                pickUpResult['value'] = str(SERVICE_TMP_ID)
                searchLogger.log(pickUpResult)
                testWebDriver.takeFullScreenshot(
                    testDir=testCaseName,
                    imgName=str(SERVICE_TMP_ID)
                )
                testResult['actions'].append(
                    {
                        'name' : constant.SEARCH_ACTION_NAME.lower(),
                        'status' : 1,
                        'data' : pickUpResult
                    }
                )
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
                    searchKeyword=searchKeyword,
                    testResult=testResult
                )
            except Exception as e:
                print('=====================================')
                print(currentTmpLink)
                print('=====================================')
                print(e)
                UNKNOWN_SERVICE_LINKS.append(currentTmpLink)
        else:
            DUPLICATED_SERVICE_LINKS.append(currentTmpLink)


def diveWebServiceLink(testWebDriver, testCaseName, extractedLinks, restrictKeyword, testResult):
    u'''Recursive Diving - link
     @param  testWebDriver   - Web Driver
     @param  testCaseName    - Test Case Name
     @param  extractedLinks  - Extracted Links
     @param  restrictKeyword - Search Limit
     @param  testResult      - Test Result
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
                    imgName=str(SERVICE_TMP_ID)
                )
                testResult['actions'].append(
                    {
                        'name' : constant.SCAN_ACTION_NAME.lower(),
                        'status' : 1,
                        'data' : {
                            'target' : currentTmpLink,
                            'value' : str(SERVICE_TMP_ID)
                        }
                    }
                )
                SERVICE_TMP_ID = SERVICE_TMP_ID + 1
                diveWebServiceLink(
                    testWebDriver=testWebDriver,
                    testCaseName=testCaseName,
                    extractedLinks=testWebDriver.getLinksInfo(
                        currentTmpLink,
                        restrictKeyword
                    ),
                    restrictKeyword=restrictKeyword,
                    testResult=testResult
                )
            except Exception as e:
                print('=====================================')
                print(currentTmpLink)
                print('=====================================')
                print(e)
                UNKNOWN_SERVICE_LINKS.append(currentTmpLink)
        else:
            DUPLICATED_SERVICE_LINKS.append(currentTmpLink)


def endAutoTest(testName, startTime):
    u'''Finish Auto Test
     @param  testName  - Test Case Name
     @param  startTime - Test Start Time
     @return void
    '''
    print(constant.BR + '====== ' + testName + ' [  END  ] ======' + constant.BR)
    print('{0} sec.'.format(time.time() - startTime))
