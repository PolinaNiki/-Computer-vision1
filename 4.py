#▅▅ -   92
#█▀█  -  96
# ⊂  94
#█▄█ -  95
#⊃ -  123
#all -  500

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import morphology

image = np.load("ps.npy.txt")
rectangle = np.array([[1,1,1,1,1,1], #  figure - ▅▅
                      [1,1,1,1,1,1],
                      [1,1,1,1,1,1],
                      [1,1,1,1,1,1]])

rec_not_complete1 = np.array([[1,1,1,1,1,1], # figure - █▀█ 
                             [1,1,1,1,1,1],
                             [1,1,0,0,1,1],
                             [1,1,0,0,1,1]])

rec_not_complete2 = np.array([[1,1,0,0,1,1], # figure - █▄█ 
                             [1,1,0,0,1,1],
                             [1,1,1,1,1,1],
                             [1,1,1,1,1,1]])

rec_not_complete3 = np.array([[1,1,1,1], # figure -  ⊂
                             [1,1,1,1],
                             [1,1,0,0],
                             [1,1,0,0],
                             [1,1,1,1],
                             [1,1,1,1]])
rec_not_complete4 = np.array([[1,1,1,1], # figure - ⊃
                             [1,1,1,1],
                             [0,0,1,1],
                             [0,0,1,1],
                             [1,1,1,1],
                             [1,1,1,1]])

result1 = morphology.binary_hit_or_miss(image, rectangle)
print("▅▅ -  ", np.sum(result1))
result2 = morphology.binary_hit_or_miss(image, rec_not_complete1)
print("█▀█  - ", np.sum(result2))
result4 = morphology.binary_hit_or_miss(image, rec_not_complete3)
print(" ⊂ ", np.sum(result4))
result3 = morphology.binary_hit_or_miss(image, rec_not_complete2)
print("█▄█ - ", np.sum(result3))
result5 = morphology.binary_hit_or_miss(image, rec_not_complete4)
print("⊃ - ", np.sum(result5))
all_figures = np.sum(result1)+np.sum(result2)+np.sum(result3)+np.sum(result4)+np.sum(result5)
print("all - ", all_figures)

plt.figure()
plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(result1)
plt.show()
