#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import Configuration Dir.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import constant
import config
import time
from PIL import Image
from handler import WebDriverWrapper as paparazzi
from handler import LoggingWrapper as log


def customConcat(parsedImages, startIdx=0, resultFileName='___result.png'):
    targetImages = parsedImages[startIdx:startIdx + 2]
    try:
        resultImg = Image.open(resultFileName)
    except Exception as e:
        resultImg = None
    if len(targetImages) is 2:
        tmpImg1 = targetImages[0]
        tmpImg2 = targetImages[1]
        dst = Image.new(
            'RGB',
            (tmpImg1['width'], tmpImg1['height'] + tmpImg2['height'])
        )
        dst.paste(tmpImg1['ins'], (0, 0))
        dst.paste(tmpImg2['ins'], (0, tmpImg1['height']))
        dst.save(resultFileName)
        customConcat(
            parsedImages=parsedImages,
            startIdx=startIdx + 2,
            resultFileName=resultFileName
        )
    else:
        tmpLastImg = targetImages[0]
        dst = Image.new(
            'RGB',
            (resultImg.width, resultImg.height + tmpLastImg['height'])
        )
        dst.paste(resultImg, (0, 0))
        dst.paste(tmpLastImg['ins'], (0, resultImg.height))
        dst.save(resultFileName)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':

    browserName = 'chrome'
    deviceType = 'pc'
    testWebDriver = paparazzi.WebDriverWrapper(
        screenshotDir=config['screenshot']['dir'],
        browser=browserName,
        device=deviceType,
        options={
            'UA': config['browserUA'][deviceType],
            'SIZE': config['browserSize'][deviceType]
        }
    )

    testWebDriver.access('http://localhost:9999/xxx.html')
    time.sleep(3)

    testWebDriver.scrollToTop()
    nextYPosition = 0
    capturedIdx = 1
    scrollFlg = True

    wholeHeight = testWebDriver.driver.execute_script(
        'return document.body.parentNode.scrollHeight'
    )
    viewportWidth = testWebDriver.driver.execute_script(
        'return window.innerWidth'
    )
    viewportHeight = testWebDriver.driver.execute_script(
        'return window.innerHeight'
    )

    print('Whole Height : {0}'.format(wholeHeight))
    print('---')
    print('Viewport Width : {0}'.format(viewportWidth))
    print('Viewport Height : {0}'.format(viewportHeight))

    overScrollBuffer = 0

    if wholeHeight <= viewportHeight:
        print('---- SPA Page ----')
    else:
        print('---- Normal Page ----')
        while scrollFlg:
            if nextYPosition > wholeHeight:
                print('---- FIN ----')
                overScrollBuffer = nextYPosition - wholeHeight
                scrollFlg = False
            else:
                nextYPosition = nextYPosition + viewportHeight
                print(nextYPosition)
                testWebDriver.driver.save_screenshot('___xxx{0}.png'.format(capturedIdx))
                capturedIdx = capturedIdx + 1
                testWebDriver.driver.execute_script(
                    'window.scrollTo(0, {0})'.format(nextYPosition)
                )
                time.sleep(0.25)

    testWebDriver.done()

    # http://pillow.readthedocs.io/en/4.0.x/handbook/concepts.html#filters
    xImg = Image.open('___xxx1.png')
    imgResizeLanczos = xImg.resize((viewportWidth, viewportHeight), Image.LANCZOS)
    imgResizeLanczos.save('___xxx1_resized.png')

    xImg = Image.open('___xxx2.png')
    imgResizeLanczos = xImg.resize((viewportWidth, viewportHeight), Image.LANCZOS)
    imgResizeLanczos.save('___xxx2_resized.png')

    xImg = Image.open('___xxx3.png')
    imgResizeLanczos = xImg.resize((viewportWidth, viewportHeight), Image.LANCZOS)
    imgResizeLanczos.save('___xxx3_resized.png')

    # Last
    xImg = Image.open('___xxx3_resized.png')
    imgCroped = xImg.crop((0, overScrollBuffer, viewportWidth, viewportHeight))
    imgCroped.save('___xxx3_croped.png')

    # ---------------------------------------
    # Test - [ Concat Images ]
    # ---------------------------------------
    images = [
        '___xxx1_resized.png',
        '___xxx2_resized.png',
        '___xxx3_croped.png'
    ]
    parsedImages = []
    for imageName in images:
        tmpImg = Image.open(imageName)
        parsedImages.append(
            {
                'src': imageName,
                'ins': tmpImg,
                'width': tmpImg.width,
                'height': tmpImg.height
            }
        )
    customConcat(
        parsedImages=parsedImages,
        startIdx=0
    )
