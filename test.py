#!/usr/bin/env python
# http://www.pyimagesearch.com/2017/02/06/faster-video-file-fps-with-cv2-videocapture-and-opencv/

# import the necessary packages
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2

import utility as ut
# import os


fvs = FileVideoStream("videos/GOPR0205_2.avi").start()

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

        perspective = ut.inversePerspective(frame)

        #ROI 1
        ROI1 = ut.selectROI(perspective, [0, 1], [0.5, 0.55])
        thresh1 = ut.threshold_2(ROI1)
        pos1 = ut.detect(thresh1)
        for x, y in pos1:
            cv2.circle(ROI1, (x, y), 30, (0, 255, 0), 2)

        #ROI 2
        ROI2 = ut.selectROI(perspective, [0, 1], [0.3, 0.35])
        thresh2 = ut.threshold_2(ROI2)
        pos2 = ut.detect(thresh2)
        for x, y in pos2:
            cv2.circle(ROI2, (x, y), 30, (0, 255, 0), 2)

        # display the size of the queue on the frame
        cv2.putText(frame, "Queue Size: {}".format(fvs.Q.qsize()), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # show the frame and update the FPS counter
        cv2.imshow("Frame", gray)
        cv2.imshow("Perspective", perspective)

        if cv2.waitKey(1) == ord('q'):
            break
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
