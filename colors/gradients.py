#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#            PYTHON COLORS EXERCISE          #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#         author: Piotr Ptak (poe)           #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import math
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import datetime as dt
import numpy as np

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

#~~~~~~~~~~~~~~~~~~
#black -(1)-> white
#just pass the value to each of the values r, g, b
def gradient_rgb_bw(v):
    return (v, v, v)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#green -(1)-> blue -(2)-> red (shortest path)
#the road consists of two parts:
# (1):
# ~ increase blue value
# ~ decrease green value
# (2):
# ~ incraese red value
# ~ decrease blue value
def gradient_rgb_gbr(v):
    g=0
    r=0
    b=0
    if v <= 0.5:            #(1)
        g = max(1 - v*2, 0)
        b = v*2
    elif v > 0.5:           #(2)
        r = max(v*2 - 1, 0)
        b = 2 - v*2

    return (r, g, b)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#green -(1)-> cyan -(2)-> blue -(3)-> magenta -(4)-> red
#the road consists of four parts:
# (1):
# ~ increase blue value
# (2):
# ~ decrease green value
# (3):
# ~ increase red value
# (4):
# ~ decrease blue value
def gradient_rgb_gbr_full(v):
    g=0
    r=0
    b=0
    if v <= 0.25:               #(1)
        g = 1
        b = v*4
    elif v <= 0.5:              #(2)
        b = 1
        g = max(2 - v*4, 0)
    elif v <= 0.75:             #(3)
        b = 1
        r = max(v*4 - 2, 0)
    else:                       #(4)
        r = 1
        b = max(4 - 4*v, 0)

    return (r, g, b)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#custom road from white to black (with all colors inbetween)
#white -(1)-> cyan -(2)-> blue -(3)-> magenta -(4)-> red -(5)-> yellow -(6)-> green -(7)-> black
#the road consists of seven parts. The idea is the same as in previous function (except we have more roads to complete now)
def gradient_rgb_wb_custom(v):
    g=0
    r=0
    b=0
    if v <= 1/7:                #(1)
        r = max(1 - v*7, 0)
        g = 1
        b = 1
    elif v <= 2/7:              #(2)
        r = 0
        g = max(2 - v*7, 0)
        b = 1
    elif v <= 3/7:              #(3)
        r = max(-2 + v*7, 0)
        g = 0
        b = 1
    elif v <= 4/7:              #(4)
        r = 1
        g = 0
        b = max(4 - v*7, 0)
    elif v <= 5/7:              #(5)
        r = 1
        g = max(-4 + v*7, 0)
        b = 0
    elif v <= 6/7:              #(6)
        r = max(6 - v*7, 0)
        g = 1
        b = 0
    else:                       #(7)
        r = 0
        g = max(7 - v*7, 0)
        b = 0
    return (r, g, b)

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

#~~~~~~~~~~~~~~~~~~~~~
#hsv black to white
def gradient_hsv_bw(v):
    #hue doesn't matter. I'm passing number 44 because "a imię jego czterdzieści i cztery"
    #saturation is equal to 0, so we get a color between black and white
    #value defines the lightness of the color
    return hsv2rgb(44, 0, v)

#~~~~~~~~~~~~~~~~~~~~~~
#hsv green -> blue -> red
def gradient_hsv_gbr(v):
    #this is just one function. saturation and value stay at 100% all the time
    #green is represented by hue 120', blue ~ 240', red ~ 360' (and 0' of course).
    return hsv2rgb(v*240 + 120, 1, 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~
#colors are picked from the image using photoshop color picker
#this is what I found:
#       1  ->  2   ->  3
# H   120     60       0
# S   50%    50%     50%
# V  100%   100%    100%
def gradient_hsv_unknown(v):
    #just one linear function
    return hsv2rgb(120 - v*120, 0.5, 1)

#~~~~~~~~~~~~~~~~~~~~~~~~~
#hsv custom gradient
#just create something creative
def gradient_hsv_custom(v):
    #just having fun

    #this gradient is defined by a sinusoidal function of current microseconds. an interesting effect
    return hsv2rgb(math.tan((dt.datetime.now().microsecond/2000))*360, 0.7, 0.9)

if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()
    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
