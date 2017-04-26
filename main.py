#!/usr/bin/env python
# http://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
import serial

import lanedetector as lane
import obstracleavoidance as obst
import car_angle_goal as carang
import datatoarduino as arduino

# import os


fvs = FileVideoStream("videos/GOPR0205_3.avi").start()

# start the FPS timer
fps = FPS().start()
time.sleep(1.0)
i = 0

# loop over frames from the video file stream
while fvs.more():
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale (while still retaining 3
    # channels)
    frame = fvs.read()
    i = i+1
    if i%1 == 0:
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gray = np.dstack([gray, gray, gray])

        # main algorithm goes here
        # set perspective
        perspective = lane.perspective_transform(frame)

        # obstracle avoidance
        pathAvaliable = obst.main(perspective)

        # detect and draw 
        for i in range(3,4):
            region, thresh, position = lane.detect(perspective, [[0, 1], [i/10, i/10+0.05]])
            lane.drawpos(region, position)

            #mark edit 23 apr 2017
            if i == 3:
                upposition = position
            if i == 4:
                loposition = position
            #mark end


            #print (position,len(position))

        # main algorithm ends here
        #mark edit 23 apr 2017
        cv2.line(region,(240,0),(240,60),(255,0,0),5)
        centercal,centershift = carang.carcenterpos(carang.choselane(position))
        cv2.line(region,(centercal,0),(centercal,60),(0,0,255),5)
        print (centershift)
        arduino.send(centershift)




        # display the size of the queue on the frame
        cv2.putText(gray, "Queue Size: {}".format(fvs.Q.qsize()), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # show the frame and update the FPS counter
        H = cv2.cvtColor(perspective, cv2.COLOR_BGR2HSV)[:,:,0]
        #cv2.imshow("pathAvaliable", pathAvaliable)
        cv2.imshow("region",region)
        cv2.imshow("real", gray)
        cv2.imshow("Perspective", perspective)
        if cv2.waitKey(1) == ord('q'):
            break
        #cv2.waitKey(0)
    else:
        pass
    time.sleep(0.05)
    fps.update()
# stop the timer and display FPS information

fps.stop()
print ("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print ("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
fvs.stop()
