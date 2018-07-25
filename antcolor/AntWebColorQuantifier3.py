from elasticsearch import Elasticsearch
import requests
import json
from io import BytesIO
import colorsys
from PIL import Image
from PIL import ImageEnhance
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Helpers import SnakeMain
from matplotlib.path import Path
from timeit import default_timer as timer
import imghdr
from skimage.segmentation import active_contour
from skimage import img_as_float


####################################################################################################################################################################################################
####### AntWebColorQuantifier3 adds rgb, hsl and hsv color data to AntWeb specimens in Elasticsearch. Requires proper mapping and specimen data in the requested Elasticsearch index ###########
####################################################################################################################################################################################################

def scisnakesegment(image,visualizebool): #function to segment using the included snake (active contour) algorithm after applying the canny algorithm to find edges

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
    snake = active_contour(img, init, alpha=0.15, beta=1, gamma=0.05, w_line=0.1, w_edge=1)
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
    imgarr = np.asarray(img)
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

########################
#### END OF FUNCTIONS
########################

myindex = 'allants4'
lastAnalyzed = 5000 #Start at 1 for first run. Set to last analyzed for subsequent runs
visualize = True #set whether to visualize the image transformations
bulk = True #set whether to index new values one at a time as they are discovered or in bulk once discovery is finished

#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index=myindex, doc_type='_doc', body={"sort": [{"sortingid": {"order": "asc"}}, "_score"], 'from': (lastAnalyzed - 1), 'size': 10000, 'query': {'match_all': {}}}) #20000-25000 missing?
# print(r['hits']) #34647
dictspecimens = r['hits']['hits']

#for every specimen...
total = 0
extracted = 0
for specimen in dictspecimens:
    c = specimen['_source']['specimenCode']
    if specimen['_source']['medium'] == 'SEM mount':
        c = ''
    r = requests.get('http://api.antweb.org/v3.1/images?shotType=H&specimenCode=' + c) #adjust shotType as preferred
    d = r.json()

    #parse for the new image query
    p = d['images']
    j = json.dumps(p)

    lightness = 0
    red = 0
    green = 0
    blue = 0
    saturation = 0

    #make sure the query has images
    if (len(j) > 4):

        # get first link, which will be the "low quality" image
        startindex = j.find('ht')
        endindex = j.find('.jp')
        string = j[startindex:endindex+4]
        print(string) #prints image link
        r = requests.get(string)

        #make sure image is valid and continue
        if (imghdr.what(BytesIO(r.content)) != None):
            img = Image.open(BytesIO(r.content))
            imgarr = np.array(img)

            # check for greyscale (SEM images) which would mess everything up
            if(len(imgarr.shape) == 3):

                start = timer()
                segmented = scisnakesegment(image=img, visualizebool=visualize)
                print('Segment time:' + str(timer() - start))
                allred = []
                allgreen = []
                allblue = []
                for row in segmented:
                    for pixel in row:
                        if(pixel[0] != 0):
                                allred.append(pixel[0])
                                allgreen.append(pixel[1])
                                allblue.append(pixel[2])

                #deal with collapsing snake due to random loaves of bread
                if(len(allred) != 0):
                    avgred = sum(allred) / float(len(allred))
                    avggreen = sum(allgreen) / float(len(allgreen)) #RGB values- the amount of red, green, and blue needed to create the color
                    avgblue = sum(allblue) / float(len(allblue))
                    print('^^^ ' + 'RGB(' + str(avgred) + ',' + str(avggreen) + ',' + str(avgblue) + ')' + ' ^^^') #prints RGB result from above image link
                    avghls = colorsys.rgb_to_hls(avgred / 255.0, avggreen / 255.0, avgblue / 255.0)
                    avghsv = colorsys.rgb_to_hsv(avgred / 255.0, avggreen / 255.0, avgblue / 255.0)

                    avglightness = avghls[1] #HSL lightness- the amount of light in the color, ie the amount of light/heat reflected by the
                    avgsaturation = avghsv[1] #HSV saturation- the amount of color, ie. the distance from white/black

                    lightness = avglightness
                    red = avgred
                    green = avggreen
                    blue = avgblue
                    saturation = avgsaturation

                    extracted+=1
                    total+=1
                    print('Extracted: ' + str(extracted)) #the number of specimens with properly extracted colors
                    # print('Total: ' + str(total)) #the total number of specimens analyzed
                    print('Total time:' + str(timer() - start))

    if lightness == 0:
        lightness = None
        total+=1
        print('SPECIMEN SKIPPED')
        # print(c) #code of skipped specimen

    if red == 0:
        red = None
    if green == 0:
        green = None;
    if blue == 0:
        blue = None;
    if saturation == 0:
        saturation = None;

    specimen['_source']['lightness'] = lightness;
    specimen['_source']['saturation'] = saturation;
    specimen['_source']['red'] = red;
    specimen['_source']['green'] = green;
    specimen['_source']['blue'] = blue;
    s = specimen['_source']
    i = specimen['_id']
    sortingi = specimen['_source']['sortingid']
    if(not bulk):
        es.index(index=myindex, doc_type='_doc', id=i, body=s)
        print('Last Sorting ID: ' + str(sortingi))


if(bulk):
    for s in dictspecimens:
        specimen = s['_source']
        id = s['_id']
        es.index(index=myindex, doc_type='_doc', id=id, body=specimen)

#previous version- AntWebColormatic2ElectricAntaloo