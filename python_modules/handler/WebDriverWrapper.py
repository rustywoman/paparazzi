#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import re
import time
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
from urllib.parse import urlparse


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WebDriverWrapper(object):
    u'''Handler Class For Web Driver [ chrome, Firefox, IE(edge) ]
    '''
    def __init__(self, screenshotDir, browser, device, options):
        u'''Constructor
         @param  screenshotDir - Directory Name
         @param  browser       - Browser Name
         @param  device        - Device Name
         @param  options       - Browser Options
        '''
        tmpBrowserSize = options['SIZE'].split(',')
        CHROME_DRIVER = os.path.sep + 'chromedriver.exe'
        GECHO_DRIVER = os.path.sep + 'geckodriver.exe'
        EDGE_DRIVER = os.path.sep + 'MicrosoftWebDriver.exe'
        DRIVER_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            ) + os.path.sep + 'driver'
        )
        self.name = 'WebDriverWrapper'
        self.screenshotDir = screenshotDir
        if browser == 'edge':
            # -------------------
            # Edge
            # -------------------
            self.driver = webdriver.Edge(DRIVER_DIR + EDGE_DRIVER)
            self.setMaximumWindowSize()
        elif browser == 'firefox':
            # -------------------
            # Firefox
            # -------------------
            if device == 'pc':
                self.driver = webdriver.Firefox(
                    executable_path=DRIVER_DIR + GECHO_DRIVER,
                    log_path=os.devnull
                )
                self.setMaximumWindowSize()
            elif device == 'tablet' or device == 'sp':
                profile = webdriver.FirefoxProfile()
                profile.set_preference('general.useragent.override', options['UA'])
                self.driver = webdriver.Firefox(
                    firefox_profile=profile,
                    executable_path=DRIVER_DIR + GECHO_DRIVER,
                    log_path=os.devnull
                )
                self.setCustomWindowSize(tmpBrowserSize[0], tmpBrowserSize[1])
        else:
            # -------------------
            # Chrome
            # -------------------
            if device == 'pc':
                self.driver = webdriver.Chrome(
                    executable_path=DRIVER_DIR + CHROME_DRIVER
                )
                self.setMaximumWindowSize()
            elif device == 'tablet' or device == 'sp':
                opts = Options()
                opts.add_argument('user-agent=' + options['UA'])
                self.driver = webdriver.Chrome(
                    executable_path=DRIVER_DIR + CHROME_DRIVER,
                    chrome_options=opts
                )
                self.setCustomWindowSize(tmpBrowserSize[0], tmpBrowserSize[1])

    def setMaximumWindowSize(self):
        u'''Maximum Browser Window Size
         @return void
        '''
        self.driver.maximize_window()

    def setCustomWindowSize(self, width, height):
        u'''Maximum Browser Window Size
         @param  width  - Window Width
         @param  height - Window Height
         @return void
        '''
        self.driver.set_window_size(width, height)

    def access(self, url):
        u'''Access
         @param  url - URL
         @return void
        '''
        self.driver.get(url)
        self.wait(2)

    def wait(self, interval=5):
        u'''Wait
         @param  interval - Interval For Browser Rendering
         @return True
        '''
        time.sleep(interval)
        # ToDo - Waiting until Specific DOM Loaded
        # try:
        #     WebDriverWait(self.driver, 20).until(
        #         expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '#wrapper'))
        #     )
        # except TimeoutException:
        #     print('Couldn\'t get Loaded DOM. ---> End.')

    def getCurrentDir(self):
        u'''Get Current Directory
         @return Absolute Path For Current Directory
        '''
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            )
        )

    def makeResultStackDir(self, root, name):
        u'''Make Test Case Directory
         @param  root - Root Directory For Test Result
         @param  name - Test Case Name
         @return True
        '''
        os.makedirs(os.path.sep.join([self.getCurrentDir(), root, name]))
        return True

    def getResultStackDir(self, root, name):
        u'''Get Test Case Directory
         @param  root - Root Directory For Test Result
         @param  name - Test Case Name
         @return Absolute Path For Test Result Directory
        '''
        tmpStackDir = os.path.sep.join([self.getCurrentDir(), root, name])
        if not os.path.exists(tmpStackDir):
            self.makeResultStackDir(root, name)
        return tmpStackDir + os.path.sep

    def customConcat(self, targetImages, startIdx, resultFileName):
        tmpImages = targetImages[startIdx:startIdx + 2]
        try:
            resultImg = Image.open(resultFileName)
        except Exception as e:
            resultImg = None
        if len(tmpImages) is 2:
            tmpImg1 = tmpImages[0]
            tmpImg2 = tmpImages[1]
            dst = Image.new(
                'RGB',
                (tmpImg1['width'], tmpImg1['height'] + tmpImg2['height'])
            )
            dst.paste(tmpImg1['ins'], (0, 0))
            dst.paste(tmpImg2['ins'], (0, tmpImg1['height']))
            dst.save(resultFileName)
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

    def takeFullScreenshot(self, testDir, imgName):
        u'''Take Screenshots
         @param  testDir - Test Case Directory
         @param  name - Test Case Name
         @return True
        '''
        root = self.screenshotDir + os.path.sep + testDir
        nextYPosition = 0
        capturedIdx = 1
        scrollFlg = True
        tmpCacheImgs = []
        wholeHeight = self.driver.execute_script(
            'return document.body.parentNode.scrollHeight'
        )
        viewportWidth = self.driver.execute_script(
            'return window.innerWidth'
        )
        viewportHeight = self.driver.execute_script(
            'return window.innerHeight'
        )
        overScrollBuffer = 0
        tmpImageRootDir = self.getResultStackDir(root, imgName)
        if wholeHeight <= viewportHeight:
            self.driver.save_screenshot(tmpImageRootDir + '___result.png')
            tmpImg = Image.open(tmpImageRootDir + '___result.png').resize((viewportWidth, viewportHeight), Image.LANCZOS)
            tmpImg.save(tmpImageRootDir + '___result.png')
        else:
            while scrollFlg:
                if nextYPosition > wholeHeight:
                    overScrollBuffer = nextYPosition - wholeHeight
                    scrollFlg = False
                else:
                    nextYPosition = nextYPosition + viewportHeight
                    tmpCapturedImgName = '{0}___tmp_captured_{1}.png'.format(tmpImageRootDir, capturedIdx)
                    self.driver.save_screenshot(tmpCapturedImgName)
                    tmpCacheImgs.append(tmpCapturedImgName)
                    capturedIdx = capturedIdx + 1
                    self.driver.execute_script(
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
            self.customConcat(parsedImages, 0, tmpImageRootDir + '___result.png')
        return True
        # root = self.screenshotDir + os.path.sep + testDir
        # totalWidth = self.driver.execute_script(
        #     'return window.innerWidth'
        # )
        # totalHeight = self.driver.execute_script(
        #     'return document.body.parentNode.scrollHeight'
        # )
        # viewportWidth = self.driver.execute_script(
        #     'return document.body.clientWidth'
        # )
        # viewportHeight = self.driver.execute_script(
        #     'return window.innerHeight'
        # )
        # rectangles = []
        # i = 0
        # while i < totalHeight:
        #     ii = 0
        #     topHeight = i + viewportHeight
        #     if topHeight > totalHeight:
        #         topHeight = totalHeight
        #     while ii < totalWidth:
        #         topWidth = ii + viewportWidth
        #         if topWidth > totalWidth:
        #             topWidth = totalWidth
        #         rectangles.append((ii, i, topWidth, topHeight))
        #         ii = ii + viewportWidth
        #     i = i + viewportHeight
        # previous = None
        # part = 1
        # capturedImages = []
        # for rectangle in rectangles:
        #     if previous is not None:
        #         self.driver.execute_script(
        #             'window.scrollTo({0},{1})'.format(
        #                 rectangle[0],
        #                 rectangle[1]
        #             )
        #         )
        #         time.sleep(0.25)
        #     fileName = self.getResultStackDir(
        #         root,
        #         imgName
        #     ) + 'captured_{0}.png'.format(part)
        #     self.driver.save_screenshot(fileName)
        #     capturedImages.append(fileName)
        #     part = part + 1
        #     previous = rectangle
        # for capturedImageIdx in range(len(capturedImages) - 1):
        #     if os.path.exists(
        #         capturedImages[capturedImageIdx]
        #     ) and os.path.exists(
        #         capturedImages[capturedImageIdx + 1]
        #     ):
        #         pngData1 = open(capturedImages[capturedImageIdx], 'rb').read()
        #         pngData2 = open(capturedImages[capturedImageIdx + 1], 'rb').read()
        #         if pngData1 == pngData2:
        #             os.remove(capturedImages[capturedImageIdx + 1])
        # return True

    def getTitle(self):
        u'''Get Title
         @return Title
        '''
        invalidDirStrLst = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        return re.sub('|'.join(map(re.escape, invalidDirStrLst)), '_', self.driver.title)

    def getElementById(self, domId):
        u'''Dom Selector by Id
         @param  domId - Dom Id
         @return Dom
        '''
        return self.driver.find_element_by_id(domId)

    def getElementByXPath(self, domXpath):
        u'''Dom Selector by XPath
         @param  domXpath - Dom XPath
         @return Dom
        '''
        return self.driver.find_element_by_xpath(domXpath)

    def getElementByName(self, domName):
        u'''Dom Selector by Name
         @param  domName - Dom Name
         @return Dom [ first ]
        '''
        return self.driver.find_element_by_name(domName)

    def getElementsByName(self, domName):
        u'''Dom Selector by Name
         @param  domName - Dom Name
         @return Dom [ all ]
        '''
        return self.driver.find_elements_by_name(domName)

    def getElementsByClassName(self, domName):
        u'''Dom Selector by Class
         @param  domName - Dom Class Name
         @return Dom [ all ]
        '''
        return self.driver.find_elements_by_class_name(domName)

    def pickUpKeywords(self, targetUrl, keywords):
        u'''Pick Up Keywords
         @param keywords - URL
         @return Matched Result
        '''
        result = {
            'url': targetUrl,
            'matched': {},
            'status': False
        }
        tmpHtml = self.driver.page_source
        for keyword in keywords:
            matchedCnt = tmpHtml.count(keyword)
            if matchedCnt == 0:
                result['matched'][keyword] = 0
            else:
                result['matched'][keyword] = matchedCnt
                result['status'] = True
        return result

    def getLinksInfo(self, targetUrl, restrictKeyword):
        u'''Get Html Information [ a(link) ]
         @param targetUrl       - URL
         @param restrictKeyword - Ex-Keyword
         @return Link List
        '''
        tmpHtml = BeautifulSoup(self.driver.page_source, 'lxml')
        links = []
        linksIdx = 1
        for link in tmpHtml.find_all('a'):
            tmpUrl = link.get('href')
            try:
                if(
                    tmpUrl is not '' and
                    tmpUrl is not None and
                    tmpUrl.startswith('#') is False and
                    tmpUrl.startswith('javascript') is False
                ):
                    if tmpUrl.startswith('//'):
                        links.append('https:' + tmpUrl)
                    else:
                        if tmpUrl.startswith('/'):
                            tmpUrl = '{uri.scheme}://{uri.netloc}{filePath}'.format(
                                uri=urlparse(targetUrl),
                                filePath=tmpUrl
                            )
                        if restrictKeyword is None:
                            links.append(tmpUrl)
                        else:
                            if not tmpUrl.find(restrictKeyword) == -1:
                                links.append(tmpUrl)
                    linksIdx = linksIdx + 1
            except Exception as e:
                print('Error [handler] : {0}'.format(tmpUrl))
        return links

    def input(self, dom, value, loopFlg=False):
        u'''Action Handler For Input
         @param  dom     - Dom
         @param  value   - Input Value
         @param  loopFlg - Multi-Input Flg For Dom[s]
         @return True
        '''
        if loopFlg:
            for tmpDom in dom:
                tmpDom.send_keys(value)
        else:
            dom.send_keys(value)
        return True

    def enter(self, dom, loopFlg=False):
        u'''Action Handler For Enter
         @param  dom     - Dom
         @param  loopFlg - Multi-Input Flg For Dom[s]
         @return True
        '''
        if loopFlg:
            for tmpDom in dom:
                tmpDom.send_keys(Keys.RETURN)
        else:
            dom.send_keys(Keys.RETURN)
        return True

    def click(self, dom, loopFlg=False):
        u'''Action Handler For Click
         @param  dom     - Dom
         @param  loopFlg - Multi-Input Flg For Dom[s]
         @return True
        '''
        if loopFlg:
            for tmpDom in dom:
                tmpDom.click()
        else:
            dom.click()
        return True

    def scrollToTop(self):
        u'''Action Handler For Window Scroll
         @return void
        '''
        self.driver.execute_script('window.scrollTo(0,0)')
        time.sleep(0.25)

    def done(self):
        u'''Kill Test Browser via Driver
         @return void
        '''
        self.driver.quit()
