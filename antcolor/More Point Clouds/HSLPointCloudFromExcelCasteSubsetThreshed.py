from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from elasticsearch import Elasticsearch
import colorsys
import pandas

#blue queens
#green males
#red workers
colorbycaste= True;

reds1 = []
greens1 = []
blues1 = []
hues1 = []
sats1 = []
lights1 = []
RGBpoints1 = []
HLSpoints1 = []


data = pandas.read_excel("C:/Users/OWNER/Desktop/castegenusthreshed5.xlsx")
print(type(data))

for index, row in data.iterrows():
   r = row['meanred']
   g = row['meangreen']
   b = row['meanblue']
   reds1.append(r)
   greens1.append(g)
   blues1.append(b)
   hls = colorsys.rgb_to_hls(r, g, b)
   hues1.append(hls[0] * 255)
   lights1.append(hls[1])
   sats1.append(hls[2] * 255 * (-1))
   if(colorbycaste):
       RGBpoints1.append([0,0,1])
   else:
      RGBpoints1.append([r/255, g/255, b/255])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

RGBpoints1 = np.asarray(RGBpoints1)
print(RGBpoints1.shape)
ax.scatter(hues1,sats1,lights1,facecolors=RGBpoints1,s=10,marker='s',depthshade= False) #s = size of points

reds1 = []
greens1 = []
blues1 = []
hues1 = []
sats1 = []
lights1 = []
RGBpoints1 = []
HLSpoints1 = []

for index, row in data.iterrows():
   r = row['meanred.y']
   g = row['meangreen.y']
   b = row['meanblue.y']
   reds1.append(r)
   greens1.append(g)
   blues1.append(b)
   hls = colorsys.rgb_to_hls(r, g, b)
   hues1.append(hls[0] * 255)
   lights1.append(hls[1])
   sats1.append(hls[2] * 255 * (-1))
   if (colorbycaste):
       RGBpoints1.append([0,0.75,0]) #r/255, g/255, b/255
   else:
      RGBpoints1.append([r/255, g/255, b/255])  # r/255, g/255, b/255

RGBpoints1 = np.asarray(RGBpoints1)
print(RGBpoints1.shape)
ax.scatter(hues1,sats1,lights1,facecolors=RGBpoints1,s=10,marker='v',depthshade= False) #s = size of points

reds1 = []
greens1 = []
blues1 = []
hues1 = []
sats1 = []
lights1 = []
RGBpoints1 = []
HLSpoints1 = []

for index, row in data.iterrows():
   r = row['meanred.x']
   g = row['meangreen.x']
   b = row['meanblue.x']
   reds1.append(r)
   greens1.append(g)
   blues1.append(b)
   hls = colorsys.rgb_to_hls(r, g, b)
   hues1.append(hls[0] * 255)
   lights1.append(hls[1])
   sats1.append(hls[2] * 255 * (-1))
   if(colorbycaste):
      RGBpoints1.append([1,0,0])
   else:
      RGBpoints1.append([r/255, g/255, b/255])

RGBpoints1 = np.asarray(RGBpoints1)
print(RGBpoints1.shape)
ax.scatter(hues1,sats1,lights1,facecolors=RGBpoints1,s=10,marker='o',depthshade= False) #s = size of points

hueavg = [1];
satavg = [2];
lightavg = [3];

plt.title("")
plt.xlim((0,255)) #hue
plt.ylim((0,122.5)) #sat
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Lightness')
ax.set_zlim((0,122.5)) #light

plt.show()