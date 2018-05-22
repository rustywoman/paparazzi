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
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, urljoin


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WebCachingWrapper(object):
    u'''Handler Class For Web Caching
    '''
    def __init__(self, cacheDir, cacheName, url, screenshotDir):
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
                # print('>>> Load Pickle Cache <<<\n')
                self.rawHtml = pickle.load(f)
        except Exception as e:
            webDriver = webdriver.Chrome(
                executable_path=DRIVER_DIR + CHROME_DRIVER,
                chrome_options=DRIVER_OPTIONS
            )
            # Check - HD
            webDriver.set_window_size(1280, 720)
            webDriver.get(url)
            # ToDo - Async Content or SPA
            time.sleep(5)
            self.rawHtml = webDriver.page_source
            self.takeHDCapture(webDriver, screenshotDir)
            webDriver.quit()
            with open(self.cache, 'wb') as f:
                pickle.dump(self.rawHtml, f)
            # print('>>> Save Pickle Cache <<<\n')
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

    def customConcat(self, targetImages, startIdx, resultFileName):
        u'''Concat Cache Images
         @param  targetImages   - Target Images List
         @param  startIdx       - Concat Start Index
         @param  resultFileName - Result File Name
        '''
        tmpImages = targetImages[startIdx:startIdx + 2]
        try:
            resultImg = Image.open(resultFileName)
        except Exception as e:
            resultImg = None
        if len(tmpImages) is 2:
            if resultImg is None:
                # 初回のみ
                tmpImg1 = tmpImages[0]
                tmpImg2 = tmpImages[1]
                dst = Image.new(
                    'RGB',
                    (tmpImg1['width'], tmpImg1['height'] + tmpImg2['height'])
                )
                dst.paste(tmpImg1['ins'], (0, 0))
                dst.paste(tmpImg2['ins'], (0, tmpImg1['height']))
                dst.save(resultFileName)
            else:
                tmpImg1 = tmpImages[0]
                tmpImg2 = tmpImages[1]
                dst = Image.new(
                    'RGB',
                    (tmpImg1['width'], tmpImg1['height'] + tmpImg2['height'])
                )
                dst.paste(tmpImg1['ins'], (0, 0))
                dst.paste(tmpImg2['ins'], (0, tmpImg1['height']))
                nextDst = Image.new(
                    'RGB',
                    (resultImg.width, resultImg.height + dst.height)
                )
                nextDst.paste(resultImg, (0, 0))
                nextDst.paste(dst, (0, resultImg.height))
                nextDst.save(resultFileName)
            self.customConcat(targetImages, startIdx + 2, resultFileName)
        else:
            tmpLastImg = tmpImages[0]
            dst = Image.new(
                'RGB',
                (resultImg.width, resultImg.height + tmpLastImg['height'])
            )
            dst.paste(resultImg, (0, 0))
            dst.paste(tmpLastImg['ins'], (0, resultImg.height))
            dst.save(resultFileName)

    def takeHDCapture(self, webDriver, savedDirPath):
        u'''Take HD Capture
         @param  webDriver    - Selenium Web Driver
         @param  savedDirPath - Captured Images Save Directory
         @return True
        '''
        nextYPosition = 0
        capturedIdx = 1
        scrollFlg = True
        tmpCacheImgs = []
        wholeHeight = webDriver.execute_script(
            'return document.body.parentNode.scrollHeight'
        )
        viewportWidth = webDriver.execute_script(
            'return window.innerWidth'
        )
        viewportHeight = webDriver.execute_script(
            'return window.innerHeight'
        )
        overScrollBuffer = 0
        if wholeHeight <= viewportHeight:
            webDriver.save_screenshot(savedDirPath + '___result.png')
            tmpImg = Image.open(savedDirPath + '___result.png').resize((viewportWidth, viewportHeight), Image.LANCZOS)
            tmpImg.save(savedDirPath + '___result.png')
        else:
            while scrollFlg:
                if nextYPosition > wholeHeight:
                    overScrollBuffer = nextYPosition - wholeHeight
                    scrollFlg = False
                else:
                    nextYPosition = nextYPosition + viewportHeight
                    tmpCapturedImgName = '{0}___tmp_captured_{1}.png'.format(savedDirPath, capturedIdx)
                    webDriver.save_screenshot(tmpCapturedImgName)
                    tmpCacheImgs.append(tmpCapturedImgName)
                    capturedIdx = capturedIdx + 1
                    webDriver.execute_script(
                        'window.scrollTo(0, {0})'.format(nextYPosition)
                    )
                    time.sleep(0.25)

        # Collect Caches
        tmpCacheImgs.sort()
        # Resize
        parsedImages = []
        resizeLoopLimit = len(tmpCacheImgs)
        resizeLoopIdx = 0
        for tmpCacheImg in tmpCacheImgs:
            # http://pillow.readthedocs.io/en/4.0.x/handbook/concepts.html#filters
            tmpImg = Image.open(tmpCacheImg).resize((viewportWidth, viewportHeight), Image.LANCZOS)
            resizeLoopIdx = resizeLoopIdx + 1
            if resizeLoopIdx is resizeLoopLimit:
                tmpImg = tmpImg.crop((0, overScrollBuffer, viewportWidth, viewportHeight))
                parsedImages.append(
                    {
                        'src': tmpCacheImg,
                        'ins': tmpImg,
                        'width': viewportWidth,
                        'height': viewportHeight - overScrollBuffer
                    }
                )
            else:
                parsedImages.append(
                    {
                        'src': tmpCacheImg,
                        'ins': tmpImg,
                        'width': viewportWidth,
                        'height': viewportHeight
                    }
                )
            # Byte化した一時画像を削除
            os.remove(tmpCacheImg)
        # Concat
        if len(parsedImages) > 0:
            self.customConcat(parsedImages, 0, savedDirPath + '___result.png')

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
