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
    testName = 'XXX'
    imgName = 'ZZZ'
    testWebDriver.access('http://localhost:9999/xxx.html')
    time.sleep(3)
    testWebDriver.scrollToTop()
    testWebDriver.takeFullScreenshot(
        testDir=testName,
        imgName=imgName
    )
    # nextYPosition = 0
    # capturedIdx = 1
    # scrollFlg = True
    # wholeHeight = testWebDriver.driver.execute_script(
    #     'return document.body.parentNode.scrollHeight'
    # )
    # viewportWidth = testWebDriver.driver.execute_script(
    #     'return window.innerWidth'
    # )
    # viewportHeight = testWebDriver.driver.execute_script(
    #     'return window.innerHeight'
    # )
    # print('Whole Height : {0}'.format(wholeHeight))
    # print('---')
    # print('Viewport Width : {0}'.format(viewportWidth))
    # print('Viewport Height : {0}'.format(viewportHeight))
    # overScrollBuffer = 0
    # if wholeHeight <= viewportHeight:
    #     print('---- SPA Page ----')
    #     testWebDriver.driver.save_screenshot('___result.png')
    #     tmpImg = Image.open('___result.png').resize((viewportWidth, viewportHeight), Image.LANCZOS)
    #     tmpImg.save('___result.png')
    # else:
    #     print('---- Normal Page ----')
    #     while scrollFlg:
    #         if nextYPosition > wholeHeight:
    #             print('---- FIN ----')
    #             overScrollBuffer = nextYPosition - wholeHeight
    #             scrollFlg = False
    #         else:
    #             nextYPosition = nextYPosition + viewportHeight
    #             testWebDriver.driver.save_screenshot('___tmp_captured_{0}.png'.format(capturedIdx))
    #             capturedIdx = capturedIdx + 1
    #             testWebDriver.driver.execute_script(
    #                 'window.scrollTo(0, {0})'.format(nextYPosition)
    #             )
    #             time.sleep(0.25)
    # testWebDriver.done()
    # print('Overscroll Buffer : {0}'.format(overScrollBuffer))

    # ##############

    # # Collect Caches
    # tmpCacheImgs = []
    # tmpCacheImgFiles = os.listdir('.')
    # for tmpCachImgFile in tmpCacheImgFiles:
    #     if tmpCachImgFile.find('___tmp') is not -1:
    #         tmpCacheImgs.append(tmpCachImgFile)
    # tmpCacheImgs.sort()

    # # Resize
    # parsedImages = []
    # resizeLoopLimit = len(tmpCacheImgs)
    # resizeLoopIdx = 0
    # for tmpCacheImg in tmpCacheImgs:
    #     # http://pillow.readthedocs.io/en/4.0.x/handbook/concepts.html#filters
    #     tmpImg = Image.open(tmpCacheImg).resize((viewportWidth, viewportHeight), Image.LANCZOS)
    #     resizeLoopIdx = resizeLoopIdx + 1
    #     if resizeLoopIdx is resizeLoopLimit:
    #         tmpImg = tmpImg.crop((0, overScrollBuffer, viewportWidth, viewportHeight))
    #         parsedImages.append(
    #             {
    #                 'src': tmpCacheImg,
    #                 'ins': tmpImg,
    #                 'width': viewportWidth,
    #                 'height': viewportHeight - overScrollBuffer
    #             }
    #         )
    #     else:
    #         parsedImages.append(
    #             {
    #                 'src': tmpCacheImg,
    #                 'ins': tmpImg,
    #                 'width': viewportWidth,
    #                 'height': viewportHeight
    #             }
    #         )
    #     # Byte化した一時画像を削除
    #     os.remove(tmpCacheImg)

    # # Concat
    # if len(parsedImages) > 0:
    #     customConcat(
    #         parsedImages=parsedImages,
    #         startIdx=0
    #     )

