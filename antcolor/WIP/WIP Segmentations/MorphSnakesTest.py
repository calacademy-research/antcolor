from itertools import cycle

import cv2
import numpy as np
from Tests import morphsnakes
from scipy import ndimage
from scipy.ndimage import binary_dilation, binary_erosion, \
                        gaussian_filter, gaussian_gradient_magnitude
from scipy.misc import imread
from matplotlib import pyplot as ppl
from Tests import tests

#WIP implementation of morphsnakes

def rgb2gray(img):
    """Convert a RGB image to gray scale."""
    return 0.2989*img[:,:,0] + 0.587*img[:,:,1] + 0.114*img[:,:,2]

def circle_levelset(shape, center, sqradius, scalerow=1.0):
    """Build a binary function with a circle as the 0.5-levelset."""
    grid = np.mgrid[list(map(slice, shape))].T - center
    phi = sqradius - np.sqrt(np.sum((grid.T)**2, 0))
    u = np.float_(phi > 0)
    return u

# Load the image.
imgcolor = imread("AntImages/highhead1.jpg") / 255.0
img = rgb2gray(imgcolor)

# g(I)
gI = morphsnakes.gborders(img, alpha=1000, sigma=2)

# Morphological GAC. Initialization of the level-set.
mgac = morphsnakes.MorphGAC(gI, smoothing=2, threshold=0.3, balloon=-1)
mgac.levelset = circle_levelset(img.shape, (163, 137), 135, scalerow=0.75)

# Visual evolution.
ppl.figure()
morphsnakes.evolve_visual(mgac, num_iters=110, background=imgcolor)

ppl.show()

