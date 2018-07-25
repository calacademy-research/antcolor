from PIL import Image
from elasticsearch import Elasticsearch
import numpy as np
import cv2
from numpy import linalg

#soil, subterranean, - expecting light
#litter
#arboreal, above ground, vegetation, canopy
radius = 3
#query specimens from your elasticsearch
es = Elasticsearch()
r = es.search(index='allants4', doc_type='_doc', body={'from': 0, 'size': 50000, 'query': {"exists" : { "field" : "decimalLatitude", "field" : "lightness"}}})
# print(r['hits'])
dictspecimens = r['hits']['hits']
specimenset = []
#[360][180][3]
#for every specimen...
total = 0
for specimen in dictspecimens:
    # if has RGB and has geo location
    if((specimen['_source']['decimalLatitude'] != None) and (specimen['_source']['lightness'] != None) and ((specimen['_source']['genus'] == 'Pheidole'))):
        lat = specimen['_source']['decimalLatitude']
        #print("Lat: " + str(lat))
        latpixel = 90 - int(lat) #pixely = 90-latitude
        #print("LatPix: " + str(latpixel))
        lon = specimen['_source']['decimalLongitude']
        #print("Lon: " + str(lon))
        lonpixel = lon + 180
        #print("LonPix: " + str(lonpixel))
        red = specimen['_source']['red']
        green = specimen['_source']['green']
        blue = specimen['_source']['blue']
        s = (latpixel, lonpixel, red, green, blue)
        specimenset.append(s)

mapimg = Image.open('proportionalmap.png')
maparr = np.array(mapimg)
#print(maparr.shape)

x = 0
y = 0
for xcoord in maparr: #180
    for ycoord in xcoord: #360
        specsinradius = []
        for spec in specimenset:
            specx = spec[0] #lat pixel
            specy = spec[1] #lon pixel
            a = np.array([x,y])
            b = np.array([specx,specy])
            if((abs(x - specx) <= radius) and (abs(y - specy) <= radius)):
                if(np.linalg.norm(a-b) <= 3):
                    specsinradius.append(spec)
            #if((abs(x - specx) < radius) and (abs(y - specy) < radius)):
                #specsinradius.append(spec)
        if(len(specsinradius) > 0):
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
            maparr[x][y][0] = avgb
            maparr[x][y][1] = avgg
            maparr[x][y][2] = avgr
        y+=1
    y = 0
    x+=1
    print('X ' + str(x))
cv2.imshow('boom', maparr)
cv2.waitKey()