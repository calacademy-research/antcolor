from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from elasticsearch import Elasticsearch

####################
#### Each RGBPointCloud function displays a 3D plot of specimen colors in the RGB colorspace. Use OnAll to make all dots
#### specimens or OnSubset to make dots categories like castes or genera. VariedMarkers allows the plotting of different
####  subsets with different markers
################

es = Elasticsearch()
r = es.search(index='allants4', doc_type='_doc', body={'from': 0, 'size': 50000,
                                                       'query': {
                                                           "exists" : {"field" : "red"}
                                                        }
                                                        })
dictspecimens = r['hits']['hits']

reds = []
greens = []
blues = []
RGBpoints = []

print(len(dictspecimens))
#for every specimen...
for specimen in dictspecimens:
    #if(specimen['_source']['genus'] == 'Formica'):
    r = specimen['_source']['red']
    g = specimen['_source']['green']
    b = specimen['_source']['blue']
    reds.append(r)
    greens.append(g)
    blues.append(b)
    RGBpoints.append([r/255,g/255,b/255])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

RGBpoints = np.asarray(RGBpoints)
print(RGBpoints.shape)
ax.scatter(reds,greens,blues,facecolors=RGBpoints,s=1,marker=',',depthshade= False) #s = size of points
plt.title("3D Color Cloud")
min = 30
max = 220
plt.xlim((min,max))
plt.ylim((min,max))
ax.set_xlabel('Red Value')
ax.set_ylabel('Green Value')
ax.set_zlabel('Blue Value')
ax.set_zlim((min,max))

plt.show()

#TODO- plot various genera with different markers