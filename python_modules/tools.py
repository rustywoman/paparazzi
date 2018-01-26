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
import json
import time
from datetime import datetime as dt
from pytz import timezone


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


def getMainScriptFileName(fileName):
    u'''Get Main Script Name
     @param  fileName - __filename__
     @return Main Script File Name without python extension
    '''
    return os.path.basename(fileName).replace(constant.PYTHON_EXT, constant.EMPTY)


def selectDeviceType():
    u'''Select Device Type
     @return Selected Device Type
    '''
    testDeviceTypeFlg = False
    deviceTypeList = ['pc', 'tablet', 'sp']
    while not testDeviceTypeFlg:
        for deviceTypeIdx in range(len(deviceTypeList)):
            print('  [{0}] - {1}'.format(deviceTypeIdx + 1, deviceTypeList[deviceTypeIdx]))
        testDeviceTypeIdx = input('> Input Device Type Index ::: ')
        try:
            testDeviceTypeIdx = deviceTypeList[int(testDeviceTypeIdx) - 1]
            testDeviceTypeFlg = True
        except Exception as e:
            testDeviceTypeFlg = False
            print('  Warning - Input Device Type Index !')
    return testDeviceTypeIdx


def selectBrowser():
    u'''Select Browser
     @return Selected Browser Type
    '''
    testBrowserFlg = False
    browserList = ['chrome', 'firefox', 'edge']
    while not testBrowserFlg:
        for browserIdx in range(len(browserList)):
            print('  [{0}] - {1}'.format(browserIdx + 1, browserList[browserIdx]))
        testBrowserTypeIdx = input('> Input Browser Index ::: ')
        try:
            testBrowserTypeIdx = browserList[int(testBrowserTypeIdx) - 1]
            testBrowserFlg = True
        except Exception as e:
            testBrowserFlg = False
            print('  Warning - Input Browser Index !')
    return testBrowserTypeIdx


def listUpTestCases(testCaseDir, execFileName):
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
            if not file.find(execFileName) == -1:
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


def endAutoTest(testName, startTime):
    u'''Finish Auto Test
     @param  testName  - Test Case Name
     @param  startTime - Test Start Time
     @return void
    '''
    print(constant.BR + '====== ' + testName + ' [  END  ] ======')
    print('{0} sec.{1}'.format(time.time() - startTime, constant.BR))
