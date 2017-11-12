#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Class
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class WebDriverWrapper(object):
    def __init__(self, screenshotDir):
        CHROME_DRIVER = '/chromedriver.exe'
        DRIVER_DIR = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            ) + os.path.sep + 'driver'
        )
        self.name = 'WebDriverWrapper'
        self.screenshotDir = screenshotDir
        self.driver = webdriver.Chrome(
            executable_path=DRIVER_DIR + CHROME_DRIVER
        )


    def maximumWindow(self):
        self.driver.maximize_window()


    def access(self, url):
        self.driver.get(url)
        self.wait(2)


    def wait(self, interval=5):
        time.sleep(interval)
        return True


    def getCurrentDir(self):
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                os.pardir
            )
        )


    def makeResultStackDir(self, root, name):
        os.makedirs(os.path.sep.join([self.getCurrentDir(), root, name]))
        return True


    def getResultStackDir(self, root, name):
        tmpStackDir = os.path.sep.join([self.getCurrentDir(), root, name])
        if not os.path.exists(tmpStackDir):
            self.makeResultStackDir(root, name)
        return tmpStackDir + os.path.sep


    def takeFullScreenshot(self, testDir, imgName):
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
            if not previous is None:
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


    def getElementById(self, domId):
        return self.driver.find_element_by_id(domId)


    def getElementByXPath(self, domXpath):
        return self.driver.find_element_by_xpath(domXpath)


    def getElementByName(self, domName):
        return self.driver.find_element_by_name(domName)


    def getElementsByName(self, domName):
        return self.driver.find_elements_by_name(domName)


    def getElementsByClassName(self, domName):
        return self.driver.find_elements_by_class_name(domName)


    def input(self, dom, value, loopFlg=False):
        if loopFlg:
            for tmpDom in dom:
                tmpDom.send_keys(value)
        else:
            dom.send_keys(value)
        return True


    def enter(self, dom, loopFlg=False):
        if loopFlg:
            for tmpDom in dom:
                tmpDom.send_keys(Keys.RETURN)
        else:
            dom.send_keys(Keys.RETURN)
        return True


    def click(self, dom, loopFlg=False):
        if loopFlg:
            for tmpDom in dom:
                tmpDom.click()
        else:
            dom.click()
        return True


    def scrollToTop(self):
        self.driver.execute_script('window.scrollTo(0,0)')
        time.sleep(0.25)


    def done(self):
        self.driver.quit()
