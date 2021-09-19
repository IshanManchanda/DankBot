from os.path import abspath, join as path_join, split as path_split

from cv2 import CHAIN_APPROX_NONE, CascadeClassifier, MORPH_CROSS, \
	RETR_EXTERNAL, THRESH_BINARY, THRESH_BINARY_INV, bitwise_and, \
	boundingRect, dilate, findContours, getStructuringElement, \
	threshold
from numpy import array

bin_path = path_split(abspath(__file__))[0]


def find_chars(img):
	# Convert image to B&W
	gray = array(img.convert("L"))

	# Convert image to binary
	ret, mask = threshold(gray, 180, 255, THRESH_BINARY)
	image_final = bitwise_and(gray, gray, mask=mask)

	ret, new_img = threshold(image_final, 180, 255, THRESH_BINARY_INV)

	# Idk
	kernel = getStructuringElement(MORPH_CROSS, (3, 3))
	dilated = dilate(new_img, kernel, iterations=1)
	contours, _ = findContours(dilated, RETR_EXTERNAL, CHAIN_APPROX_NONE)

	coords = []
	for contour in contours:
		# get rectangle bounding contour
		[x, y, w, h] = boundingRect(contour)
		# ignore large chars (probably not chars)
		# if w > 70 and h > 70:
		# 	continue
		coords.append((x, y, w, h))
	return coords


def find_eyes(img):
	coords = []
	face_cascade = CascadeClassifier(
		path_join(bin_path, 'resources/classifiers/haarcascade_frontalface.xml')
	)
	eye_cascade = CascadeClassifier(
		path_join(bin_path, 'resources/classifiers/haarcascade_eye.xml')
	)
	gray = array(img.convert("L"))

	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in faces:
		roi_gray = gray[y:y + h, x:x + w]
		eyes = eye_cascade.detectMultiScale(roi_gray)
		for (ex, ey, ew, eh) in eyes:
			coords.append((x + ex + ew / 2, y + ey + eh / 2))
	return coords
