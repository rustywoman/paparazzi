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

import numpy as np
import matplotlib.pyplot as plt


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
    # IMAGE_URL = 'https://assets-cdn.github.com/images/modules/logos_page/Octocat.png'
    IMAGE_URL = 'https://raw.githubusercontent.com/nkmk/python-snippets/master/notebook/data/src/lena_square.png'
    response = urllib.request.urlopen(IMAGE_URL)
    data = response.read()
    img = Image.open(BytesIO(data))
    # Histogram
    r = np.array(img)[:, :, 0].flatten()
    g = np.array(img)[:, :, 1].flatten()
    b = np.array(img)[:, :, 2].flatten()
    bins_range = range(0, 257, 8)
    xtics_range = range(0, 257, 32)
    plt.hist(
        (r, g, b),
        bins=bins_range,
        color=['r', 'g', 'b'],
        label=['red', 'green', 'blue']
    )
    plt.legend(loc=2)
    plt.grid(True)
    [xmin, xmax, ymin, ymax] = plt.axis()
    plt.axis([0, 256, 0, ymax])
    plt.xticks(xtics_range)
    plt.savefig("___histogram.png")
    # http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.31.1421&rep=rep1&type=pdf
    # Color List
    resultRGB = []
    pixels = list(img.convert('RGB').getdata())
    for r, g, b in pixels:
       resultRGB.append(rgb2hex(r, g, b))
    resultRGB = list(set(resultRGB))
    resultRGB.sort(key=getHSV)
    # print(resultRGB)
    print('{0} colors used.'.format(len(resultRGB)))
