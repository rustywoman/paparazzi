#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import Configuration Dir.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import random
import sys
import uuid
from google_measurement_protocol import Event, report, PageView
from time import sleep
from tqdm import tqdm


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def extractRandomIdx(valList):
    return random.randint(0, len(valList) - 1)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    args = sys.argv
    # Tracking ID
    TRACKING_ID = args[1]
    # User Number
    DUMMY_USER_NUMBER = 2000
    GA_PARAM_SPLITTER = '_'
    DOMAIN = 'http://example.org'
    TARGET_PAGE = ['/', '/detail', '/search']
    PAGE_TITLE = ['トップ', '詳細', '検索結果']
    EVENT_CATEGORY_SERVICE = ['t']
    EVENT_CATEGORY_PAGE = ['top', 'detail', 'search']
    EVENT_CATEGORY_LOCATION = ['header', 'banner', 'content', 'footer']
    EVENT_CATEGORY_DOM = ['a']
    EVENT_ACTION = ['click', 'blur']
    EVENT_LABEL = ['campaign']
    EVENT_LABEL_SUFFIX = ['20180101', '20171231']
    with tqdm(total=DUMMY_USER_NUMBER) as pbar:
        for i in range(DUMMY_USER_NUMBER):
            CLIENT_ID = uuid.uuid4()
            PAGE_IDX = extractRandomIdx(TARGET_PAGE)
            pbar.set_description('Processing No. {0} / {1} | ID : {2}'.format(i + 1, DUMMY_USER_NUMBER, CLIENT_ID))
            report(
                TRACKING_ID,
                CLIENT_ID,
                PageView(
                    path=TARGET_PAGE[PAGE_IDX],
                    title=PAGE_TITLE[PAGE_IDX]
                )
            )
            tmpCategory = GA_PARAM_SPLITTER.join(
                [
                    EVENT_CATEGORY_SERVICE[extractRandomIdx(EVENT_CATEGORY_SERVICE)],
                    EVENT_CATEGORY_PAGE[PAGE_IDX],
                    EVENT_CATEGORY_LOCATION[extractRandomIdx(EVENT_CATEGORY_LOCATION)],
                    EVENT_CATEGORY_DOM[extractRandomIdx(EVENT_CATEGORY_DOM)]
                ]
            )
            tmpAction = EVENT_ACTION[extractRandomIdx(EVENT_ACTION)]
            tmpLabel = GA_PARAM_SPLITTER.join(
                [
                    EVENT_LABEL[extractRandomIdx(EVENT_LABEL)],
                    EVENT_LABEL_SUFFIX[extractRandomIdx(EVENT_LABEL_SUFFIX)]
                ]
            )
            report(
                TRACKING_ID,
                CLIENT_ID,
                Event(
                    category=tmpCategory,
                    action=tmpAction,
                    label=tmpLabel
                )
            )
            pbar.update(1)
            sleep(1)
