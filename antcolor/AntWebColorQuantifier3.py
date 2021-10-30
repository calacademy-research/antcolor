from elasticsearch import Elasticsearch
import requests
from requests.adapters import HTTPAdapter
from requests.adapters import Retry
import json
from io import BytesIO
import colorsys
from PIL import Image
import numpy as np
from timeit import default_timer as timer
import imghdr
import math
import random
from Helpers import CQColorDefs
from Helpers import CQSegmentations

####################
#### AntWebColorQuantifier extracts and stores color data from AntWeb specimen images stored in Elasticsearch.
#### Before running, use AntWeb2Elastic to index specimens to an index with the mapping specified in kibanacommands.txt
################

myindex = 'allantshsv' #The Elasticsearch index to pull from and index to
lastAnalyzed = 1
#Start at 1 for first run. Set to last analyzed for subsequent runs
size = 50000 #The number of specimens to attempt to query and analyze starting from lastAnalyzed
visualizeAll = False #set whether to visualize the image transformations as they occur
visualizeEnd = True
saveSegmentImg = True
bulk = False #set whether to index new values one at a time as they are discovered or in bulk once discovery is finished
randomize = True
indexElastic = False
shotType = 'H' #H for head, P for profile, D for dorsal
#TODO imageQuality = 0 #0 for low, 1 for medium, 2 for high

#query specimens from your elasticsearch ordered by
es = Elasticsearch()
r = es.search(index=myindex, doc_type='_doc', body={"sort": [{"sortingid": {"order": "asc"}}, "_score"], 'from': (lastAnalyzed - 1), 'size': size, 'query': {'match_all': {}}}) #20000-25000 missing?
specimenlist = r['hits']['hits']

if(randomize):
    random.shuffle(specimenlist)

total = 0
extracted = 0
#for every specimen...
for specimen in specimenlist:
    #get specimenCode
    c = specimen['_source']['specimenCode']
    print(c)
    #cancel if SEM mounted
    if specimen['_source']['medium'] == 'SEM mount':
        c = ''
    #query image from AntWeb
    session = requests.Session()
    retry = requests.adapters.Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    url = 'https://antweb.org/v3.1/images?shotType=' + shotType + '&specimenCode=' + c + '&up=1'
    r = requests.get(url)

    #convert image to json
    d = r.json()
    p = d['images']
    j = json.dumps(p)

    #initialize all parameters to be extracted from the image
    pixUsed = None
    pixSD = None
    red = None
    green = None
    blue = None
    hue = None #HSL/HSV hue
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
        #print(string)  # prints image link
        imgUsed = string
        r = requests.get(string)

        #make sure image is valid and continue
        if (imghdr.what(BytesIO(r.content)) != None):
            img = Image.open(BytesIO(r.content))
            imgarr = np.array(img)

            #check for greyscale (SEM images) again which would cause errors
            if(len(imgarr.shape) == 3):

                #segment using one of the functions provided in CQSegmentations
                start = timer()
                segmented = CQSegmentations.snakesegment(image=img, visAll=visualizeAll, visEnd=visualizeEnd,saveOutput=saveSegmentImg,outputName=c)
                #print('Segment time:' + str(timer() - start))

                #restart the loop after segment if we're not actually indexing the data
                if(indexElastic == False):
                    continue

                #get pixel values from segmented
                allred = []
                allgreen = []
                allblue = []
                pixelhsl = None
                allhue = []
                allhslsat = []
                allhsvsat = []
                alllight = []
                allval = []
                for row in segmented:
                    for pixel in row:
                        if(pixel[0] != 0):
                                allred.append(pixel[0])
                                allgreen.append(pixel[1])
                                allblue.append(pixel[2])
                                pixelhsl = colorsys.rgb_to_hls(pixel[0]/255, pixel[1]/255, pixel[2]/255)
                                pixelhsv = colorsys.rgb_to_hsv(pixel[0]/255, pixel[1]/255, pixel[2]/255)
                                allhue.append(pixelhsl[0] * 360)
                                allhslsat.append(pixelhsl[2])
                                alllight.append(pixelhsl[1])
                                allhsvsat.append(pixelhsv[1])
                                allval.append(pixelhsv[2])


                #deal with collapsing snake bug
                if(len(allred) != 0):

                    #get the number of pixels used
                    pixUsed = len(allred)

                    #calculate standard deviation of pixel values, may be useful for considering color variation
                    sd1 = np.std(np.array(allhue))
                    sd2 = np.std(np.array(allhslsat))
                    sd3 = np.std(np.array(alllight))
                    pixSD = math.sqrt((sd1 * sd1 + sd2 * sd2 + sd3 * sd3) / 3)

                    #calculate averages
                    avgred = sum(allred) / float(len(allred))
                    avggreen = sum(allgreen) / float(len(allgreen))
                    avgblue = sum(allblue) / float(len(allblue))
                    avghue = sum(allhue) / float(len(allhue))
                    avghslsat = sum(allhslsat) / float(len(allhslsat))
                    avghsvsat = sum(allhsvsat) / float(len(allhsvsat))
                    avglight = sum(alllight) / float(len(alllight))
                    avgval = sum(allval) / float(len(allval))

                    #prints RGB, HSV, and HSL results results
                    print('^^^ ' + 'RGB(' + str(avgred) + ',' + str(avggreen) + ',' + str(avgblue) + ')' + ' ^^^')
                    print('^^^ ' + 'HSL(' + str(avghue) + ',' + str(avghslsat) + ',' + str(avglight) + ')' + ' ^^^')
                    print('^^^ ' + 'HSV(' + str(avghue) + ',' + str(avghsvsat) + ',' + str(avgval) + ')' + ' ^^^')

                    lightness = avglight #HSL lightness
                    hue = avghue #HSL/HSV hue
                    saturation = avghslsat #HSV saturation
                    value = avgval #HSV value
                    red = avgred
                    green = avggreen
                    blue = avgblue
                    lightbluenessHSV = avghsvsat #temp hack

                    #Redness etc. are estimates of relative color intensity based on HSL distance formulated by the author
                    #Redness for example is a measure of the Euclidian distance from the color to pure red, with higher values closer to red
                    #This distance is floored at the distance from pure red to the black/white axis and scaled from 0-1

                    huedegrees = hue;

                    #HSL distance
                    rednessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 0, 1, .5)
                    orangenessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 30, 1, .5)
                    yellownessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 60, 1, .5)
                    brownnessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 30, 1, 0.25)
                    darkbrownnessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 30, 1, 0.125)
                    brownblacknessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, huedegrees, saturation, 0)
                    greennessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 120, 1, .5)
                    #lightbluenessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 180, 1, .5)
                    bluenessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 240, 1, .5)
                    purplenessHSV = CQColorDefs.hsvhsldist(huedegrees, saturation, lightness, 270, 1, .5)

                    #RGB distance, currently not in use
                    # rednessRGB = CQColorDefs.rgbdist(red, green, blue, 255, 0, 0)
                    # orangenessRGB = CQColorDefs.rgbdist(red, green, blue, 255, 127.5, 0)
                    # yellownessRGB = CQColorDefs.rgbdist(red, green, blue, 255,255,0)
                    # brownnessRGB = CQColorDefs.rgbdist(red, green, blue, 127.5,65.5,0)
                    # darkbrownnessRGB = CQColorDefs.rgbdist(red, green, blue, 63.75, 31.88, 0)
                    # brownblacknessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 0, 0)
                    # greennessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 255, 0)
                    # lightbluenessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 255, 255)
                    # bluenessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 0, 255)
                    # purplenessRGB = CQColorDefs.rgbdist(red, green, blue, 127.5, 0, 255)

                    extracted+=1
                    total+=1

                    print('Extracted: ' + str(extracted)) #the number of specimens with properly extracted colors
                    print('Total: ' + str(total)) #the total number of specimens analyzed
                    print('Total time:' + str(timer() - start))

    #if lightness is still None, no analysis took place so set all to None
    if lightness == None:
        total+=1
        print('SPECIMEN SKIPPED: ' + str(c)) #print specimen code
        if(indexElastic == False):
            continue

    specimen['_source']['pixUsed'] = pixUsed
    specimen['_source']['pixSD'] = pixSD
    specimen['_source']['imgUsed'] = imgUsed
    specimen['_source']['red'] = red
    specimen['_source']['green'] = green
    specimen['_source']['blue'] = blue
    specimen['_source']['hue'] = hue
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

    #specimen['_source']['rednessRGB'] = rednessRGB
    #specimen['_source']['yellownessRGB'] = yellownessRGB
    #specimen['_source']['orangenessRGB'] = orangenessRGB
    #specimen['_source']['brownnessRGB'] = brownnessRGB
    #specimen['_source']['darkbrownnessRGB'] = darkbrownnessRGB
    #specimen['_source']['brownblacknessRGB'] = brownblacknessRGB
    #specimen['_source']['greennessRGB'] = greennessRGB
    #specimen['_source']['lightbluenessRGB'] = lightbluenessRGB
    #specimen['_source']['bluenessRGB'] = bluenessRGB
    #specimen['_source']['purplenessRGB'] = purplenessRGB

    s = specimen['_source']
    i = specimen['_id']
    sortingi = specimen['_source']['sortingid']
    if(not bulk):
        es.index(index=myindex, doc_type='_doc', id=i, body=s)
        print('Last Sorting ID: ' + str(sortingi))


if(bulk):
    for s in specimenlist:
        specimen = s['_source']
        id = s['_id']
        es.index(index=myindex, doc_type='_doc', id=id, body=specimen)