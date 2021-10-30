from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from elasticsearch import Elasticsearch
import colorsys
import pandas

####################
#### ColorPointCloudFromExcel creates an HSL point cloud using Excel data
################

reds1 = []
greens1 = []
blues1 = []
hues1 = []
sats1 = []
lights1 = []
RGBpoints1 = []
HLSpoints1 = []


data = pandas.read_excel("C:/Users/OWNER/Desktop/speciesdata.xlsx")
print(type(data))
#scatter all ie. Pheidole

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
   RGBpoints1.append([r / 255, g / 255, b / 255])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

RGBpoints1 = np.asarray(RGBpoints1)
print(RGBpoints1.shape)
ax.scatter(hues1,sats1,lights1,facecolors=RGBpoints1,s=1.25,marker='1',depthshade= False) #s = size of points


plt.title("")
plt.xlim((0,255)) #hue
plt.ylim((0,175)) #sat
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Lightness')
ax.set_zlim((0,175)) #light

plt.show()