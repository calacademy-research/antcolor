import numpy as np
import cv2
from PIL import Image
from PIL import ImageEnhance
import SnakeMain
import SnakeObj
import pylab as plt
from matplotlib.path import Path
import GraphMain


#get edges with cv2's canny algorithm
img = Image.open('head4.jpg')
contrasted = ImageEnhance.Contrast(img).enhance(2)
imgarr = np.asarray(contrasted)
imgarr = cv2.bilateralFilter(imgarr, 15,100,100)
edged = cv2.Canny(imgarr, 150,300)
cv2.imshow('edged', edged)
cv2.waitKey()

snakemain = SnakeMain.SnakeMain()
snakemain.load_image(file_to_load=edged)

while(snakemain.progress < 50):
    pass
contours = snakemain.points
width = img.width
height = img.height
contours = np.asarray(contours)
print(contours)

#fix contours
# for point in contours:
#     point[1] = height - point[1]

# polygon=[(0.1*width, 0.1*height), (0.15*width, 0.7*height), (0.8*width, 0.75*height), (0.72*width, 0.15*height)]
poly_path=Path(contours)

y, x = np.mgrid[:height, :width]
coors=np.hstack((x.reshape(-1, 1), y.reshape(-1,1))) # coors.shape is (4000000,2)

mask = poly_path.contains_points(coors)
print(type(mask))
plt.imshow(mask.reshape(height, width))
mask = mask.reshape(height,width)
plt.ylim(0,img.height)
plt.xlim(0,img.width)
plt.show()
mask = np.array(mask, dtype=np.uint8)
res = cv2.bitwise_and(imgarr,imgarr,mask = mask)
cv2.imshow('final',res)
cv2.waitKey()
graph = GraphMain
graph.segment(in_image=res,sigma=0.8, k=325, min_size=75)

x, y = contours.T
plt.scatter(x,y)
plt.ylim(0,img.height)
plt.xlim(0,img.width)
plt.show()
