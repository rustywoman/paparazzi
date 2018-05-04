#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class ConsoleWrapper(object):
    u'''Static Class For Print
    '''
    def __init__(self):
        u'''Constructor
        '''
        # underline
        self.UNDERLINE = '\033[4m'
        # color
        self.STR_BLACK = '\033[90m'
        self.STR_RED = '\033[91m'
        self.STR_GREEN = '\033[92m'
        self.STR_YELLOW = '\033[93m'
        self.STR_BLUE = '\033[94m'
        self.STR_PURPLE = '\033[95m'
        self.STR_CYAN = '\033[96m'
        self.STR_WHITE = '\033[97m'
        # Background
        self.BG_RED = '\033[41m'
        self.BG_GREEN = '\033[42m'
        self.BG_YELLOW = '\033[43m'
        self.BG_BLUE = '\033[44m'
        self.BG_PURPLE = '\033[45m'
        self.BG_CYAN = '\033[46m'
        self.BG_WHITE = '\033[47m'
        # reset
        self.END_CODE = '\033[0m'
        # tab
        self.TAB = '    '

    def customPrint(self, color, msg):
        u'''Print Wrapper
         @param  color - Print Color Code
         @param  msg   - Print Message
        '''
        print('{0}{1}{2}'.format(color, msg, self.END_CODE))

    def log(self, msg):
        u'''Print OK
         @param  msg - OK Message
        '''
        self.customPrint(self.STR_GREEN, msg)

    def info(self, msg):
        u'''Print INFORMATION
         @param  msg - INFORMATION Message
        '''
        self.customPrint(self.STR_CYAN, msg)

    def error(self, msg):
        u'''Print ERROR
         @param  msg - ERROR Message
        '''
        self.customPrint(self.STR_RED, msg)

    def warn(self, msg):
        u'''Print WARN
         @param  msg - WARN Message
        '''
        self.customPrint(self.STR_YELLOW, msg)
