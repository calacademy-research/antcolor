from PIL import Image
from PIL import ImageEnhance
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Helpers import SnakeMain
from matplotlib.path import Path
from skimage.segmentation import active_contour
from skimage import img_as_float

####################
#### ColorQuantifierSegmentations includes defs for segmenting ants from images
################

def scisnakesegment(image,visualizebool): #function to segment using the faster and more reliable SKIMAGE snake (active contour) algorithm after applying the canny algorithm to find edges

    #get edges with cv2's canny algorithm
    img = image
    imgarr = np.array(img)
    if(visualizebool):
        imgvis = imgarr[:, :, ::-1].copy()  # convert from RGB to BGR
        cv2.imshow('Input Image',imgvis)
        cv2.waitKey()
    contrasted = ImageEnhance.Contrast(img).enhance(2)
    contrastedarr = np.array(contrasted)
    contrastedarr = contrastedarr[:, :, ::-1].copy()  # convert from RGB to BGR
    if(visualizebool):
        cv2.imshow('Contrasted Image', contrastedarr)
        cv2.waitKey()
    greyscaled = cv2.cvtColor(contrastedarr, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(greyscaled, 6, 50, 50)
    if (visualizebool):
        cv2.imshow('Bilaterally Filtered Image', contrastedarr)
        cv2.waitKey()
    edged = cv2.Canny(filtered, 125, 250) #100, 225
    if(visualizebool):
        cv2.imshow('Image Edges with Canny', edged)
        cv2.waitKey()

    forsnake = img_as_float(edged)

    # apply the snake algorithm from the skimage package
    height = forsnake.shape[0]
    width = forsnake.shape[1]
    sdiameter = height * 0.6

    s = np.linspace(0, 2 * np.pi, sdiameter)
    x = width / 2 + sdiameter * np.cos(s)
    y = height / 2 - (height / 20) + sdiameter * np.sin(s) * (height / width)
    init = np.array([x, y]).T
    snake = active_contour(img, init, alpha=0.15, beta=1, gamma=0.05, w_line=0.1, w_edge=1) #a = 0.15 g=0.05 #The actual skimage function
    #snake = active_contour(forsnake, init, alpha=0.1, beta=5, gamma=0.004, w_line=0.1, w_edge=1, convergence=1)
    contours = np.asarray(snake)

    width = img.width
    height = img.height

    #visualize contour points
    if(visualizebool):
        x, y = contours.T
        plt.scatter(x, y)
        plt.ylim(0, height)
        plt.xlim(0, width)
        plt.show()

    #get polygon mask from contour points
    poly_path = Path(contours)
    y, x = np.mgrid[:height, :width]
    coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))
    mask = poly_path.contains_points(coors)
    plt.imshow(mask.reshape(height, width))
    mask = mask.reshape(height, width)
    if(visualizebool):
        plt.ylim(0, img.height)
        plt.xlim(0, img.width)
        plt.show()
    mask = np.array(mask, dtype=np.uint8)
    #apply mask
    final = cv2.bitwise_and(imgarr, imgarr, mask=mask)
    finalvis = final[:, :, ::-1].copy()  # convert from RGB to BGR
    if(visualizebool):
        cv2.imshow('Image with Mask', finalvis)
        cv2.waitKey()
    return final

def snakesegment(image,visualizebool): #function to segment using the included snake (active contour) algorithm after applying the canny algorithm to find edges

    #get edges with cv2's canny algorithm
    img = image
    imgarr = np.array(img)
    if(visualizebool):
        imgvis = imgarr[:, :, ::-1].copy()  # convert from RGB to BGR
        cv2.imshow('Input Image',imgvis)
        cv2.waitKey()
    contrasted = ImageEnhance.Contrast(img).enhance(2)
    contrastedarr = np.array(contrasted)
    contrastedarr = contrastedarr[:, :, ::-1].copy()  # convert from RGB to BGR
    if(visualizebool):
        cv2.imshow('Contrasted Image', contrastedarr)
        cv2.waitKey()
    greyscaled = cv2.cvtColor(contrastedarr, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(greyscaled, 6, 50, 50)
    if (visualizebool):
        cv2.imshow('Bilaterally Filtered Image', contrastedarr)
        cv2.waitKey()
    edged = cv2.Canny(filtered, 125, 250) #100, 225
    if(visualizebool):
        cv2.imshow('Image Edges with Canny', edged)
        cv2.waitKey()

    #apply included snake algorithm
    snakecharmer = SnakeMain.SnakeMain()
    snakecharmer.load_image(file_to_load=edged,visualizebool=visualizebool)

    # while specified number of iterations not completed...
    while(snakecharmer.progress < 10):
        pass

    #get contour points from the finished snake
    contours = snakecharmer.points
    contours = np.asarray(contours)

    width = img.width
    height = img.height

    #visualize contour points
    if(visualizebool):
        x, y = contours.T
        plt.scatter(x, y)
        plt.ylim(0, height)
        plt.xlim(0, width)
        plt.show()

    #get polygon mask from contour points
    poly_path = Path(contours)
    y, x = np.mgrid[:height, :width]
    coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))
    mask = poly_path.contains_points(coors)
    plt.imshow(mask.reshape(height, width))
    mask = mask.reshape(height, width)
    if(visualizebool):
        plt.ylim(0, img.height)
        plt.xlim(0, img.width)
        plt.show()
    mask = np.array(mask, dtype=np.uint8)
    #apply mask
    final = cv2.bitwise_and(imgarr, imgarr, mask=mask)
    finalvis = final[:, :, ::-1].copy()  # convert from RGB to BGR
    if(visualizebool):
        cv2.imshow('Image with Mask', finalvis)
        cv2.waitKey()
    return final

def saturationthreshsegment(image,visualizebool): #assumes that ants possess more HSV saturation than the background and segments based on a saturation threshold - pretty bad
    imgarr = np.asarray(image)
    hsv_img = cv2.cvtColor(imgarr, cv2.COLOR_BGR2HSV)
    lowrange = [0, 150, 0]
    lowrange = np.asarray(lowrange)
    highrange = [180, 255, 255]
    highrange = np.asarray(highrange)
    mask = cv2.inRange(hsv_img, lowrange, highrange)
    if(visualizebool):
        cv2.imshow("mask", mask)
        cv2.waitKey()
    return mask