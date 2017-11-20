from skimage import data
import skimage.io
from skimage.morphology import disk
from skimage.filters.rank import median
from skimage.filters import gaussian
from matplotlib import pyplot as plt
import numpy as np


image = data.load("/Users/poe/Code/human-computer-interaction/airplanes/tmp.jpg")
grayScaleImage = data.load("/Users/poe/Code/human-computer-interaction/airplanes/tmp.jpg", 1)
#med = median(grayScaleImage, disk(12))
gaus = gaussian(image, sigma=3, mode='reflect', multichannel=True)
plt.imshow(gaus)
plt.show()
