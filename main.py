import cv2
import numpy as np

img: np.ndarray = cv2.imread('assets/gam.jpg')

if img is not None:
    print(type(img))
    print(img.shape)
    print(img)

    gray = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) / 3

    img[:, :, 0] = gray
    img[:, :, 1] = gray
    img[:, :, 2] = gray

    cv2.imshow('gam junior', img)

    # 0 means wait indefinitely for a key press
    # Any other positive integer (e.g., 1000) waits for that number of milliseconds
    cv2.waitKey(0)

    # Closes all the OpenCV windows we created
    cv2.destroyAllWindows()
