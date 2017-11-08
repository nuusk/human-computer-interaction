#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gradients as grd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

#drawing map using an array of colors. each point has r,g,b values
def drawMap(_colorMap, fileName):
    fig = plt.figure()
    plt.imshow(_colorMap)
    plt.show()
    fig.savefig(fileName + ".pdf")

#analyzing the data given as an input to the program.
#first row defines height, width of the map and also a distance between two points on the map (in centimeters)
#after we save those values, we can safely delete them, because all the other values will be used to draw the map
def loadCoordinates(fileName):
    with open(fileName) as file:
        _map = file.read().splitlines()
    _map = [i.split(' ') for i in _map]
    _height = int(_map[0][0])
    _width = int(_map[0][1])
    _distance = int(_map[0][2])
    del _map[0]
    return _map, _height, _width, _distance


#given the height of each point on the map, create a color array which represents color of each individual point
def colorMap(mapData, colorData, PEAK, PIT):
    for i in range (0, len(mapData)):
        for j in range(0, len(mapData[i])):
            try:
                colorData[i][j] = grd.gradient_rgb_bw((float(mapData[i][j])-PIT)/(PEAK-PIT))
            except Exception as exc:
                print(exc)
                exit()

    return colorData

#use this function to get the highest(peak) and the lowest(pit) point on the map
#the highest point will determine 100% value of gradient that is used to color the map
#the lowest point will determine the 0% value of the gradient that is used to color the map
#use it after you loaded coordinates (which is where we get rid of height, width and distance)
def getExtremes(mapData):
    currentPeak = 0
    currentPit = float(mapData[0][0])
    for row in mapData:
        for columnElement in row:
            if float(columnElement) > currentPeak:
                currentPeak = float(columnElement)
            if float(columnElement) < currentPit:
                currentPit = float(columnElement)

    return currentPeak, currentPit


if __name__ == '__main__':
    _map, _height, _width, _distance = loadCoordinates("mapData.dem")
    PEAK, PIT = getExtremes(_map)
    _color = np.zeros((_height, _width, 3), dtype=np.float32)
    _color = colorMap(_map, _color, PEAK, PIT)
    drawMap(_color, "map")
    plt.close()
