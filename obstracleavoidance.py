import cv2
import numpy as np
import imutils

def preprocess(image):

    img = image

    return img

def mask(image,colour,error=15, kernel=10):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)[:, :, 0]
    ret, thresh = cv2.threshold(hsv, colour-error, colour+error, cv2.THRESH_BINARY)
    kernel = np.ones((kernel,kernel),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    return thresh

def selectROI(image, pos_x, pos_y):
    '''
    select a porpotion of image in percentage of ...
    '''
    height = np.size(image, 0)
    width = np.size(image, 1)

    height_l = int(round(height*pos_y[0]))
    height_u = int(round(height*pos_y[1]))

    width_l = int(round(width*pos_x[0]))
    width_u = int(round(width*pos_x[1]))

    region = image[height_l:height_u, width_l:width_u]
    return region


def sidefill(mask, step=5,fillblack=False):
    height = mask.shape[0]
    width = mask.shape[1]

    canvas = np.zeros((height,width),np.uint8)

    for w in range(width-1,0,-step):
        black_flag = False
        for h in range(height-1,0,-step):
            paint = False
            if h == height-1:
                if mask[h,w] == 0:
                    black_flag = True
            if black_flag ==True:
                if mask[h,w] == 0:
                    if fillblack:
                        paint =True
                else:
                    black_flag = False
                    paint =True
            else:
                if mask[h,w] != 0:
                    paint =True
                else:
                    break
            if paint:
                canvas[h,w] = 255
    kernel = 10
    canvas = cv2.dilate(canvas,np.ones((kernel,kernel),np.uint8),iterations = 1)
    return canvas

def selectColour(roi):

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)[:, :, 0]
    mean = np.average(hsv)
    return mean

def main(image):
    roi = selectROI(image, [0.45,0.55], [1-0.15,1-0.05])
    colour = selectColour(roi)
    thresh = mask(image,colour)
    filled  = sidefill(thresh, fillblack=False)

    return filled