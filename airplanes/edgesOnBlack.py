from skimage import filters,data,color,measure,exposure
import skimage.io
from skimage.morphology import disk
from skimage.filters.rank import median
from skimage.filters import gaussian
from skimage.filters import sobel
from skimage.feature import canny
from matplotlib import pyplot as plt
import numpy as np
import cv2
import os
from random import choice as rcg

#root directory of the project
projectDirectory = os.getcwd()
#"/Users/poe/Code/human-computer-interaction/airplanes/"

#cool selection of colors ( ͡° ͜ʖ ͡°)
myColors = ["#e25724", "#ffd149", "#ffff49", "#a4ff49", "#59bf3d", "#33cea2", "#40cce5", "#37a0fc", "#4655d6", "#825ff4", "#e539bd", "#fc1964"]

#parameters used for filtering and contour finding
qthPercentile = 12
contourLevelValue = 0.3
contourWidth = 1.4
airplanes = []
contours = []

#get the images and store them in an array
def collectImages(baseName, lastNumber):
    images = []
    for i in range(0, lastNumber):
        if (i<10):
            images.append(cv2.imread(projectDirectory + "/img/" + baseName + "0" + str(i) + ".jpg"))
        else:
            images.append(cv2.imread(projectDirectory + "/img/" + baseName+ str(i) + ".jpg"))
    return images



def drawPictureWithContour(image, x):
    #fig = plt.figure()
    
    #rescale exposure
    min = np.percentile(image, 5)
    perc = np.percentile(image, qthPercentile)
    resc = exposure.rescale_intensity(image,in_range=(min, perc))

    #kernel is used for dilatation and erosion
    kernel = np.ones((5,5),np.uint8)

    #we will be changing the outcome depending on the image value, hence the hsv format
    img = color.rgb2hsv(resc)
    height, width, channels = img.shape
    #print("width: " + str(width))
    #print("height: " + str(height))
    #print("channels: " + str(channels))

    #create 'inverse' array
    inv = np.zeros([height, width])
    for i in range(height):
        for j in range(width):
            #sky is a lot brighter than planes. inverse array will contain the data used for edge finding
            inv[i][j] = 1 - img[i][j][2]

    #time to smooth the results
    #inv = gaussian(inv, sigma=0.8)

    #erosion and dilatation to patch up objects on the sky
    inv = cv2.erode(inv,kernel,iterations = 1)
    inv = cv2.dilate(inv,kernel,iterations = 3)
    inv = cv2.erode(inv,kernel,iterations = 1)

    #actual contour finding
    contours = measure.find_contours(inv, contourLevelValue)
    for n, contours in enumerate(contours):
        M = cv2.moments(c)
        centerX = int(M["m10"] / M["m00"])
        centerY = int(M["m01"] / M["m00"])
        plt.plot(contours[:,1],contours[:,0],linewidth=contourWidth, color=rcg(myColors))



    ''' ~~~ displaying image with matplotlib
    opencv represents rgb images as nd-array, but in reverse order (they are bgr instead of rgb)
    we have to convert them back to rgb using COLOR_BGR2RGB function
    '''
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #plt.imshow(inv)
    #plt.show()
    fig.savefig(str(x) + ".pdf")

def main():
    airplanes = collectImages("samolot", 20)

    for i in range(0, 5):
        drawPictureWithContour(airplanes[i], i)

main()
