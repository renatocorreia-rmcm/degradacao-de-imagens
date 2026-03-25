import math

import numpy as np
import cv2


def linear_map(matrix: np.ndarray, img: np.ndarray):
	assert matrix.ndim == 2
	assert img.ndim == 3

	new_img = np.zeros(shape=img.shape, dtype='uint8')

	for i, line in enumerate(img):
		for p, pixl in enumerate(line):
			# compute new coordinates
			new_coord = matrix @ np.array([p, i])
			# assign to new img
			if 0 <= new_coord[0] < img.shape[1] and 0 <= new_coord[1] < img.shape[0]:
				new_img[int(new_coord[1])][int(new_coord[0])] = pixl

	cv2.imshow('linear map', new_img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


v: np.ndarray = cv2.imread('assets/gam.jpg')
A = np.array([[0.5, -0.5], [0, 0.5]])

theta = -math.pi/8
R = np.array([[math.cos(theta), math.sin(theta)], [-math.sin(theta), math.cos(theta)]])

linear_map(R, v)
