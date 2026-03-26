import math

import numpy as np
import cv2
from numpy import interp


def resize(old_img: np.ndarray, new_w: int, new_h: int):
	"""
		no interpolation - repeats pixels
	"""
	old_w = old_img.shape[1]
	old_h = old_img.shape[0]

	new_img = np.zeros(shape=([new_h, new_w, 3]), dtype='uint8')

	for new_i, line in enumerate(new_img):
		for new_j, pixl in enumerate(line):

			# discover equivalent coordinate in old image
			old_j = int(new_j*(old_w/new_w))
			old_i = int(new_i*(old_h/new_h))

			new_img[new_i][new_j] = old_img[old_i][old_j]

	return new_img


def bilinear(v00, v01, v10, v11, di, dj):
	return (
			v00 * (1 - di) * (1 - dj) +
			v01 * (1 - di) * dj +
			v10 * di * (1 - dj) +
			v11 * di * dj
	)


def resize_interp(old_img: np.ndarray, new_w: int, new_h: int = None):

	old_h, old_w, = old_img.shape[:2]

	if new_h is None:
		new_h = int(old_h*(new_w/old_w))


	new_img = np.zeros((new_h, new_w, 3), dtype='uint8')

	for new_i in range(new_h):
		for new_j in range(new_w):

			# pixel-center aligned mapping
			old_j = (new_j + 0.5) * (old_w / new_w) - 0.5
			old_i = (new_i + 0.5) * (old_h / new_h) - 0.5

			# bounds safety
			old_i = max(0, min(old_i, old_h - 1))
			old_j = max(0, min(old_j, old_w - 1))

			fi = int(math.floor(old_i))
			fj = int(math.floor(old_j))
			ci = min(fi + 1, old_h - 1)
			cj = min(fj + 1, old_w - 1)

			di = old_i - fi
			dj = old_j - fj

			v00 = old_img[fi, fj]
			v01 = old_img[fi, cj]
			v10 = old_img[ci, fj]
			v11 = old_img[ci, cj]

			new_img[new_i, new_j] = bilinear(v00, v01, v10, v11, di, dj)

	return new_img

img = cv2.imread('assets/gam.jpg')
resized = resize_interp(img, new_w=10000)

cv2.imshow('resized', resized)
cv2.waitKey(0)
cv2.destroyAllWindows()