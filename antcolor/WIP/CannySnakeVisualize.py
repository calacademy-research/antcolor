import numpy as np
import cv2
from PIL import Image
from PIL import ImageEnhance
import pylab as plt
from matplotlib.path import Path
from Helpers import CQSegmentations

#Run to easily test and visualize an image with a segmentation algorithm
img = Image.open('AntImages\color1.jpg')
image = CQSegmentations.snakesegment(img,True)