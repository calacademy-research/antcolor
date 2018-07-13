
from PIL import Image
import numpy as np
import cv2
import SnakeMain
import colorsys
from PIL import ImageEnhance

testimages = ['ants\head1.jpg', 'ants\head2.jpg', 'ants\head3.jpg', 'ants\head4.jpg', 'ants\head5.jpg',  'ants\head6.jpg',  'ants\head7.jpg']
for img in testimages:
    img = Image.open(img)
    contrasted = ImageEnhance.Contrast(img).enhance(2)
    contrastedarr = np.array(contrasted)
    contrastedarr = contrastedarr[:, :, ::-1].copy()  # convert from RGB to BGR
    cv2.imshow('Contrasted Image', contrastedarr)
    cv2.waitKey()
    greyscaled = cv2.cvtColor(contrastedarr, cv2.COLOR_BGR2GRAY)
    filtered = greyscaled
    filtered = cv2.bilateralFilter(greyscaled, 6, 50, 50)
    cv2.imshow('Bilaterally Filtered Image', filtered)
    cv2.waitKey()
    edged = cv2.Canny(filtered, 100, 225)
    cv2.imshow('Image Edges with Canny', edged)
    cv2.waitKey()
    # image = Image.open(img)
    # segmented = snakesegment(image, visualizebool=True)
    # allred = []
    # allgreen = []
    # allblue = []
    # for row in segmented:
    #     for pixel in row:
    #         if (pixel[0] != 0):
    #             allred.append(pixel[0])
    #             allgreen.append(pixel[1])
    #             allblue.append(pixel[2])
    #
    # avgred = sum(allred) / float(len(allred))
    # avggreen = sum(allgreen) / float(len(allgreen))
    # avgblue = sum(allblue) / float(len(allblue))
    # print('RGB(' + str(avgred) + ',' + str(avggreen) + ',' + str(avgblue) + ')' + ' ^^^')
    # avghls = colorsys.rgb_to_hls(avgred / 255.0, avggreen / 255.0, avgblue / 255.0)
    # avghsv = colorsys.rgb_to_hsv(avgred / 255.0, avggreen / 255.0, avgblue / 255.0)
    #
    # avglightness = avghls[1]
    # print(avglightness)
    # avgsaturation = avghsv[1]
    # print(avgsaturation)
