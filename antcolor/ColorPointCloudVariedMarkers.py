from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from elasticsearch import Elasticsearch
import colorsys

es = Elasticsearch()
r = es.search(index='allantshsv', doc_type='_doc', body={'from': 0, 'size': 50000,
                                                       'query': {
                                                           "exists" : {"field" : "red"}
                                                        }
                                                        })
dictspecimens = r['hits']['hits']

reds1 = []
greens1 = []
blues1 = []
hues1 = []
sats1 = []
lights1 = []
RGBpoints1 = []
HLSpoints1 = []

print(len(dictspecimens))

#scatter all ie. Pheidole
for specimen in dictspecimens:
    if(True): #specimen['_source']['genus'] == 'Pheidole'
        if(specimen['_source']['caste'] == 'worker'):
            r = specimen['_source']['red']
            g = specimen['_source']['green']
            b = specimen['_source']['blue']
            reds1.append(r)
            greens1.append(g)
            blues1.append(b)
            hls = colorsys.rgb_to_hls(r,g,b)
            print(str(hls))
            hues1.append(hls[0]*255)
            lights1.append(hls[1])
            sats1.append(hls[2]*255*(-1))
            #HLSpoints1.append(hls[0] / 255, hls[2] / 255, hls[1] / 255)
            RGBpoints1.append([r/255,g/255,b/255])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

RGBpoints1 = np.asarray(RGBpoints1)
print(RGBpoints1.shape)
ax.scatter(hues1,sats1,lights1,facecolors=RGBpoints1,s=10,marker='2',depthshade= False) #s = size of points

reds1 = []
greens1 = []
blues1 = []
RGBpoints1 = []

#scatter all Camponotus
for specimen in dictspecimens:
    if (False):
        if(specimen['_source']['caste'] == 'queen'):
            r = specimen['_source']['red']
            g = specimen['_source']['green']
            b = specimen['_source']['blue']
            reds1.append(r)
            greens1.append(g)
            blues1.append(b)
            RGBpoints1.append([r/255,g/255,b/255])

#RGBpoints1 = np.asarray(RGBpoints1)
#print(RGBpoints1.shape)
#HLSpoints1 = np.asarray(HLSpoints1)
#ax.scatter(hues1,sats1,lights1,facecolors=RGBpoints1,s=10,marker='o',depthshade= False) #s = size of points


plt.title("3D Color Cloud")
min = 30
max = 220
plt.xlim((min,max))
plt.ylim((min,max))
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Lightness')
ax.set_zlim((min,max))

plt.show()

#TODO- plot various genera with different markers