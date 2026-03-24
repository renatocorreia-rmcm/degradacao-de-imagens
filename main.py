import cv2
import numpy as np

img: np.ndarray = cv2.imread('assets/gradiente.png')

if img is not None:
    print(type(img))
    print(img.shape)
    print(img)
    print(img)