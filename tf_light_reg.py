import numpy as np
import cv2
import time

    
def traffic_light_check(img):
	lower_green = np.array([45,127,127])
	upper_green = np.array([75,255,255])
	#img = cv2.imread('images/green2.jpg')
	#img = cv2.imread('images/real.png')


	original_image = img


	blank_image = np.zeros((100,100,3), np.uint8)
	frame = cv2.blur(img,(15,15))
	#hsv convert
	hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	# Use inRange to capture only the values betdween lower & upper_blue


	#HSV EQ
	hsv_img[:,:,2] += 50
	#mark1 = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)




	mask = cv2.inRange(hsv_img, lower_green, upper_green)

	# Perform Bitwise AND on mask and our original frame
	res3 = cv2.bitwise_and(frame, frame, mask=mask)
	imgray = cv2.cvtColor(res3, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(imgray, 127, 255, 0)


	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	if len(contours) == 1:

	    cv2.drawContours(res3, contours, 0, (0,255,0), 1)
	    cnt = contours[0]

	    x,y,w,h = cv2.boundingRect(cnt)
	    #x = x-10
	    #y = y-10
	    #w = w+10
	    #h = h+10
	    #position of green light
	    #print x,y,w,h
	    #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	    crop_img = original_image[y-10: y + h + 20, x-10: x + w + 20]
	    crop_img = cv2.blur(crop_img,(1,1))

	    #See average color
	    average_color_per_row = np.average(crop_img, axis=0)
	    average_color = np.average(average_color_per_row, axis=0)

	    color_ = np.uint8([[[average_color[2],average_color[1],average_color[0]]]])
	    color_hsv = cv2.cvtColor(color_,cv2.COLOR_BGR2HSV)
	    h = color_hsv[0,0,0]
	    s = color_hsv[0,0,1]
	    v = color_hsv[0,0,2]

	    return 1,img

	return 0,img