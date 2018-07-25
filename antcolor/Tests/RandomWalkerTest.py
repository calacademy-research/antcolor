import numpy as np
import matplotlib.pyplot as plt

from skimage.segmentation import random_walker
from skimage.data import binary_blobs
from skimage.exposure import rescale_intensity
from skimage.viewer import ImageViewer
import skimage
from scipy import ndimage
from skimage import color
from numpy import ndarray
import cv2

# Generate noisy synthetic data
data = skimage.img_as_float(binary_blobs(length=128, seed=1))
sigma = 0.35
data += np.random.normal(loc=0, scale=sigma, size=data.shape)
data = rescale_intensity(data, in_range=(-sigma, 1 + sigma),
                         out_range=(-1, 1))

data = ndimage.imread('head1.jpg')
data = skimage.color.rgb2hsv(data)
print(str(data.shape))
viewer = ImageViewer(data)
viewer.show()

# The range of the binary image spans over (-1, 1).
# We choose the hottest and the coldest pixels as markers.

markers = np.zeros(data.shape)
markers = data[:,:,1] > 150
markers = markers.astype(int)
markers[markers == 1] = 2
markers[markers == 0] = 1
print(markers)
#data[threshold,1] = threshold
#markers[data[:,:,1] < 150] = 1
#markers[data[:,:,1]] = 2

# Run random walker algorithm
labels = random_walker(data, markers, beta=10, mode='bf')

# Plot results
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.2),
                                    sharex=True, sharey=True)
ax1.imshow(data, cmap='gray', interpolation='nearest')
ax1.axis('off')
ax1.set_title('Noisy data')
ax2.imshow(markers, cmap='magma', interpolation='nearest')
ax2.axis('off')
ax2.set_title('Markers')
ax3.imshow(labels, cmap='gray', interpolation='nearest')
ax3.axis('off')
ax3.set_title('Segmentation')

fig.tight_layout()
plt.show()