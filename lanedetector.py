import cv2
import numpy as np
import imutils

def detect(perspective, roipos, thresh_l=120, thresh_h=255):
    '''
    main function
    '''

    region = selectROI(perspective, roipos[0], roipos[1])
    thresh = threshold(region, thresh_l=thresh_l, thresh_h=thresh_h)
    position = detect_blob(thresh)

    return region, thresh, position

def drawpos(region, position, radius=20, colour=(0, 255, 0)):
    '''
    draw in perspective mat
    '''
    ret = False
    if len(position) > 0:
        for x, y in position:
            cv2.circle(region, (x, y), radius, colour, 2)
        ret = True
    else:
        pass

    return ret

def perspective_transform(image):

    '''
    return the perspective transform
    '''

    height = np.size(image, 0)
    width = np.size(image, 1)

    horizon = 0.64
    horizon_width = 0.06

    pts1 = np.float32([[width*(0.5 - horizon_width), height*horizon],
                       [width*(0.5 + horizon_width), height*horizon],
                       [0, height], [width, height]])

    pts2 = np.float32([[height*(0.5 - horizon_width), 0],
                       [height*(0.5 + horizon_width), 0],
                       [height*0.45, width],
                       [height*0.55, width]])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    perspective = cv2.warpPerspective(image, matrix, (height, width))
    blur = cv2.GaussianBlur(perspective, (3, 3), 0)
    blur = cv2.GaussianBlur(blur, (5, 5), 0)
    blur = cv2.GaussianBlur(blur, (15, 15), 0)

    return blur

def threshold(roi, thresh_l=120, thresh_h=255, channel=2):
    '''
    hsv image thresholding
    '''
    # Threshold the Image
    single_channel = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)[:, :, channel]
    ret, thresh = cv2.threshold(single_channel, thresh_l, thresh_h, cv2.THRESH_BINARY)
    return thresh

def detect_blob(thresh):
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
    if len(cnts) <= 0:
        pass
    else:
        for cnt in cnts:
            # compute the center of the contour
            moment = cv2.moments(cnt)
            if moment["m00"] != 0:
                pos_x = int(moment["m10"] / moment["m00"])
                pos_y = int(moment["m01"] / moment["m00"])
                pos.append([pos_x, pos_y])
            else:
                pass
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
