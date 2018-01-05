import math
import png
import random

n = 7
rough = 0.5
roughness = rough * 127 / (math.pow(2, n - 2))
size = int(math.pow(2, n) + 1)
s = [[127 for j in range(size)] for i in range(size)]

def getVal(x, y):
    x = int(x) % size
    y = int(y) % size
    return s[x][y]

def setVal(x, y, val):
    x = int(x) % size
    y = int(y) % size
    if val > 255:
        val = 255
    elif val < 0:
        val = 0
    s[x][y] = val

def square(x, y, stepsize):
    avg = getVal(x - stepsize, y - stepsize) + getVal(x + stepsize, y + stepsize) + getVal(x - stepsize, stepsize + y) + getVal(x + stepsize, stepsize - y)
    setVal(x, y, int(avg/4 + roughness * (random.random() * 2 * stepsize - stepsize)))

def diamond(x, y, stepsize):
    avg = getVal(x - stepsize, y) + getVal(x, y + stepsize) + getVal(x + stepsize, y) + getVal(x, y - stepsize)
    setVal(x, y, int(avg/4 + roughness * (random.random() * 2 * stepsize - stepsize)))

def divide(i):
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

def water(val):
    if val > 127:
        return val
    else:
        return 0
# s = [[water(s[i][j]) for j in range(size)] for i in range(size)]

f = open('png.png', 'wb')
w = png.Writer(len(s[0]), len(s), greyscale=True)
w.write(f, s)
f.close()
for x in range(size):
    for y in range(size):
        print('[' + str(x) + ',' + str(y) + ',' + str(s[x][y] - 127) + ']')


# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].

#!/usr/bin/env python
import pyqtgraph as pg
import numpy as np

coord_list = []
for x in range(size):
    for y in range(size):
        coord_list.append((x * 10, y * 10, s[x][y]))

pg.mkQApp()
import pyqtgraph.opengl as gl
view = gl.GLViewWidget()
view.show()

zgrid = gl.GLGridItem()
surfacemap = gl.GLSurfacePlotItem(shader='shaded')
surfacemap.setData(z=np.array(s))
surfacemap.scale(10, 10, 1)
view.addItem(zgrid)

water2 = gl.GLSurfacePlotItem(shader='shaded')
waterdata = np.zeros((size, size))
for x in range(size):
    for y in range(size):
        waterdata[x, y] = 127
water2.setData(z=waterdata)
water2.scale(10, 10, 1)
water2.setColor(np.array([0.2, 0.2, 0.8, 0.1]))
view.addItem(water2)


# water = gl.GLGridItem(color=np.array([0, 0, 1, 0]))
# water.translate(size * 10 /2, size* 10 /2, 127)
# water.scale(size/2, size/2, 1)
# water.setSpacing(x=0.01, y=0.01)
# view.addItem(water)

zgrid.scale(0.2, 0.2, 0.2)

coords = np.array(coord_list)
colors = (1, 1, 1, 1)
# plt = gl.GLScatterPlotItem(pos=coords, color = colors, size=5, pxMode=True)
# view.addItem(plt)
view.addItem(surfacemap)
