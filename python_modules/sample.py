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
from pytz import timezone
from tqdm import tqdm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def outputAsciiArt():
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
    testCaseIdx = 1
    testCaseStack = []
    print(constant.BR)
    print('> Selecable Test Case [X]')
    for root, dirs, files in os.walk(testCaseDir):
        for file in files:
            print('  [{0}] - {1}'.format(
                testCaseIdx,
                file.replace(
                    constant.TEST_CASE_EXT,
                    constant.EMPTY
                )
            ))
            testCaseIdx = testCaseIdx + 1
            testCaseStack.append(file)
    return testCaseStack


def selectTestCase(testCaseDir, testCaseStack):
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
    utcNow = dt.now(timezone('UTC'))
    print(constant.BR + '====== ' + testName + ' [ START ] ======')
    print('Date : {0}'.format(utcNow.astimezone(timezone('Asia/Tokyo')).strftime('%Y.%m.%d %H:%M:%S')) + constant.BR)
    print('Initializing Dummy Browser ...')
    return time.time()


def executeAutoTest(testName, testCaseInfo):
    print('Execute Auto Test ...' + constant.BR)
    testWebDriver = paparazzi.WebDriverWrapper(
        screenshotDir=config['screenshot']['dir']
    )
    testWebDriver.maximumWindow()
    with tqdm(total=len(testCaseInfo)) as pbar:
        for testCase in testCaseInfo:
            testWebDriver.access(testCase['url'])
            for action in testCase['action']:
                if action == constant.PHOTO_ACTION_NAME:
                    testWebDriver.scrollToTop()
                    testWebDriver.takeFullScreenshot(
                        testDir=testName,
                        imgName=testCase['name']
                    )
                elif action == constant.WAIT_ACTION_NAME:
                    testWebDriver.wait()
                else:
                    loopFlg = False
                    actionInfo = action.split(constant.ACTION_SPLIT_ID)
                    tmpEvent = actionInfo[0]
                    tmpSelectorType = actionInfo[1]
                    tmpSelector = actionInfo[2]
                    try:
                        tmpOption = actionInfo[3]
                    except:
                        tmpOption = constant.EMPTY
                    if tmpSelectorType == 'xpath':
                        targetDom = testWebDriver.getElementByXPath(tmpSelector)
                    if tmpSelectorType == 'id':
                        targetDom = testWebDriver.getElementById(tmpSelector)
                    if tmpSelectorType == 'class':
                        targetDom = testWebDriver.getElementsByClassName(tmpSelector)
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
    print(constant.BR + '====== ' + testName + ' [  END  ] ======')
    print('{0} sec.{1}'.format(time.time() - startTime, constant.BR))


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
