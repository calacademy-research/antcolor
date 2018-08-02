from elasticsearch import Elasticsearch
import requests
from Helpers import CQColorDefs
import json
import colorsys

####################
#### RefreshColorMetrics adds new metrics for color based on those already existing in a database.
#### Only necessary to run on databases created using old ColorQuantifier or if you want to add new color metrics without taking the time to reanalyze all the images
################

myindex = 'allants'
lastAnalyzed = 1
size = 50000

#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index=myindex, doc_type='_doc', body={"sort": [{"sortingid": {"order": "asc"}}, "_score"], 'from': (lastAnalyzed - 1), 'size': size, 'query': {'match_all': {}}})

dictspecimens = r['hits']['hits']

#for every specimen...
for specimen in dictspecimens:

    #initialize all parameters to be extracted from the image
    pixUsed = None
    pixSD = None
    imgUsed = None
    red = specimen['_source']['red']
    green = specimen['_source']['green']
    blue = specimen['_source']['blue']
    lightness = specimen['_source']['lightness'] #HSL lightness
    saturation = specimen['_source']['saturation'] #HSV saturation
    value = None #HSV value
    rednessHSV = None
    yellownessHSV = None
    orangenessHSV = None
    brownnessHSV = None
    darkbrownnessHSV = None
    blacknessHSV = None
    rednessRGB = None
    yellownessRGB = None
    orangenessRGB = None
    brownnessRGB = None
    darkbrownnessRGB = None
    blacknessRGB = None #distance from a single black on the vector of orange's hue

    avghls = colorsys.rgb_to_hls(red / 255.0, green / 255.0, blue / 255.0)
    avghsv = colorsys.rgb_to_hsv(red / 255.0, green / 255.0, blue / 255.0)

    hue = avghsv[0]
    saturation = avghsv[1] #HSV saturation- the amount of color, ie. the distance from white/black
    value = avghsv[2] #HSV value- distance from black, consider pure red equal to pure white

    #Redness etc. are estimates of relative color intensity based on HSL distance formulated by the author
    #Redness for example is a measure of the Euclidian distance from the color to pure red
    #This distance is floored at the distance from pure red to the black/white axis and scaled from 0-1
    #They may be considered as the distance from the color that would be assumed if the ant was fully saturated with a given pigment

    huedegrees = hue * 360
    rednessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,0,1,1)
    orangenessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,1)
    yellownessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,60,1,1)
    brownnessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,0.5)
    darkbrownnessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,0.25)
    blacknessHSV = CQColorDefs.hsvdist(huedegrees,saturation,value,30,1,0)
    rednessRGB = CQColorDefs.rgbdist(red, green, blue, 255, 0, 0)
    orangenessRGB = CQColorDefs.rgbdist(red, green, blue, 255, 127.5, 0)
    yellownessRGB = CQColorDefs.rgbdist(red, green, blue, 255,255,0)
    brownnessRGB = CQColorDefs.rgbdist(red, green, blue, 127.5,65.5,0)
    darkbrownnessRGB = CQColorDefs.rgbdist(red, green, blue, 63.75, 31.88, 0)
    blacknessRGB = CQColorDefs.rgbdist(red, green, blue, 0, 0, 0)

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
    specimen['_source']['blacknessHSV'] = blacknessHSV
    specimen['_source']['rednessRGB'] = rednessRGB
    specimen['_source']['yellownessRGB'] = yellownessRGB
    specimen['_source']['orangenessRGB'] = orangenessRGB
    specimen['_source']['brownnessRGB'] = brownnessRGB
    specimen['_source']['darkbrownnessRGB'] = darkbrownnessRGB
    specimen['_source']['blacknessRGB'] = blacknessRGB

    s = specimen['_source']
    i = specimen['_id']
    sortingi = specimen['_source']['sortingid']
    es.index(index=myindex, doc_type='_doc', id=i, body=s)
    print('ID Progress: ' + str(sortingi))