#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import jsbeautifier
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

    def getHtmlTitle(self):
        u'''Get Html Title Via BeautifulSoup
         @return Html Title
        '''
        return self.html.title.string

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

    def getOuterScript(self):
        u'''Get Script @ File Via BeautifulSoup
         @return Script File List
        '''
        return self.html.find_all(
            'script',
            {
                'src': True
            }
        )

    def getInlineMeta(self):
        u'''Get Inline Meta @ Raw Html Via BeautifulSoup
         @return Meta List
        '''
        return self.html.find_all('meta')

    def getInlineText(self):
        u'''Get Inline Text @ Raw Html Via BeautifulSoup
         @return Text List
        '''
        textDOM = self.html.find_all(
            [
                'h1',
                'h2',
                'h3',
                'h4',
                'h5',
                'h6',
                'article',
                'section',
                'div',
                'p',
                'span',
                'i',
                'a'
            ]
        )
        textReport = []
        for dom in textDOM:
            if dom.string is not None:
                stripDOMString = dom.string.strip()
                if stripDOMString is not '':
                    textReport.append(stripDOMString)
        textReport = list(set(textReport))
        textReport = sorted(textReport, key=str.lower)
        return textReport

    def getInlineImage(self):
        u'''Get Inline Image @ Raw Html Via BeautifulSoup
         @return Image List
        '''
        return self.html.find_all('img')

    def getInlineStyle(self):
        u'''Get Inline Style @ Raw Html Via BeautifulSoup
         @return Style List
        '''
        return self.html.find_all('style')

    def getInlineScript(self, spliterStr):
        u'''Get Inline Script @ Raw Html Via BeautifulSoup
         @return Script List
        '''
        opts = jsbeautifier.default_options()
        opts.indent_size = 2
        opts.space_in_empty_paren = True
        tmpInnerScripts = self.html.find_all(
            'script',
            {
                'src': False
            }
        )
        resultList = []
        for script in tmpInnerScripts:
            rawScript = jsbeautifier.beautify(script.string, opts).split(spliterStr)
            formatScript = []
            for splitRawScript in rawScript:
                # ToDo - Comment '/* hogehoge */'
                if splitRawScript is not '' and re.match('^//', splitRawScript) is None:
                    formatScript.append(splitRawScript)
            resultList.append(spliterStr.join(formatScript))
        return resultList

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

    def downloadImage(self, savedDirPath, domain, assetURL):
        u'''Download Image
         @param  savedDirPath - Image Saved Directory Path
         @param  domain       - Target Web Page Domain
         @param  assetURL     - Target Image URL
         @return Saved Status
        '''
        refinedImageURL = self.changeAbsPathToRelPath(
            domain,
            re.sub('url\(\'|url\(\"|url\(|\'\)|\"\)|\)', '', assetURL)
        )
        localSavedImageURL = savedDirPath + str(uuid.uuid4().hex) + '_' + self.getDispFileName(refinedImageURL)
        result = {
            'status': 0,
            'path': {
                'raw': refinedImageURL,
                'local': localSavedImageURL
            }
        }
        try:
            with urllib.request.urlopen(refinedImageURL) as response:
                try:
                    with open(localSavedImageURL, 'wb') as scrapedImage:
                        data = response.read()
                        scrapedImage.write(data)
                        result['status'] = 1
                        result['path']['local'] = localSavedImageURL.replace(savedDirPath, '')
                        return result
                except Exception as ioEx:
                    result['status'] = 0
                    result['path']['local'] = localSavedImageURL.replace(savedDirPath, '')
                    return result
        except Exception as httpEx:
            result['status'] = -1
            result['path']['local'] = localSavedImageURL.replace(savedDirPath, '')
            return result
