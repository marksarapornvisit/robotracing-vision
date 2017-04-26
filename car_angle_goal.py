import cv2
import numpy as np
import lanedetector as lane
import math

def carangle(upposition,loposition):

	if len(upposition) > 0:
		x1 = upposition[1][0]
		x2 = upposition[0][1]
		x3 = loposition[1][0]
		x4 = loposition[0][1]

		upper_center = x2 - x1
		lower_center = x4 - x3
		a = upper_center - lower_center
		#b = y3 - y1
		b = 50

		seta = np.arctan(b/a)

		seta = np.rad2deg(seta)
		return seta
	else:
		pass
	
def carcenterpos(position,centerpixel = 240):
	#240 is from width frame divde 2
	if len(position) == 2:
		x1 = position[1][0] #left position
		x2 = position[0][0] #right position

		centerposition = (x2 + x1)/2

		#center_shift = centerposition - centerpixel
		center_shift = centerpixel - centerposition 

		#print (center_shift)
	else:
		return 0,0

	return int(centerposition),center_shift




#This will retrun index of array of lane chosing
def choselane(position,current_pos = 240):

	lane = []
	#lane.astype(int)
	if len(position) == 0:
		return False
	#len1 use current pos and follow that line
	###############################

	if len(position) == 1:
		return position
	#note to mark : edit here it's error
	###############################
	if len(position) == 2:
		return position

	if len(position) > 2:
		weight = np.zeros(len(position))
		for i in range(0,len(position)):
			if current_pos > position[i][0]:
				weight[i] = current_pos - position[i][0]
			else: 
				weight[i] = position[i][0] - current_pos

		minindex = np.zeros((2))
		j = 0
		for i in range(0,len(weight)):
			if weight[i] == min(weight):
				minindex[j] = i
				j = j + 1
				weight[i] = 99999
			if j == 2:
				break
		lane = position[int(minindex[0])],position[int(minindex[1])]
		return ([lane[0], lane[1]])
			
	
