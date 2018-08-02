import numpy as np
import cv2
from PIL import Image
from PIL import ImageEnhance
import pylab as plt
from matplotlib.path import Path
from Helpers import CQSegmentations


#get edges with cv2's canny algorithm
img = Image.open('AntImages\head5.jpg')
image = CQSegmentations.snakesegment(img,True)