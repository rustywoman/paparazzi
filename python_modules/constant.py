#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sys


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class _const(object):
    u'''Temporary Class For Constant in Python
    '''
    class ConstError(TypeError):
        u'''Custom Inner Error for Undiefined Constant
         @param  TypeError - Error
         @return void
        '''
        pass

    def __setattr__(self, name, value):
        u'''Setter For Constant
         @param  name  - Constant Name
         @param  value - Constant Value
         @return Constant
        '''
        if name in self.__dict__:
            raise self.ConstError('Can\'t rebind const(%s)' % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        u'''Delattr For Constant
         @param  name - Constant Name
         @return Custom Inner Error
        '''
        if name in self.__dict__:
            raise self.ConstError('Can\'t unbind const(%s)' % name)
        raise NameError(name)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Instance
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
constant = _const()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Definition
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
u'''[CONST] Status "OK"'''
constant.OK = 1

u'''[CONST] Status "NG"'''
constant.NG = 0

u'''[CONST] Log Splitter'''
constant.SPLITTER = '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-'

u'''[CONST] Test Case Extension'''
constant.TEST_CASE_EXT = '.json'

u'''[CONST] Log File Extension'''
constant.LOG_EXT = '.log'

u'''[CONST] Python File Extension'''
constant.PYTHON_EXT = '.py'

u'''[CONST] Empty String'''
constant.EMPTY = ''

u'''[CONST] String [br]'''
constant.BR = '\n'

u'''[CONST] String [---]'''
constant.ACTION_SPLIT_ID = '---'

u'''[CONST] String [___]'''
constant.CASE_TEST_PREFIX = '___'

u'''[CONST] String [logPaparazzi]'''
constant.DEFAULT_LOGGER_NAME = 'logPaparazzi'

u'''[CONST] String [WAIT]'''
constant.WAIT_ACTION_NAME = 'WAIT'

u'''[CONST] String [PHOTO]'''
constant.PHOTO_ACTION_NAME = 'PHOTO'

u'''[CONST] String [SCAN]'''
constant.SCAN_ACTION_NAME = 'SCAN'

u'''[CONST] String [SEARCH]'''
constant.SEARCH_ACTION_NAME = 'SEARCH'

u'''[CONST] String [input]'''
constant.INPUT_ACTION = 'input'

u'''[CONST] String [enter]'''
constant.ENTER_ACTION = 'enter'

u'''[CONST] String [click]'''
constant.CLICK_ACTION = 'click'


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Export
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sys.modules[__name__] = constant
