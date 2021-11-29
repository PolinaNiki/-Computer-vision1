import numpy as np
import matplotlib.pyplot as plt
from typing import Dict
 
def find_bias(image1, image2):
     for i in range(len(image1)):
         for j in range(len(image1[i])):
             if image1[i][j] == 1:
                 find_i = i
                 find_j = j
     for i in range(len(image2)):
         for j in range(len(image2[i])):
             if image2[i][j] == 1:
                 bias_i = abs(find_i - i)
                 bias_j = abs(find_j - j)
     return bias_i, bias_j
         

def read_data(file_name) -> Dict:
    return_array = []
    with open(file_name, 'r') as f:
        data = f.read()
    splited_data = data.split('\n')
    for row in splited_data[2:-1]:
        splited_row = row.split(' ')
        return_array.append(list(map(int, splited_row[:-1])))
    return {"array": return_array}
 
image1 = read_data("img1.txt")['array']
image2 = read_data("img2.txt")['array']

res_val = find_bias(image1, image2)
print(res_val)
 
plt.imshow(image2)
plt.show()