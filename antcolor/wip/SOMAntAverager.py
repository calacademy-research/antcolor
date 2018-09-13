from PIL import Image
import cv2
import numpy as np
from elasticsearch import Elasticsearch
import requests
import json
from io import BytesIO
from minisom import MiniSom
import matplotlib.pyplot as plt
from sklearn import datasets
from PIL import ImageEnhance
import AntWebColorQuantifier3

#an attempt to apply a visual Self Organizing Map to ants of a given genus. unfinished
es = Elasticsearch()
#change genus name below
r = es.search(index='allants', doc_type='_doc', body={'query': {'match': {'genus' : 'Pheidole'}}})
dictspecimens = r['hits']['hits']

matrix = []
progress = 0
dictspecimens = dictspecimens[0:20]
#add all specimens in genus to training set for SOM
for specimen in dictspecimens:
    c = specimen['_source']['specimenCode']
    r = requests.get('http://api.antweb.org/v3.1/images?shotType=H&specimenCode=' + c)
    d = r.json()

    # parse for the new image query
    p = d['images']
    j = json.dumps(p)
    startindex = j.find('ht')
    endindex = j.find('.jp')
    string = j[startindex:endindex + 4]

    #get image from query
    r = requests.get(string)
    img = Image.open(BytesIO(r.content))

    #contrast, greyscale, filter, edge, resize
    contrasted = ImageEnhance.Contrast(img).enhance(2)
    contrastedarr = np.array(contrasted)
    contrastedarr = contrastedarr[:, :, ::-1].copy()  # convert from RGB to BGR
    cv2.imshow('Contrasted Image', contrastedarr)
    cv2.waitKey()
    greyscaled = cv2.cvtColor(contrastedarr, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(greyscaled, 6, 50, 50)
    cv2.imshow('Bilaterally Filtered Image', contrastedarr)
    cv2.waitKey()
    edged = cv2.Canny(filtered, 125, 250)  # 100, 225
    img = Image.fromarray(edged)
    resized = img.resize((30, 30), Image.ANTIALIAS)

    resized.show()

    #resize and binarize!
    imgarr = np.array(img)
    resized = img.resize((30,30), Image.ANTIALIAS)
    resized.show()
    grayscale = resized.convert('L')
    grayscale.show()
    binarized = grayscale.point(lambda x: 0 if x<128 else 255, '1')
    binarized.show()
    binarized = grayscale #skip binarization
    imgarr = np.asarray(grayscale)
    flattened = imgarr.flatten()
    print(flattened)
    matrix.append(flattened)

trainingdata = np.asarray(matrix)
som = MiniSom(6, 6, 900, sigma=0.3, learning_rate=0.5)
print ("Training...")
som.train_random(trainingdata, 20)

#visualize- like this but with ANTS!!
digits = datasets.load_digits(n_class=4)
data = digits.data  # matrix where each row is a vector that represent a digit.
num = digits.target  # num[i] is the digit represented by data[i]

som = MiniSom(20, 20, 64, sigma=.8, learning_rate=0.5)
print("Training...")
som.train_random(data, 1500)  # random training
print("\n...ready!")
plt.figure(figsize=(7, 7))
wmap = {}
im = 0
for x, t in zip(data, num):  # scatterplot
    w = som.winner(x)
    wmap[w] = im
    plt. text(w[0]+.5,  w[1]+.5,  str(t),
              color=plt.cm.Dark2(t / 4.), fontdict={'weight': 'bold',  'size': 11})
    im = im + 1
plt.axis([0, som.get_weights().shape[0], 0,  som.get_weights().shape[1]])

print('Loadin')
plt.figure(figsize=(10, 10), facecolor='white')
cnt = 0
for j in reversed(range(20)):  # images mosaic
    for i in range(20):
        plt.subplot(20, 20, cnt+1, frameon=False,  xticks=[],  yticks=[])
        if (i, j) in wmap:
            plt.imshow(digits.images[wmap[(i, j)]],
                       cmap='Greys', interpolation='nearest')
        else:
            plt.imshow(np.zeros((8, 8)),  cmap='Greys')
        cnt = cnt + 1

plt.tight_layout()
plt.show()


