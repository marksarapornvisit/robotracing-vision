import cv2
import numpy as np
from scipy import signal
import imutils
def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edged = cv2.Canny(image, 0, 50)
    kernel = np.ones((10,10),np.uint8)
    edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)


    # return the edged image
    return edged

def inversePerspective(image):
    height = np.size(image, 0)
    width = np.size(image, 1)

    horizon = 0.64
    horizon_width = 0.06

    pts1 = np.float32(
        [[width*(0.5 - horizon_width), height*horizon],
        [width*(0.5 + horizon_width), height*horizon],
        [0,height],[width,height]])

    pts2 = np.float32([[height*(0.5 - horizon_width),0],[height*(0.5 + horizon_width),0],[height*0.45,width],[height*0.55,width]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    perspective = cv2.warpPerspective(image, M, (height, width))
    blur = cv2.GaussianBlur(perspective, (3, 3), 0)
    blur = cv2.GaussianBlur(blur, (5, 5), 0)
    blur = cv2.GaussianBlur(blur, (15, 15), 0)

    return blur


def lineTransform(edges,image):

    minLineLength  = 100
    maxLineGap = 10


    lines = cv2.HoughLinesP(edges, 1, np.pi/180.0, 100, np.array([]), 200, 100)
    a,b,c = lines.shape
    for i in range(a):
        cv2.line(image, (lines[i][0][0], lines[i][0][1]),
        (lines[i][0][2], lines[i][0][3]), (255, 0, 255), 1, cv2.LINE_AA)

    return image

def highPass(frame,gain = 2):
    frame = np.abs(((cv2.Laplacian(frame,cv2.CV_64F)**gain))*3)
    return np.abs(frame.astype(np.uint8))

def threshold(frame, lower=30, upper=255, kernel=5):
    '''
    asdasdas
    '''
    k = np.ones((kernel, kernel), np.uint8)


    ret, binary = cv2.threshold(frame.astype(np.uint8), lower, upper, cv2.THRESH_BINARY)

    binary = cv2.dilate(binary, k, iterations=4)
    binary = cv2.erode(binary, k, iteration=4)
    # binary = cv2.dilate(binary,k,iterations = 1)
    # binary = cv2.erode(binary,k,iterations = 1)

    # binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, k)
    # binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, k)

    return binary

def threshold_2(roi, thresh_l=130, thresh_h=255, channel=2):
    '''
    hsv image thresholding
    '''
    # Threshold the Image
    single_channel = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)[:, :, channel]
    ret, thresh = cv2.threshold(single_channel, thresh_l, thresh_h, cv2.THRESH_BINARY)
    return thresh

def detect(thresh):
    '''
    detect the lanes in ROI
    return list of position pos(x,y)
    '''
    #setup
    pos = []

    #finds contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    #finds position
    for cnt in cnts:
        # compute the center of the contour
        moment = cv2.moments(cnt)
        pos_x = int((moment["m10"] / moment["m00"]))
        pos_y = int((moment["m01"] / moment["m00"]))
        #add position to the list
        pos.append([pos_x, pos_y])
    return pos

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

def drawPos(ROI, pos):
    frame = ROI

    for x, y in pos:
        cv2.circle(frame, (y, x), 15, (255, 255, 255), -1)

    return frame
