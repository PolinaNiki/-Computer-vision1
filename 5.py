import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import morphology
from skimage.measure import label, regionprops
from skimage.filters import threshold_triangle

def circularity(region, label = 1):
    return (region.perimeter ** 2) / region.area

def toGray(image):
    return (0.2989 * image[:,:,0] + 0.587 * image[:,:,1] + 0.114 * image[:,:,2]).astype("uint8")

def binarisation(image, limit_min, limit_max):
    A = image.copy()
    A[A >= limit_max] = 0
    A[A <= limit_min] = 0
    A[A > 0] = 1
    return A

pencil = 0

for i in range(1, 13):
    
    image = plt.imread("img ("+str(i)+").jpg")
  
    gray = toGray(image)
  
    thresh = threshold_triangle(gray)
  
    binary = binarisation(gray, 0, thresh)
    binary = morphology.binary_dilation(binary, iterations = 1)
  
    labeled = label(binary)
    areas = []
    for region in regionprops(labeled):
        areas.append(region.area)
    
    for region in regionprops(labeled):
        if region.area < np.mean(areas):
            labeled[labeled == region.label] = 0
        bbox = region.bbox
        if bbox[0] == 0 or bbox[1] == 0:
            labeled[labeled == region.label] = 0
        
    labeled[labeled > 0] = 1
    labeled = label(labeled)
  
    c = 0 #счетчик
    kol = 0
    for region in regionprops(labeled):

        c += 1
        if (( (320000 < region.area < 500000) and (circularity(region, c) > 100))):
            kol += 1
    print("Количество карандашей на img ("+str(i)+").jpg = ", kol)
    pencil = pencil + kol

print("Общее число карандашей = ", pencil)

