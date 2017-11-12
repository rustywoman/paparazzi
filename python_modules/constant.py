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
    u'''CONSTANTとしてエクスポートするための、一時クラス。
    '''
    class ConstError(TypeError):
        u'''未定義の値を照会しようとした場合の内部空例外クラス。
         @param  TypeError エラー文言
         @return Empty
        '''
        pass

    def __setattr__(self, name, value):
        u'''自変数設定関数を上書き。
         @param  name  定数化したい値の名前
         @param  value 定数化したい値そのもの
         @return 設定済み定数値を返却。
         ただし、重複して、同じ名前の値を設定しようとした場合には、内部空例外を発火。
        '''
        if name in self.__dict__:
            raise self.ConstError('Can\'t rebind const(%s)' % name)
        self.__dict__[name] = value

    def __delattr__(self, name):
        u'''自変数削除関数を上書き。
         @param  name  削除したい値の名前
         @return 原則削除不可能。
         既に設定されている定数を消そうとした場合には、内部空例外を発火。
         未設定の定数を消そうとした場合には、NameErrorを発火。
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

u'''[CONST] Empty String'''
constant.EMPTY = ''

u'''[CONST] String [br]'''
constant.BR = ''

u'''[CONST] String [---]'''
constant.ACTION_SPLIT_ID = '---'

u'''[CONST] String [WAIT]'''
constant.WAIT_ACTION_NAME = 'WAIT'

u'''[CONST] String [PHOTO]'''
constant.PHOTO_ACTION_NAME = 'PHOTO'

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
