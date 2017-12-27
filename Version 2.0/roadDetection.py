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

def getPolygon(image):

	'''
	Get the vertices of the polygon

	Coordinates of the image:

	(0,0) --> left upper corner

	(0,0) --- x
	
	|
	|

	y

	'''

	rows = image.shape[0] 	# 2464
	cols = image.shape[1]	# 3280

	bottom_left  = [cols*0.4, rows*0.4]
	top_left     = [cols*0.1, rows*0.9]
	bottom_right = [cols*0.9, rows*0.9]
	top_right    = [cols*0.6, rows*0.32]
	
	edges = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)

	return edges

def maskImage(img):
	
	#step 1: apply an image mask
	#step 2: keep only the region of the image defined by the polygon (vertices)

	vertices = getPolygon(img)

	# apply the mask
	mask = np.zeros_like(img)

	#fill pixels inside the given polygon
	#if len(mask.shape) == 2 : 255
	#else (255,) * mask.shape[2]
	cv2.fillPoly(mask, vertices, 255)

	#cv2.imwrite('proba.jpg',mask)

	#bitwise_and --> Calculates the per-element bit-wise conjuction of two arrays or an array and a scalar
	masked_image = cv2.bitwise_and(img, mask)

	return masked_image

def hough_transform(img,rho,theta,threshold,min_line_len,max_line_gap):

	# cv2.HoughLinesP - detects lines in the mask images
	lines = cv2.HoughLinesP(img,rho,theta,threshold,np.array([]),minLineLength=min_line_len,maxLineGap = max_line_gap)

	'''
	lines = cv2.HoughLines(img,1,np.pi/180,10)

	for rho,theta in lines[0]:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho

		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*a)
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*a)

		cv2.line(img1,(x1,y1),(x2,y2),(0,0,255),2)

	'''

	return lines

def avarage_lanes(lines):

	# lines - array of line
	# line = (x1,y1,x2,y2) coordinates

	left_lines 		= []
	left_weights 	= []
	right_lines 	= []
	right_weights 	= []

	for line in lines:
		for x1,y1,x2,y2 in line:
			if x1 == x2:
				continue
			# lenght of line
			length = np.sqrt((y2-y1)**2+(x2-x1)**2)
			
			angle = (y2-y1)/(x2-x1)

			# doles
			intercept = y1 - angle*x1

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

	angle = line[0]
	intercept = line[1]

	x1 = int((y1-intercept)/angle)
	x2 = int((y2-intercept)/angle)

	y1 = int(y1)
	y2 = int(y2)

	#return the pixels
	return ((x1,y1),(x2,y2))

def lane_lines(img,lines):

	left_lane,right_lane = avarage_lanes(lines)

	y1 = image.shape[0]
	y2 = y1 * 0.4

	left_line = line_pixels(y1,y2,left_lane)
	right_line = line_pixels(y1,y2,right_lane)

	return left_line,right_line

def draw_lines(image,lines) :

	color = [0,0,255]
	thickness = 70

	line_img = np.zeros_like(image)

	for line in lines:
		if line is not None:
			cv2.line(line_img,*line,color,thickness)

	return cv2.addWeighted(image,1.0,line_img,0.95,0.0)

def angle_of_lines(left,right):

	# angle = atan(y2-y1,x2-x1) * 180 / pi

	turn_left = 0
	turn_right = 0

	if left is None:
		print("No left line recognized.")
		angle_left = 0
		turn_left = 1
	else:
		angle_left = np.arctan2(left[0][1]-left[1][1],left[0][0]-left[1][0]) * 180/np.pi

	if right is None:
		print("No right line recognized.")
		angle_right = 0
		turn_right = 1
	else:
		angle_right = np.arctan2(right[1][1]-right[0][1],right[1][0]-right[0][0]) * 180/np.pi

	angle_left = abs(angle_left)
	angle_right = abs(angle_right)


	if (abs(angle_left - angle_right) < 1.5):
		print("OK")
	else:
		print("El van fordulva.")


	print(angle_left)
	print(angle_right)

	return angle_left,angle_right


if __name__ == "__main__":

	#load image
	try:
		image = cv2.imread('road_direction_lessleft.jpg')
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
	#edges = np.array([[(0,image.shape[0]),(450,320),(490,320),(image.shape[1],image.shape[0])]])
	masked_image = maskImage(cannyImage)
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

	lane_line = lane_lines(masked_image,lines)
	
	print("\nLines: ")
	print("Left: ", lane_line[0])
	print("Right: ",lane_line[1])
	print("")

	angle = angle_of_lines(lane_line[0],lane_line[1])

	image = draw_lines(image,lane_line)

	cv2.imwrite('detected_lines.jpg',image)
