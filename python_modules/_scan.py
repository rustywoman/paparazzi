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
import shutil
import tools
from datetime import datetime
from handler import LoggingWrapper as log


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    tools.outputAsciiArt()
    TEST_TMP_REPORTS_DIR = os.path.sep.join(
        [
            config['report']['tmp-dir']
        ]
    )
    if not os.path.exists(TEST_TMP_REPORTS_DIR):
        os.makedirs(TEST_TMP_REPORTS_DIR)
    TEST_TMP_REPORTS_DIR = TEST_TMP_REPORTS_DIR + os.path.sep
    TEST_SAVED_REPORTS_DIR = os.path.sep.join(
        [
            config['report']['dir'],
            'assets',
            'json'
        ]
    )
    if not os.path.exists(TEST_SAVED_REPORTS_DIR):
        os.makedirs(TEST_SAVED_REPORTS_DIR)
    TEST_SAVED_REPORTS_DIR = TEST_SAVED_REPORTS_DIR + os.path.sep
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
    tmpResultInfoFiles = os.listdir(TEST_TMP_REPORTS_DIR)
    for resultInfoFile in tmpResultInfoFiles:
        if resultInfoFile.replace(constant.TEST_CASE_EXT, '') == TEST_NAME:
            shutil.copyfile(
                TEST_TMP_REPORTS_DIR + resultInfoFile,
                TEST_SAVED_REPORTS_DIR + resultInfoFile
            )
    indexLinkList = []
    tmpReportInfoFiles = os.listdir(TEST_SAVED_REPORTS_DIR)
    for researchResult in tmpReportInfoFiles:
        indexLinkList.append(
            {
                'name': researchResult.replace(constant.TEST_CASE_EXT, constant.EMPTY),
                'path': '/___' + researchResult.replace(constant.TEST_CASE_EXT, ''),
                'date': tools.getTimeFromEpoc(os.path.getctime(TEST_SAVED_REPORTS_DIR + researchResult))
            }
        )
    indexLinkStream = open(
        os.path.sep.join(
            [
                config['report']['dir'],
                'index' + constant.TEST_CASE_EXT
            ]
        ),
        'w'
    )
    json.dump(indexLinkList, indexLinkStream, indent=2)
    indexLinkStream.close()
    tools.endAutoTest(
        testName=TEST_NAME,
        startTime=START_TIME
    )