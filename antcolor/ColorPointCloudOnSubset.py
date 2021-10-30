from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from elasticsearch import Elasticsearch

es = Elasticsearch()
r = es.search(index='speciessubset4', doc_type='species', body={'from': 0, 'size': 10000, "query": { "match_all": {}}})

dictspecimens = r['hits']['hits']

reds = []
greens = []
blues = []
RGBpoints = []

#for every specimen...
for specimen in dictspecimens:
    r = specimen['_source']['meanred']
    g = specimen['_source']['meangreen']
    b = specimen['_source']['meanblue']
    reds.append(r)
    greens.append(g)
    blues.append(b)
    RGBpoints.append([r/255,g/255,b/255])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

RGBpoints = np.asarray(RGBpoints)
print(RGBpoints.shape)
ax.scatter(reds,greens,blues,facecolors=RGBpoints,s=10,marker=',',depthshade= False) #s = size of points
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
