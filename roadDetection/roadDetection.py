#mask the image
#detect the road lines

import cv2
import numpy as np
import math

#change the image into gray scale:
def grayscaleImage(img):
	return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#identify the lanes in white color. Use canny
def cannyImg(img,low_threshold,high_threshold):

	'''
	OpenCV documentation: 
    	-If a pixel gradient is higher than the upper threshold, the pixel is accepted as an edge
    	-If a pixel gradient value is below the lower threshold, then it is rejected.
    	-If the pixel gradient is between the two thresholds, then it will be accepted only if it is connected to a pixel that is above the upper threshold.
	'''

	return cv2.Canny(img,low_threshold,high_threshold)

def maskImage(img,vertices):
	
	#step 1: apply an image mask
	#step 2: keep only the region of the image defined by the polygon (vertices)

	# apply the mask
	mask = np.zeros_like(img)
	#fill pixels inside the given polygon
	cv2.fillPoly(mask, vertices, 255)
	#cv2.imwrite('proba.jpg',mask)

	#bitwise_and --> Calculates the per-element bit-wise conjuction of two arrays or an array and a scalar
	masked_image = cv2.bitwise_and(img, mask)

	return masked_image

def hough_transform(img,rho,theta,threshold,min_line_len,max_line_gap):

	# cv2.HoughLinesP - detects lines in the mask images
	lines = cv2.HoughLinesP(img,rho,theta,threshold,np.array([]),minLineLength=min_line_len,maxLineGap = max_line_gap)

	return lines

def avarage_lanes(lines):

	left_lines = []
	left_weights = []
	right_lines = []
	right_weights = []

	#lines - array of line
	for line in lines:
		#line - (x1,y1,x2,y2) pontokbol all
		for x1,y1,x2,y2 in line:
			if x1 == x2:
				continue
			angle = (y2-y1)/(x2-x1)
			intercept = y1 - slope*x1
			length = np.sqrt((y2-y1)**2+(x2-x1)**2)

			# if angle < 0 --> left lane
			# if angle > 0 --> right lane

			if angle < 0:
				left_lines.append((angle,intercept))
				left_weights.append(length)
			else:
				right_lines.append((angle,intercept))
				right_weights.append((length))
	
	if len(left_weights) > 0:
		left_lane  = np.dot(left_weights,  left_lines) /np.sum(left_weights)
	else:
		left_lane = None

	if len(right_weights) > 0:
		right_lane = np.dot(right_weights, right_lines)/np.sum(right_weights)
	else:
		right_lane = None

	return left_lane,right_lane

def line_pixels(y1,y2,line):

	#Convert a line into pixels

	if line is None:
		return None

	(angle,intercept) = line

	x1 = int((y1-intercept)/angle)
	x2 = int((y2-intercept)/angle)

	y1 = int(y1)
	y2 = int(y2)

	#return the pixels
	return ((x1,y1),(x2,y2))

def lane_lines(img,lines):

	left_lane,right_lane = avarage_lanes(lines)

	y1 = image.shape[0]
	y2 = y1 * 0.6

	left_line = line_pixels(y1,y2,left_lane)
	right_line = line_pixels(y1,y2,right_lane)

	return left_line,right_line

def draw_lines(image,lines) :

	color = [0,0,255]
	thickness = 10

	line_img = np.zeros_like(image)

	for line in lines:
		if line is not None:
			cv2.line(line_img, (line[0][0],line[0][1]),(line[0][2],line[0][3]), color, thickness)

	return cv2.addWeighted(image,1.0,line_img,0.95,0.0)


if __name__ == "__main__":

	#load image
	try:
		image = cv2.imread('road.jpg')
	except FileNotFoundError:
		raise ValueError("Image not found!")

	#grayscale the image
	grayscale = grayscaleImage(image)
	cv2.imwrite('grayscale.jpg',grayscale)
	# apply Canny
	cannyImage = cannyImg(grayscale,50,150)
	cv2.imwrite('canny.jpg',cannyImage)

	#mask image	
	#kell irni egy fuggvenyt, ami kiszamolja pontosan a pontokat. De kb jo ertekek.
	edges = np.array([[(0,image.shape[0]),(450,320),(490,320),(image.shape[1],image.shape[0])]])
	masked_image = maskImage(cannyImage,edges)
	cv2.imwrite('masked_image.jpg',masked_image)

	#----Hough Transform Line Detection----
	# function : cv2.HoughLinesP 
	# parameters:
	#	rho - distance resolution of the accumulator in pixels.
	#	theta - angle resolution of the accumulator in radians.
	#	threshold - accumulator threshold parameter.  Only those lines are returned that get enough votes 
	#	minLineLenght - minimum line length
	#	maxLineGap - maximum allowed gap between points on the same line to link them.

	rho = 1
	theta = np.pi/180
	threshold = 20
	min_line_len = 20
	max_line_gap = 100
	
	lines = hough_transform(masked_image,rho,theta,threshold,min_line_len,max_line_gap)
	
	image = draw_lines(image,lines)

	cv2.imwrite('detected_lines.jpg',image)
