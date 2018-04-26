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
import multiprocessing as multi
import numpy as np
# ---
from handler import LoggingWrapper as log
from multiprocessing import Pool


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Global
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEST_CASE_GROUP_IDX = 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def bridgeMultiSeleniumHandler(testName, browserName, deviceType, testCase, groupIdx):
    tools.executeAutoTest(
        logger=log.LoggingWrapper(
            loggerName=constant.DEFAULT_LOGGER_NAME,
            logFineName=testName + constant.LOG_EXT
        ),
        testName=testName + '_' + str(groupIdx),
        testCaseInfo=testCase,
        browserName=browserName,
        deviceType=deviceType
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    TEST_CASE_DIR = config['test']['dir']
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
    POOL_LIMIT = multi.cpu_count()
    SPLIT_TEST_CASE = np.array_split(np.array(TEST_CASE), POOL_LIMIT)
    print(constant.BR + '====== [ {0} ] Connection ======'.format(POOL_LIMIT))
    POOL = Pool(POOL_LIMIT)
    for testCaseGroup in SPLIT_TEST_CASE:
        POOL.apply_async(
            bridgeMultiSeleniumHandler,
            args=(
                TEST_NAME,
                BROWSER_NAME,
                DEVICE_TYPE,
                testCaseGroup,
                TEST_CASE_GROUP_IDX
            )
        )
        TEST_CASE_GROUP_IDX = TEST_CASE_GROUP_IDX + 1
    POOL.close()
    START_TIME = tools.startAutoTest(TEST_NAME)
    POOL.join()
    tools.endAutoTest(
        testName=TEST_NAME,
        startTime=START_TIME
    )
