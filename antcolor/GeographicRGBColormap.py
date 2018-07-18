from PIL import Image
from elasticsearch import Elasticsearch
import numpy as np
import cv2

radius = 3
#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index='allants2', doc_type='_doc', body={'from': 0, 'size': 50000, 'query': {"exists" : { "field" : "decimalLatitude", "field" : "lightness"}}})
# print(r['hits'])
dictspecimens = r['hits']['hits']

specimenset = []
#[360][180][3]
#for every specimen...
total = 0
for specimen in dictspecimens:
    # if has RGB and has geo location
    # print(specimen)
    if((specimen['_source']['decimalLatitude'] != None) and (specimen['_source']['lightness'] != None)):
        lat = specimen['_source']['decimalLatitude']
        latpixel = 90 - int(lat) #pixely = 90-latitude
        lon = specimen['_source']['decimalLongitude']
        lonpixel = lon + 180
        red = specimen['_source']['red']
        green = specimen['_source']['green']
        blue = specimen['_source']['blue']
        s = (latpixel, lonpixel, red, green, blue)
        specimenset.append(s)

mapimg = Image.open('proportionalmap.png')
maparr = np.array(mapimg)

x = 0
y = 0
for xcoord in maparr:
    for ycoord in xcoord:
        specsinradius = []
        for spec in specimenset:
            specx = spec[0]
            specy = spec[1]
            if((abs(x - specy) < radius) and (abs(y - specx) < radius)):
                specsinradius.append(spec)
        print(specsinradius)
        if(len(specsinradius) > 0):
            print('some in radius')
            totalr = 0
            totalg = 0
            totalb = 0

            for s in specsinradius:
                totalr += s[2]
                totalg += s[3]
                totalb += s[4]

            avgr = totalr / len(specsinradius)
            avgg = totalg / len(specsinradius)
            avgb = totalb / len(specsinradius)
            maparr[y][x][0] = avgb
            maparr[y][x][1] = avgg
            maparr[y][x][2] = avgr
            print(maparr)
        y+=1
        print('Y ' + str(y))
    y = 0
    x+=1
    print('X ' + str(x))
cv2.imshow('boom', maparr)
cv2.waitKey()