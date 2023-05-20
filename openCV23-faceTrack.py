import cv2
print(cv2.__version__)
import numpy as np
import time
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)

pan=90
time.sleep(.5)
tilt=135
time.sleep(.5)

kit.servo[0].angle = pan
kit.servo[1].angle = tilt

print(cv2.__version__)
dispW=640
dispH=480
flip=0  # change camera play direction
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)

# get the webCamera size --which we set the window size before
width=cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('width: ',width, 'height: ',height)

# step1: load the algorithm 
face_cascade = cv2.CascadeClassifier("/home/xj/Desktop/pyPro/cascade/face_alt2.xml")
eye_cascade = cv2.CascadeClassifier("/home/xj/Desktop/pyPro/cascade/eye.xml")

while True:
    ret, frame = cam.read()
    #step2: pre-deal with the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #step3: in gray-frame to find a face. store the result in 'faces' object
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #step4: draw the result date in original frame
    for (x,y,w,h) in faces:
        print('face x,y,w,h: ',x,y,w,h)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        # in face area to find an eye
        roi_gray = gray[y:y+h,x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        Roi_frame = frame[y:y+h,x:x+w]
        for (xEye,yEye,wEye,hEye) in eyes:
            print('eye x1,y1,w1,h1: ',xEye,yEye,wEye,hEye)
            cv2.circle(Roi_frame, (int(xEye+wEye/2),int(yEye+hEye/2)),12,(255,0,0),-1)
        
        # center of the rectangle, h means object height, w means object width
        objX = x + int(w/2)
        objY = y + int(h/2)
        
        # mofidy distance = the offset of the "screen center position" and the "rectangle center position" 
        # width/2 means the window center pixel-X, height/2 means the window center pixel-Y
        errorPan = objX - int(width/2)
        errorTilt = objY - int(height/2)
        # move slow or quick base on errorPan/errorTilt offset value
        
        # move quick strategy, if Pixels <= 15, not change
        if abs(errorPan) > 15:
            pan = pan - int(errorPan/50)  # 1 degree = n pixeles, n can be change like a threshold
        if abs(errorTilt) > 15:
            tilt = tilt - int(errorTilt/50)

        # move slow strategy
        if errorPan > 0:
            pan = pan - .2 # 0.2 means change the degree to pixel by divide 5
        if errorPan < 0:
            pan = pan + .2
        if errorTilt > 0:
            tilt = tilt - .2
        if errorTilt < 0:
            tilt = tilt + .2

        # control the servor not out of range [0,180]
        if pan > 180:
            pan = 180
            print('pan out of left range')
        if pan < 0:
            pan = 0
            print('pan out of right range')
        if tilt > 180:
            tilt = 180
            print('tilt out of up range')
        if tilt < 0:
            tilt = 0    
            print('tilt out of down range')  

        kit.servo[0].angle = pan
        kit.servo[1].angle = tilt

        # if only want to focus the max rectangle, just put the break here, not consider 2nd biggest retangle
        break

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()