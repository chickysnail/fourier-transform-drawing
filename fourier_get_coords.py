import numpy as np
from MPLdraw import drawing
arr = drawing("background_images/letovo.png")
print(arr)
width = arr.shape[0]
height = arr.shape[1]
    
with open('fourier_image_coords.txt', 'w') as f:
    for i in range(width):
        for j in range(height):
            f.write(f'{arr[i, j]} ')
        f.write('\n')