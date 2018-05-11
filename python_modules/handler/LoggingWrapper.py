#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import logging
import logging.config
import os


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class LoggingWrapper(object):
    u'''Handler Class For Logging
    '''
    def __init__(self, loggerName, logFineName):
        u'''Constructor
         @param  loggerName - Logger Name
         @param  logFineName - Definition Name
        '''
        self.projectDir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            )
        )
        self.logDir = os.path.join(self.projectDir, 'log')
        self.confDir = os.path.join(self.projectDir, 'conf')
        if not os.path.exists(self.logDir):
            os.makedirs(self.logDir)
        logging.fileName = os.path.join(self.logDir, logFineName)
        logging.config.fileConfig(os.path.join(self.confDir, 'logging.conf'))
        self.logger = logging.getLogger(loggerName)

    def debug(self, msg):
        u'''Debug
         @param  msg - Debug Message
        '''
        self.logger.debug(msg)

    def log(self, msg):
        u'''Log
         @param  msg - Log Message
        '''
        self.logger.debug(msg)

    def info(self, msg):
        u'''Info
         @param  msg - Info. Message
        '''
        self.logger.info(msg)

    def warn(self, msg):
        u'''Warn
         @param  msg - Warn. Message
        '''
        self.logger.warning(msg)
