import GraphMain
from PIL import Image
import numpy as np
from PIL import ImageEnhance

#WIP implementation of graph-based segmentation

graph = GraphMain
img = Image.open('head5.jpg')
img = ImageEnhance.Sharpness(img).enhance(2)
img = np.asarray(img)
graph.segment(in_image=img,sigma=0.8, k=325, min_size=75)