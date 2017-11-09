#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#             PYTHON MAP EXERCISE            #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#         author: Piotr Ptak (poe)           #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #

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
def drawMap(colorMap, fileName):
    fig = plt.figure()
    plt.imshow(colorMap)
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
                colorData[i][j] = grd.gradient_hsv_physical_map((float(mapData[i][j])-PIT)/(PEAK-PIT))
            except Exception as exc:
                print(exc)
                exit()

    return colorData

#add light value to the pixel, but keep it between 0 and 1
def applyLight(pixel, light):
    pixel += light
    pixel[0] = max(0, min(pixel[0], 1))
    pixel[1] = max(0, min(pixel[1], 1))
    pixel[2] = max(0, min(pixel[2], 1))

    return pixel

#change the value of a pixel depending of a value of a pixel next to it
def primitiveLight(colorMap, mapData):
    #lightValue will be added to the higher pixel, and reduced from lower pixel
    lightValue = 0.12
    for i in range (1, len(mapData)):
        for j in range(1, len(mapData[i])):
            try:
                if float(mapData[i][j-1]) < float(mapData[i][j]):
                    colorMap[i][j] = applyLight(colorMap[i][j], lightValue)
                else:
                    colorMap[i][j] = applyLight(colorMap[i][j], -lightValue)
            except Exception as exc:
                print(exc)
                exit()
    return colorMap

def sunLight(mapData, colorMap, height, width, realDistance, PEAK, PIT, sunY, sunX, sunHeight):
    #first let's set our sun position
    sunPosition = np.array([sunY, sunX, sunHeight])

    realDistance /= 1000

    #we're searching for the angle between the sun and the surface. let's create the data structure that will store this information
    #there will be a specific value for every pixel which will represent the angle between this point and the sun
    sunToSurfaceAngle = np.zeros([height,width])
    for i in range(0, height):
        for j in range(0, width):
            #a surface normal can be calculated using cross product of two edges of triangles created by specific points on the surface
            #each triangle consists of three points: p1, p2, p3
            #p1 is always the starting point of the iteration
            #each point is represented by x, y and z
            #mapData[i][j] corresponds to the hight of the points on the map
            p1 = np.array([i*realDistance, j*realDistance, mapData[i][j]])                  #upper left corner when i%2, bottom right otherwise

            #now to cover the surface with triangles
            if i % 2 == 0:
                p3 = np.array([(i+1)*realDistance, j*realDistance, mapData[i+1][j]])        #bottom left corner
                if j < width-1:
                    p2 = np.array([i*realDistance, realDistance*(j+1), mapData[i][j+1]])    #upper right corner
                else:
                    p2 = np.array([i*realDistance, realDistance*(j-1),  mapData[i][j-1]])   #when we hit the border, we can just use the previous pixel (which is the upper left corner from the PREVIOUS iteration)
            else:
                p3 = np.array([(i-1)*realDistance,j*realDistance, mapData[i-1][j]])         #upper left right
                if j > 0:
                    p2 = np.array([i*realDistance,(j-1)*realDistance, mapData[i][j-1]])     #bottom left corner
                else:
                    p2 = np.array([i*realDistance, (j+1)*realDistance, mapData[i][j+1]])    #when j==0, we just use the next pixel (which is the bottom right pixel of the next iteration)

            p1 = p1.astype(float)
            p3 = p3.astype(float)
            p2 = p2.astype(float)

            #calculate vector between our starting point and the sun
            vectorToSun = sunPosition - p1

            #calculate normal
            U = p2 - p1
            V = p3 - p1
            normal = np.array([U[1]*V[2] - U[2]*V[1], U[2]*V[0] - U[0]*V[2], U[0]*V[1] - U[1]*V[0]])

            #calculate the angle between the normal and sun vector
            sunToSurfaceAngle[i][j] = math.degrees(np.arccos(np.dot(normal,vectorToSun)/(np.linalg.norm(normal)*np.linalg.norm(vectorToSun))))

    #now the actual shadowing (and lighting)
    for i in range(0, height):
        for j in range(0, width):
            #print(sunToSurfaceAngle[i][j], ' -> ', math.sin(math.radians(sunToSurfaceAngle[i][j])))
            colorMap[i][j][1] = max(0, math.sin(math.radians(sunToSurfaceAngle[i][j])))
            colorMap[i][j][2] = max(0, math.sin(math.radians(sunToSurfaceAngle[i][j])))
    return colorMap


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

    #create empty color matrix
    _color = np.zeros((_height, _width, 3), dtype=np.float32)

    #assign colors to the matrix according to the data given
    _color = colorMap(_map, _color, PEAK, PIT)

    #primitive lightning algorithm
    #_color = primitiveLight(_color, _map)

    #normal-vector lightning algorithm
    _color = sunLight(_map, _color, _height, _width, _distance, PEAK, PIT, -_distance, -_distance, 1)

    #convert hsv to rgb to be able to display it
    for i in range (0, len(_color)):
        for j in range(0, len(_color[i])):
            _color[i][j] = grd.hsv2rgb(_color[i][j][0], _color[i][j][1], _color[i][j][2])

    #draw the result
    drawMap(_color, "map")
    plt.close()
