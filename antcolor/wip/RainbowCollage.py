from elasticsearch import Elasticsearch
import requests
import json
import numpy as np
from PIL import Image
from io import BytesIO
import cv2

#WIP, currently saves columns one by one
es = Elasticsearch()
r = es.search(index='allants', doc_type='_doc',
              body={"sort": [{"lightness": {"order": "desc"}}, "_score"], 'size': 50000, 'query': {"exists" : {"field" : "rednessHSV"}}})
dictspecimens = r['hits']['hits']

numtall = 10
#Red
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['rednessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
reddestmerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    reddestmerged = np.vstack((reddestmerged,imgarr))

reddestmerged = reddestmerged[:, :, ::-1].copy()
cv2.imwrite('red.png',reddestmerged)

#Orange
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['orangenessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
orangemerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    orangemerged = np.vstack((orangemerged,imgarr))


orangemerged = orangemerged[:, :, ::-1].copy()

cv2.imwrite('orange.png',orangemerged)

#YELLOW
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['yellownessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
yellowmerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    yellowmerged = np.vstack((yellowmerged,imgarr))

yellowmerged = yellowmerged[:, :, ::-1].copy()
cv2.imwrite('yellow.png',yellowmerged)

#GREEN
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['greennessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
greenmerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    greenmerged = np.vstack((greenmerged,imgarr))

greenmerged = greenmerged[:, :, ::-1].copy()
cv2.imwrite('green.png',greenmerged)

#LIGHT BLUE
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['lightbluenessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
lightbluemerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    lightbluemerged = np.vstack((lightbluemerged,imgarr))

lightbluemerged = lightbluemerged[:, :, ::-1].copy()
cv2.imwrite('lightblue.png',lightbluemerged)

#BLUENESS MERGED
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['bluenessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
bluemerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    bluemerged = np.vstack((bluemerged,imgarr))

bluemerged = bluemerged[:, :, ::-1].copy()
cv2.imwrite('blue.png',bluemerged)

#PURPLE
reddest = list()
for specimen in dictspecimens:
    s = specimen['_source']
    redness = s['purplenessHSV']
    img = s['imgUsed']
    if(len(reddest) < numtall):
        reddest.append((redness,img))
        print(reddest)
    else:
        min = (100,)
        for red in reddest:
            if(red[0] < min[0]):
                min = red
        if(redness > min[0]):
            reddest.remove(min)
            reddest.append((redness,img))

print(reddest)

reddestsorted = reddest.sort(key=lambda tup: tup[1], reverse=True)

print(reddestsorted)

imglink = reddest[0]
imglink = imglink[1]
purplemerged = Image.open(BytesIO(requests.get(imglink).content))
for x in range(1,numtall):
    imglink =  reddest[x]
    imglink = imglink[1]
    r = requests.get(imglink)
    img = Image.open(BytesIO(r.content))
    imgarr = np.array(img)
    purplemerged = np.vstack((purplemerged,imgarr))

purplemerged = purplemerged[:, :, ::-1].copy()
cv2.imwrite('purple.png',purplemerged)

#rainbow = np.hstack((reddestmerged,orangemerged,yellowmerged,greenmerged,lightbluemerged,bluemerged,purplemerged))

cv2.imshow('r', rainbow)
cv2.waitKey()