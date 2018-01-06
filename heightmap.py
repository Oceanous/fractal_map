#!/usr/bin/env python
import math
import png
import random
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from scipy import ndimage as nd
n = 7
rough = 0.4
roughness = rough * 127 / (math.pow(2, n - 2))
smooth = 0.7
size = int(math.pow(2, n) + 1)
s = [[127 for j in range(size)] for i in range(size)]

def getVal(x, y):
    # Get height values, wrapping around edges
    x = int(x) % size
    y = int(y) % size
    return s[x][y]

def setVal(x, y, val):
    # Set height values, wrapping around edges and clipping at 0 and 255
    x = int(x) % size
    y = int(y) % size
    if val > 255:
        val = 255
    elif val < 0:
        val = 0
    s[x][y] = val

def square(x, y, stepsize):
    # Average the values of 4 corners of a square, add some randomness, and set the center value
    avg = getVal(x - stepsize, y - stepsize) + getVal(x + stepsize, y + stepsize) + getVal(x - stepsize, stepsize + y) + getVal(x + stepsize, stepsize - y)
    setVal(x, y, int(avg/4.0 + roughness * (np.random.normal() * 2 * stepsize)))

def diamond(x, y, stepsize):
    # Average the values of 4 corners of a diamond, add some randomness, and set the center value
    avg = getVal(x - stepsize, y) + getVal(x, y + stepsize) + getVal(x + stepsize, y) + getVal(x, y - stepsize)
    setVal(x, y, int(avg/4.0 + roughness * (np.random.normal() * 2 * stepsize)))

def divide(i):
    # Square and diamond recursively until done
    half = int(i / 2)
    if half == 0:
        return
    for y in range(half, size - 1, i):
        for x in range(half, size - 1, i):
            square(x, y, half)
    for y in range(0, size - 1, half):
        for x in range((y + half) % i, size - 1, i):
            diamond(x, y, half)
    divide(int(i / 2))

divide(size - 1)

s = nd.gaussian_filter(s, sigma=smooth)

f = open('png.png', 'wb')
w = png.Writer(len(s[0]), len(s), greyscale=True)
w.write(f, s)
f.close()
# for x in range(size):
#     for y in range(size):
#         print('[' + str(x) + ',' + str(y) + ',' + str(s[x][y] - 127) + ']')

pg.mkQApp()
view = gl.GLViewWidget()
view.setCameraPosition(distance=1500)
view.show()

zgrid = gl.GLGridItem()
surfacemap = gl.GLSurfacePlotItem(shader='shaded')
surfacemap.setData(z=np.array(s))
surfacemap.translate(-size*5, -size*5, 0)
surfacemap.scale(10, 10, 1)
view.addItem(zgrid)

water = gl.GLSurfacePlotItem(shader='shaded')
waterdata = np.zeros((size, size))
for x in range(size):
    for y in range(size):
        waterdata[x, y] = 127
water.setData(z=waterdata)
water.scale(10, 10, 1)
water.translate(-size*5, -size*5, 0)
water.setColor(np.array([0.2, 0.2, 0.8, 0.1]))
view.addItem(water)

zgrid.scale(0.2, 0.2, 0.2)
view.addItem(surfacemap)
