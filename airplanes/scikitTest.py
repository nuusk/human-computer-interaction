from skimage import data
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



#root directory of the project
projectDirectory = os.getcwd()
#"/Users/poe/Code/human-computer-interaction/airplanes/"

#get the images and store them in an array
def collectImages(baseName, lastNumber):
    images = []
    for i in range(0, lastNumber):
        if (i<10):
            images.append(cv2.imread(projectDirectory + "/img/" + baseName + "0" + str(i) + ".jpg"))
        else:
            images.append(cv2.imread(projectDirectory + "/img/" + baseName+ str(i) + ".jpg"))
    return images

#function for finding optimal value of paramaters for bilateral filter
def tryBilateral(image, numberOfIterations, jump):
    fig = plt.figure()
    for i in range(0, numberOfIterations, jump):
        plt.imshow(cv2.bilateralFilter(image, 9, i, i))
        fig.savefig(str(i) + ".pdf")

#function for finding optimal value of paramaters for canny edge detector
def tryCanny(image, numberOfIterations, jump):
    fig = plt.figure()
    for i in range(0, numberOfIterations, jump):
        plt.imshow(cv2.Canny(image, i, i))
        fig.savefig(str(i) + ".pdf")

#function for finding optimal value of paramaters for erosion
def tryErode(image, numberOfIterations, jump):
    fig = plt.figure()
    kernel = np.ones((4, 4), np.uint8)
    for i in range(0, numberOfIterations, jump):
        plt.imshow(cv2.erode(image, kernel, iterations=i))
        fig.savefig(str(i) + ".pdf")

#function for finding optimal value of paramaters for bilateral dilatation
def tryDilate(image, numberOfIterations, jump):
    fig = plt.figure()
    kernel = np.ones((4, 4), np.uint8)
    for i in range(0, numberOfIterations, jump):
        plt.imshow(cv2.dilate(image, kernel, iterations=i))
        fig.savefig(str(i) + ".pdf")

def main():
    airplanes = []
    airplanes = collectImages("samolot", 20)
    tmpMedian = median(airplanes[0], disk(5))
    print(tmpMedian)

    #first I apply bilateral filter to smooth the texture and retain sharp edges
    #tryBilateral(airplanes[0], 200, 25)        #found good parameter -> 170
    airplanes[0] = cv2.bilateralFilter(airplanes[0], 9, 170, 170)

    #canny algorithm is used to detect edges on the images
    #tryCanny(airplanes[0], 200, 25)            #found good parameter -> 100
    airplanes[0] = cv2.Canny(airplanes[0], 100, 100)

    #kernel = np.ones((4, 4), np.uint8)

    #tryErode(airplanes[0], 7, 1)

    #tryDilate(airplanes[0], 7, 1)

    #fig = plt.figure()

    #plt.imshow(cv2.erode(airplanes[0], kernel, iterations=0))
    #fig.savefig("0.pdf")
    #plt.show()





main()
