#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import configparser
import os
import sys


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Definition
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
config = configparser.ConfigParser()
config.read(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    ) + '/conf/paparazzi.conf'
)
u'''設定ファイルの項目数を保持。
'''
configCheck = len(config.sections())


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if configCheck == 0:
    u'''設定ファイルの項目が0の場合、「ファイル未配置」と判断し、例外発火。
    '''
    raise Exception('\"paparazzi.conf\" doesn\'t exist !!!')
else:
    u'''設定ファイルの項目が確認できた場合、「CONFIG.」プレフィックスで定数化。
    '''
    sys.modules[__name__] = config
