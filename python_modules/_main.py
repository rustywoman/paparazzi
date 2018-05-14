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
from datetime import datetime
from handler import LoggingWrapper as log


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
    tools.executeAutoTest(
        logger=log.LoggingWrapper(
            loggerName=constant.DEFAULT_LOGGER_NAME,
            logFineName=TEST_NAME + '_' + datetime.now().strftime(constant.LOG_TIMESTAMP_FORMAT) + constant.LOG_EXT
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
