import cv2
import time
import os
import datetime
import imutils
cap = cv2.VideoCapture(0)

cap.set(3,640)
cap.set(4,480)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

firstFrame = None

record = False
fctr = 0
while(True):
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    #cv2.imwrite("im1.jpg", gray)
   
    # if the first frame is None, initialize it
    if firstFrame is None:
    	firstFrame = gray
    	continue

    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1] 

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
        if cv2.contourArea(c) > 1000:
            # compute the bounding box for the contour, draw it on the frame,
	    # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            fctr = 0
            
            if record is False:
                record = True
                ts = datetime.datetime.now()
                print("writing out", ts)
                out = cv2.VideoWriter(os.path.join('./backup','out{dt}.mp4'.format(dt=ts)), fourcc, 20.0, (640,480))

    if fctr < 50 and out is not None:
        out.write(frame)
    elif out is not None and out.isOpened():
        print("closing vid")
        out.release()
        record = False
    fctr +=1

cap.release()
out.release()
