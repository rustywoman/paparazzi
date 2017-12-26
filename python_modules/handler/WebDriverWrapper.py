#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.parse import urlparse


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WebDriverWrapper(object):
    u'''Handler Class For Web Driver [ chrome ]
    '''
    def __init__(self, screenshotDir, browser):
        u'''Constructor
         @param  screenshotDir - Directory Name
         @param  browser       - Directory Name
        '''
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
        elif browser == 'firefox':
            # -------------------
            # Firefox
            # -------------------
            self.driver = webdriver.Firefox(
                executable_path=DRIVER_DIR + GECHO_DRIVER,
                log_path=os.devnull
            )
        else :
            # -------------------
            # Chrome
            # -------------------
            self.driver = webdriver.Chrome(
                executable_path=DRIVER_DIR + CHROME_DRIVER
            )

    def maximumWindow(self):
        u'''Maximum Browser Window Size
         @return void
        '''
        self.driver.maximize_window()

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
        return True

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

    def takeFullScreenshot(self, testDir, imgName):
        u'''Take Screenshots
         @param  testDir - Test Case Directory
         @param  name - Test Case Name
         @return True
        '''
        root = self.screenshotDir + os.path.sep + testDir
        totalWidth = self.driver.execute_script(
            'return window.innerWidth'
        )
        totalHeight = self.driver.execute_script(
            'return document.body.parentNode.scrollHeight'
        )
        viewportWidth = self.driver.execute_script(
            'return document.body.clientWidth'
        )
        viewportHeight = self.driver.execute_script(
            'return window.innerHeight'
        )
        rectangles = []
        i = 0
        while i < totalHeight:
            ii = 0
            topHeight = i + viewportHeight
            if topHeight > totalHeight:
                topHeight = totalHeight
            while ii < totalWidth:
                topWidth = ii + viewportWidth
                if topWidth > totalWidth:
                    topWidth = totalWidth
                rectangles.append((ii, i, topWidth, topHeight))
                ii = ii + viewportWidth
            i = i + viewportHeight
        previous = None
        part = 1
        capturedImages = []
        for rectangle in rectangles:
            if previous is not None:
                self.driver.execute_script(
                    'window.scrollTo({0},{1})'.format(
                        rectangle[0],
                        rectangle[1]
                    )
                )
                time.sleep(0.25)
            fileName = self.getResultStackDir(
                root,
                imgName
            ) + 'part_{0}.png'.format(part)
            self.driver.save_screenshot(fileName)
            capturedImages.append(fileName)
            part = part + 1
            previous = rectangle
        for capturedImageIdx in range(len(capturedImages) - 1):
            if os.path.exists(
                capturedImages[capturedImageIdx]
            ) and os.path.exists(
                capturedImages[capturedImageIdx + 1]
            ):
                pngData1 = open(capturedImages[capturedImageIdx], 'rb').read()
                pngData2 = open(capturedImages[capturedImageIdx + 1], 'rb').read()
                if pngData1 == pngData2:
                    os.remove(capturedImages[capturedImageIdx + 1])
        return True

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
