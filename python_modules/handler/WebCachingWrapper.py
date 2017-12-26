#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import pickle
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WebCachingWrapper(object):
    u'''Handler Class For Web Caching
    '''
    def __init__(self, cacheDir, cacheName, url):
        u'''Constructor
         @param  cacheDir  - Directory Name
         @param  cacheName - Cache Name
         @param  url       - Target URL
        '''
        CHROME_DRIVER = '/chromedriver.exe'
        DRIVER_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            ) + os.path.sep + 'driver'
        )
        DRIVER_OPTIONS = Options()
        DRIVER_OPTIONS.add_argument('--headless')
        self.name = 'WebCachingWrapper'
        self.cache = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            ) + os.path.sep + cacheDir
        ) + os.path.sep + cacheName + '.pickle'
        # cachedTime = dt.fromtimestamp(os.stat(self.cache).st_mtime)
        # now = dt.now()
        # delta = (now - cacheTime).total_seconds()
        # print(delta)
        try:
            with open(self.cache, 'rb') as f:
                self.rawHtml = pickle.load(f)
        except Exception as e:
            webDriver = webdriver.Chrome(
                executable_path=DRIVER_DIR + CHROME_DRIVER,
                chrome_options=DRIVER_OPTIONS
            )
            webDriver.get(url)
            self.rawHtml = webDriver.page_source
            webDriver.quit()
            with open(self.cache, 'wb') as f:
                pickle.dump(self.rawHtml, f)
        self.html = BeautifulSoup(self.rawHtml, 'lxml')

    def getHtml(self):
        u'''Get Html Via BeautiflSoup
         @return Html Object converted by BeautifulSoup
        '''
        return self.html

    def loadRawCss(self, cssName):
        u'''Load Raw Css Information
         @return Decoded Css Information
        '''
        try:
            rawCss = str(urllib.request.urlopen(cssName).read().decode(encoding='utf-8'))
        except Exception as e:
            rawCss = str(urllib.request.urlopen(cssName).read().decode(encoding='shift_jis'))
        return rawCss

    def getDispFileName(self, cssName):
        u'''Get Display Name
         @return Slim Name for Display
        '''
        return os.path.basename(urlparse(cssName).path)
