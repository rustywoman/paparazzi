#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import pickle
import re
import time
import urllib.request
import uuid
from bs4 import BeautifulSoup
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, urljoin


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
        try:
            with open(self.cache, 'rb') as f:
                self.rawHtml = pickle.load(f)
        except Exception as e:
            webDriver = webdriver.Chrome(
                executable_path=DRIVER_DIR + CHROME_DRIVER,
                chrome_options=DRIVER_OPTIONS
            )
            webDriver.get(url)
            # ToDo - Async Content or SPA
            time.sleep(5)
            self.rawHtml = webDriver.page_source
            webDriver.quit()
            with open(self.cache, 'wb') as f:
                pickle.dump(self.rawHtml, f)
        self.html = BeautifulSoup(self.rawHtml, 'lxml')

    def getHtml(self):
        u'''Get Html Via BeautifulSoup
         @return Html Object converted by BeautifulSoup
        '''
        return self.html

    def getOuterCss(self):
        u'''Get Css @ File Via BeautifulSoup
         @return Css File List
        '''
        return self.html.find_all(
            'link',
            {
                'rel': 'stylesheet'
            }
        )

    def getInlineImage(self):
        u'''Get Inline Image @ Raw Html Via BeautifulSoup
         @return Image List
        '''
        return self.html.find_all('img')

    def changeMultiToOneArray(self, selectorsList):
        u'''Change Multi List To Single List
         @param  selectorsList - Target Multi List
         @return Single List
        '''
        result = []
        for selectors in selectorsList:
            for selector in selectors:
                result.append(selector)
        return result

    def getDispFileName(self, cssName):
        u'''Get Display Name
         @return Slim Name for Display
        '''
        return os.path.basename(urlparse(cssName).path)

    def changeAbsPathToRelPath(self, domain, relativePath):
        u'''Change Absolute Path To Relative Path
         @param  domain       - Target Web Page Domain
         @param  relativePath - Target Asset's URL
         @return Asset's Relative Path
        '''
        return urljoin(domain, relativePath)

    def downloadImage(self, savedDirPath, domain, assetURL, inlineFlg=True):
        u'''Download Image
         @param  savedDirPath - Image Saved Directory Path
         @param  domain       - Target Web Page Domain
         @param  assetURL     - Target Image URL
         @param  inlineFlg    - Tag or Css
         @return Saved Status
        '''
        if inlineFlg:
            # Html Image Tag
            refinedImageURL = self.changeAbsPathToRelPath(domain, assetURL)
        else:
            # Background-Image @ Css
            refinedImageURL = self.changeAbsPathToRelPath(
                domain,
                re.sub('url\(\'|url\(\"|url\(|\'\)|\"\)|\)', '', assetURL)
            )
        localSavedImageURL = savedDirPath + str(uuid.uuid4().hex) + '_' + self.getDispFileName(refinedImageURL)
        try:
            with urllib.request.urlopen(refinedImageURL) as response:
                try:
                    with open(localSavedImageURL, 'wb') as scrapedImage:
                        data = response.read()
                        scrapedImage.write(data)
                        return True
                except Exception as ioEx:
                    return False
        except Exception as httpEx:
            return False
