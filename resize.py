import math

import numpy as np
import cv2


def resize(old_img: np.ndarray, new_w: int, new_h: int):
	"""
		no interpolation - repeats pixels
	"""
	old_w = old_img.shape[1]
	old_h = old_img.shape[0]

	if new_h == 0:
		new_h = int(old_h*(new_w/old_w))

	new_img = np.zeros(shape=([new_h, new_w, 3]), dtype='uint8')
	for new_i, line in enumerate(new_img):
		for new_j, pixl in enumerate(line):

			# discover equivalent coordinate in old image
			old_j = int(new_j*(old_w/new_w))
			old_i = int(new_i*(old_h/new_h))

			new_img[new_i][new_j] = old_img[old_i][old_j]

	return new_img


img = cv2.imread('assets/cat.jpg')
cv2.imshow('resized', resize(img, new_w=30, new_h=30))
cv2.waitKey(0)
cv2.destroyAllWindows()

