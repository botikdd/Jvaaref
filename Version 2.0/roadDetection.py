import cv2
import numpy as np
import math
import SerialHandler
import threading,serial,time,sys

global serialHandler

#Change the image into gray scale:
def grayscaleImage(img):
	return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#Identify the lanes in white color. Use canny
def cannyImg(img,low_threshold,high_threshold):

	'''
	OpenCV documentation: 
    	-If a pixel gradient is higher than the upper threshold, the pixel is accepted as an edge
    	-If a pixel gradient value is below the lower threshold, then it is rejected.
    	-If the pixel gradient is between the two thresholds, then it will be accepted only if it is connected to a pixel that is above the upper threshold.
	'''

	return cv2.Canny(img,low_threshold,high_threshold)

#Get the vertices of the polygon
def getPolygon(image_proba,i):

	'''
	Coordinates:

	(0,0) --> left upper corner

	(0,0) --- x
	
	|
	|

	y

	'''

	rows = image_proba.shape[0] 	# 2464
	cols = image_proba.shape[1]		# 3280

	bottom_left  = [cols*0.4, rows*0.4]
	top_left     = [cols*0.15, rows*0.9]
	bottom_right = [cols*0.95, rows*0.9]
	top_right    = [cols*0.6, rows*0.32]

	
	#TEST: draw the polygon
	'''
	
	cv2.circle(image_proba,(int(cols*0.4), int(rows*0.4)),20,(255,0,0),-1)
	cv2.circle(image_proba,(int(cols*0.15), int(rows*0.9)),20,(255,0,0),-1)
	cv2.circle(image_proba,(int(cols*0.95), int(rows*0.9)),20,(255,0,0),-1)
	cv2.circle(image_proba,(int(cols*0.6), int(rows*0.32)),20,(255,0,0),-1)

	proba = "proba" + str(i) + ".jpg"

	cv2.imwrite(proba,image_proba)
	'''
	return np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)

def maskImage(img,i):
	
	#step 1: apply an image mask
	#step 2: keep only the region of the image defined by the polygon (vertices)

	vertices = getPolygon(img,i)

	#Apply the mask
	mask = np.zeros_like(img)

	#Fill pixels inside the given polygon
	#if len(mask.shape) == 2 : 255
	#else (255,) * mask.shape[2]
	cv2.fillPoly(mask, vertices, 255)

	#bitwise_and --> Calculates the per-element bit-wise conjuction of two arrays or an array and a scalar
	return 	cv2.bitwise_and(img, mask)

def hough_transform(img,rho,theta,threshold,min_line_len,max_line_gap):

	#cv2.HoughLinesP - detects lines in the mask images
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

			intercept = y1 - angle*x1

			# if angle < 0 --> left line
			# if angle > 0 --> right line

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

	#print("Bal sav hossza: ", len(left_lines))
	#print("Jobb sav hossza: ", len(right_lines))

    #Kicsi vonalak ne kavarjanak be pluszba. Uj savot hoznak letre.
	if len(left_lines) * 3 < len(right_lines):
		left_lane = None
	if len(right_lines) * 3 < len(left_lines):
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

#Get left and right lines
def lane_lines(img,lines):

	left_lane,right_lane = avarage_lanes(lines)

	y1 = image.shape[0]
	y2 = y1 * 0.4

	left_line = line_pixels(y1,y2,left_lane)
	right_line = line_pixels(y1,y2,right_lane)

	return left_line,right_line

#Draw the lines.
def draw_lines(image,lines) :

	color = [0,0,255]
	thickness = 70

	line_img = np.zeros_like(image)

	for line in lines:
		if line is not None:
			cv2.line(line_img,*line,color,thickness)

	return cv2.addWeighted(image,1.0,line_img,0.95,0.0)

#Get the angles and move the car.
def angle_of_lines(left,right):

	# angle = atan(y2-y1,x2-x1) * 180 / pi
    if left is None and right is None:
        print("Nincs sav, Romaniaban vagyunk.")
        return 0,0

	if left is None:
		print("No left line recognized.")
		angle_left = 0
	else:
		angle_left = np.arctan2(left[0][1]-left[1][1],left[0][0]-left[1][0]) * 180/np.pi

	if right is None:
		print("No right line recognized.")
		angle_right = 0
	else:
		angle_right = np.arctan2(right[1][1]-right[0][1],right[1][0]-right[0][0]) * 180/np.pi

	angle_left = abs(angle_left)
	angle_right = abs(angle_right)

	print("Angles: ")
	print("Left: ",angle_left)
	print("Right: ",angle_right)

	return angle_left,angle_right

if __name__ == "__main__":

    #Initialization
	i = 0
    global serialHandler

    serialHandler=SerialHandler.SerialHandler()
    serialHandler.startReadThread()
    
    motion_event = threading.Event()
    serialHandler.readThread.addWaiter("MCTL",motion_event)
    serialHandler.readThread.addWaiter("BRAK",motion_event)

    speed = 0.0
    brake_speed = 0.0
    car_angle = 0.0

    stop = False
        
    try:
        while i < 7 and stop == False

            #lines = []
            #lane_lines = []

            i = i + 1

            print("\nImage nr ",i)

            #load image
            load_img = "test/road" + str(i) + ".jpg"
            try:
                image = cv2.imread(load_img)
            except FileNotFoundError:
                raise ValueError("Image not found!")

            #grayscale the image
            grayscale = grayscaleImage(image)
            #grayscale_img = "test_results/grayscale" + str(i) + ".jpg"
            #cv2.imwrite(grayscale_img,grayscale)
            
            # apply Canny
            cannyImage = cannyImg(grayscale,50,150)
            canny_img = "test_results/canny" + str(i) + ".jpg"
            cv2.imwrite(canny_img,cannyImage)

            #mask image
            masked_image = maskImage(cannyImage,i)
            masked_img = "test_results/masked_img" + str(i) + ".jpg"
            cv2.imwrite(masked_img,masked_image)

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

            #Get the angles : left & right
            angles = angle_of_lines(lane_line[0],lane_line[1])

            #There are no lines
            if angles[0] == 0 and angles[1] == 0:

                print("Nincs sav, Romania.")
                sent = serialHandler.sendBrake(brake_speed)
                if sent:
                    motion_event.wait()
                    print("Breaking sent")
                
                else:
                    print("Sending brake signal problem")
                print("KeyboardInterrupt Exception, wait 5 seconds for the serial handler to close connection")
                time.sleep(5.0)
                serialHandler.readThread.deleteWaiter("BRAK",motion_event)
                serialHandler.readThread.deleteWaiter("MCTL",motion_event)
                serialHandler.close()
                stop = True
    
            if (abs(angles[0] - angles[1]) < 1.5) and angles[0] != 0 and angles[1] != 0:
                print("OK. GO.")
                if speed <= 9.0:
                    speed = speed + 1.0
            else:
                print("El van fordulva.")
                if angles[0] < angles[1]:
                    print("Jobb szog nagyobb. Balra kell kanyarodni")
                    if angle <= 8.0:
                        angle = angle + 2.0
                else:
                    print("Bal szog nagyobb. Jobbra kell kanyarodni")
                    if angle >= 8.0:
                        angle = angle - 2.0

            image = draw_lines(image,lane_line)

            detected_img = "test_results/detected_img" + str(i) + ".jpg"
            cv2.imwrite(detected_img,image)

            print("-------------------")

    except KeyboardInterrupt:
        sent = serialHandler.sendBrake(brake_speed)
        if sent:
            motion_event.wait()
            print("Braking sent")
            
            else:
                print("Sending brake signal problem")
            print("KeyboardInterrupt Exception, wait 5 seconds for the serial handler to close connection")
            time.sleep(5.0)
            serialHandler.readThread.deleteWaiter("BRAK",motion_event)
            serialHandler.readThread.deleteWaiter("MCTL",motion_event)
            serialHandler.close()
            exit()


