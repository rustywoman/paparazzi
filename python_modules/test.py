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
import colorsys
import urllib.request
from io import BytesIO
from PIL import Image


# RGB --> HEX
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def getHSV(hexrgb):
    hexrgb = hexrgb.lstrip('#')
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255.0 for i in range(0, 5, 2))
    return colorsys.rgb_to_hsv(r, g, b)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if __name__ == '__main__':
    OCTOCAT_URL = 'https://assets-cdn.github.com/images/modules/logos_page/Octocat.png'
    response = urllib.request.urlopen(OCTOCAT_URL)
    data = response.read()
    img = Image.open(BytesIO(data))
    resultRGB = []
    pixels = list(img.convert('RGB').getdata())
    for r, g, b in pixels:
       resultRGB.append(rgb2hex(r, g, b))
    resultRGB = list(set(resultRGB))
    resultRGB.sort(key=getHSV)
    print(resultRGB)