from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from elasticsearch import Elasticsearch

es = Elasticsearch()
# r = es.search(index='allants2', doc_type='_doc', body={'from': 0, 'size': 1000, 'query': {"range" : {"age" : {"gt" : 0}}}})
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

#for every specimen...
for specimen in dictspecimens:
    if(specimen['_source']['genus'] == 'Formica'):
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
ax.scatter(reds,greens,blues,facecolors=RGBpoints,s=20,marker=',',depthshade= False) #s = size of points
plt.title("3D Color Cloud")
plt.xlim((0,255))
plt.ylim((0,255))
ax.set_xlabel('Red Value')
ax.set_ylabel('Green Value')
ax.set_zlabel('Blue Value')
ax.set_zlim((0,255))

plt.show()

#TODO- plot various genera with different markers