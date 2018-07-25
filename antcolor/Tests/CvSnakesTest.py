import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage import data
from skimage.filters import gaussian
from skimage.segmentation import active_contour
import cv2
from matplotlib import path
from skimage import img_as_float
from PIL import Image
from PIL import ImageEnhance

img = Image.open('AntImages\head9.jpg')
contrasted = ImageEnhance.Contrast(img).enhance(2)
contrastedarr = np.array(contrasted)
greyscaled = cv2.cvtColor(contrastedarr, cv2.COLOR_BGR2GRAY)
filtered = cv2.bilateralFilter(greyscaled, 6, 50, 50)
edged = cv2.Canny(filtered, 100, 200) #100, 225 #125, 250

img = img_as_float(edged)
#cv2.imshow('c', data.astronaut())
#cv2.waitKey()
forsnake = img

height = forsnake.shape[0]
width = forsnake.shape[1]
sdiameter = height * 0.6

s = np.linspace(0, 2*np.pi, sdiameter)
x = width / 2 + sdiameter*np.cos(s)
y = height / 2 - (height / 20) + sdiameter*np.sin(s) * (height / width)
init = np.array([x, y]).T

#s = np.linspace(0, 2*np.pi, 50)
#x = (img.shape[1] / 2) + 50*np.cos(s)
#y = (img.shape[0] / 2) - 10 + 50*np.sin(s)
#init = np.array([x, y]).T
finished = False

while(not finished):
    snake = active_contour(img, init, alpha=0.15, beta=1, gamma=0.05, w_line=0.1, w_edge=1) #0.005
    print(snake)
    if(len(snake) > 0):
        finished = True

fig, ax = plt.subplots(figsize=(7, 7))
ax.imshow(forsnake, cmap=plt.cm.gray)
ax.plot(init[:, 0], init[:, 1], '--r', lw=3)
ax.plot(snake[:, 0], snake[:, 1], '-b', lw=3)
ax.set_xticks([]), ax.set_yticks([])
ax.axis([0, img.shape[1], img.shape[0], 0])
plt.show()