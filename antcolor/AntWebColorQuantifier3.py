from elasticsearch import Elasticsearch
import requests
import json
from io import BytesIO
import colorsys
from PIL import Image
import numpy as np
from timeit import default_timer as timer
import imghdr
import math
from Helpers import CQColorDefs
from Helpers import CQSegmentations

####################
#### AntWebColorQuantifier4 extracts and stores color data from AntWeb specimen images stored in Elasticsearch.
#### Before running, use AntWeb2Elastic to index specimens to an index with the mapping specified in kibanacommands.txt
################

myindex = 'allants' #The Elasticsearch index to pull from and index to
lastAnalyzed = 44281 #Start at 1 for first run. Set to last analyzed for subsequent runs #14000
size = 10000 #The number of specimens to attempt to query and analyze starting from lastAnalyzed
visualize = True #set whether to visualize the image transformations
bulk = False #set whether to index new values one at a time as they are discovered or in bulk once discovery is finished
#shotType = 'H' #H for head, P for profile, D for dorsal
#imageQuality = 1 #0 for low, 1 for medium, 2 for high

#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index=myindex, doc_type='_doc', body={"sort": [{"sortingid": {"order": "asc"}}, "_score"], 'from': (lastAnalyzed - 1), 'size': size, 'query': {'match_all': {}}}) #20000-25000 missing?
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

    #initialize all parameters to be extracted from the image
    pixUsed = None
    pixSD = None
    red = None
    green = None
    blue = None
    lightness = None #HSL lightness
    saturation = None #HSV saturation
    value = None #HSV value
    rednessHSV = None
    yellownessHSV = None
    orangenessHSV = None
    brownnessHSV = None
    darkbrownnessHSV = None
    brownblacknessHSV = None
    greennessHSV = None
    lightbluenessHSV = None
    bluenessHSV = None
    purplenessHSV = None
    rednessRGB = None
    yellownessRGB = None
    orangenessRGB = None
    brownnessRGB = None
    darkbrownnessRGB = None
    brownblacknessRGB = None
    greennessRGB = None
    lightbluenessRGB = None
    bluenessRGB = None
    purplenessRGB = None
    imgUsed = None

    #make sure the query produced a valid result
    if (len(j) > 4):
        #have to search for substrings because the dictionary isn't organized predictably
        endindex = j.find('h_1_low.jpg') + 11
        startindex = j.rfind('https', 0, endindex)
        string = j[startindex:endindex]
        if(string == ""): #h1 doesn't exist
            endindex = j.find('h_2_low.jpg') + 11
            startindex = j.rfind('https', 0, endindex)
            string = j[startindex:endindex]
        if (string == ""):  # h2 doesn't exist either, AHH! Fortunately, h3 must exist now
            endindex = j.find('h_3_low.jpg') + 11
            startindex = j.rfind('https', 0, endindex)
            string = j[startindex:endindex]

        string = j[startindex:endindex]
        print(string)  # prints image link
        imgUsed = string
        r = requests.get(string)

        #make sure image is valid and continue
        if (imghdr.what(BytesIO(r.content)) != None):
            img = Image.open(BytesIO(r.content))
            imgarr = np.array(img)

            #check for greyscale (SEM images) which cause errors
            if(len(imgarr.shape) == 3):
                start = timer()
                segmented = CQSegmentations.snakesegment(image=img, visualizebool=visualize)
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
                    pixUsed = len(allred)
                    sdred = np.std(np.array(allred))
                    sdgreen = np.std(np.array(allgreen))
                    sdblue = np.std(np.array(allblue))
                    pixSD = math.sqrt((sdred * sdred + sdgreen * sdgreen + sdblue * sdblue) / 3)
                    avgred = sum(allred) / float(len(allred))
                    avggreen = sum(allgreen) / float(len(allgreen)) #RGB values- the amount of red, green, and blue needed to create the color
                    avgblue = sum(allblue) / float(len(allblue))
                    print('^^^ ' + 'RGB(' + str(avgred) + ',' + str(avggreen) + ',' + str(avgblue) + ')' + ' ^^^') #prints RGB result from above image link
                    avghls = colorsys.rgb_to_hls(avgred / 255.0, avggreen / 255.0, avgblue / 255.0)
                    avghsv = colorsys.rgb_to_hsv(avgred / 255.0, avggreen / 255.0, avgblue / 255.0)
                    #avgcmyk = rgb_to_cmyk(avgred,avggreen,avgblue)

                    lightness = avghls[1] #HSL lightness- the amount of light in the color, ie the amount of light/heat reflected by the
                    hue = avghsv[0]
                    saturation = avghsv[1] #HSV saturation- the amount of color, ie. the distance from white/black
                    value = avghsv[2] #HSV value- distance from black, consider pure red equal to pure white
                    red = avgred
                    green = avggreen
                    blue = avgblue

                    #Redness etc. are estimates of relative color intensity based on HSL distance formulated by the author
                    #Redness for example is a measure of the Euclidian distance from the color to pure red
                    #This distance is floored at the distance from pure red to the black/white axis and scaled from 0-1

                    huedegrees = hue * 360
                    rednessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,0,1,1)
                    orangenessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,1)
                    yellownessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,60,1,1)
                    brownnessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,0.5)
                    darkbrownnessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,0.25)
                    brownblacknessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,huedegrees,saturation,0)
                    greennessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,120,1,1)
                    lightbluenessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,180,1,1)
                    bluenessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,240,1,1)
                    purplenessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,270,1,1)

                    rednessRGB = CQColorDefs.rgbdist(red, green, blue, 255, 0, 0)
                    orangenessRGB = CQColorDefs.rgbdist(red, green, blue, 255, 127.5, 0)
                    yellownessRGB = CQColorDefs.rgbdist(red, green, blue, 255,255,0)
                    brownnessRGB = CQColorDefs.rgbdist(red, green, blue, 127.5,65.5,0)
                    darkbrownnessRGB = CQColorDefs.rgbdist(red, green, blue, 63.75, 31.88, 0)
                    brownblacknessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 0, 0)
                    greennessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 255, 0)
                    lightbluenessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 255, 255)
                    bluenessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 0, 255)
                    purplenessRGB = CQColorDefs.rgbdist(red, green, blue, 127.5, 0, 255)

                    extracted+=1
                    total+=1

                    print('Extracted: ' + str(extracted)) #the number of specimens with properly extracted colors
                    print('Total: ' + str(total)) #the total number of specimens analyzed
                    print('Total time:' + str(timer() - start))

    #if lightness is still 0, no analysis took place so set all to None
    if lightness == None:
        total+=1
        print('SPECIMEN SKIPPED: ' + str(c)) #print specimen code

    specimen['_source']['pixUsed'] = pixUsed
    specimen['_source']['pixSD'] = pixSD
    specimen['_source']['imgUsed'] = imgUsed
    specimen['_source']['red'] = red
    specimen['_source']['green'] = green
    specimen['_source']['blue'] = blue
    specimen['_source']['lightness'] = lightness
    specimen['_source']['saturation'] = saturation
    specimen['_source']['value'] = value

    specimen['_source']['rednessHSV'] = rednessHSV
    specimen['_source']['yellownessHSV'] = yellownessHSV
    specimen['_source']['orangenessHSV'] = orangenessHSV
    specimen['_source']['brownnessHSV'] = brownnessHSV
    specimen['_source']['darkbrownnessHSV'] = darkbrownnessHSV
    specimen['_source']['brownblacknessHSV'] = brownblacknessHSV
    specimen['_source']['greennessHSV'] = greennessHSV
    specimen['_source']['lightbluenessHSV'] = lightbluenessHSV
    specimen['_source']['bluenessHSV'] = bluenessHSV
    specimen['_source']['purplenessHSV'] = purplenessHSV

    specimen['_source']['rednessRGB'] = rednessRGB
    specimen['_source']['yellownessRGB'] = yellownessRGB
    specimen['_source']['orangenessRGB'] = orangenessRGB
    specimen['_source']['brownnessRGB'] = brownnessRGB
    specimen['_source']['darkbrownnessRGB'] = darkbrownnessRGB
    specimen['_source']['brownblacknessRGB'] = brownblacknessRGB
    specimen['_source']['greennessRGB'] = greennessRGB
    specimen['_source']['lightbluenessRGB'] = lightbluenessRGB
    specimen['_source']['bluenessRGB'] = bluenessRGB
    specimen['_source']['purplenessRGB'] = purplenessRGB


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