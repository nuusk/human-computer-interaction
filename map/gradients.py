#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#           PYTHON GRADIENT MODULE           #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#         author: Piotr Ptak (poe)           #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #

#!/usr/bin/env python
# -*- coding: utf-8 -*-

def hsv2rgb(h, s, v):
    #we want h to be 0<=h<=360
    while h > 360:
        h -= 360
    while h < 0:
        h += 360
    hue = h/60
    c = v * s
    x = c * (1 - abs((hue % 2) -1))
    m = v - c

    #r, g, b is assigned according to the part of the circle H is in
    if h < 60:
        rTmp = c
        gTmp = x
        bTmp = 0
    elif h < 120:
        rTmp = x
        gTmp = c
        bTmp = 0
    elif h < 180:
        rTmp = 0
        gTmp = c
        bTmp = x
    elif h < 240:
        rTmp = 0
        gTmp = x
        bTmp = c
    elif h < 300:
        rTmp = x
        gTmp = 0
        bTmp = c
    else:
        rTmp = c
        gTmp = 0
        bTmp = x

    r = (rTmp + m)
    g = (gTmp + m)
    b = (bTmp + m)

    return (r, g, b)

def gradient_hsv_physical_map(v):
    #just one linear function
    return (120 - v*120, 1, 0.7)
