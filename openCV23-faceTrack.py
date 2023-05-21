import cv2
print(cv2.__version__)
import numpy as np
import time
from adafruit_servokit import ServoKit
kit=ServoKit(channels=16)

# servo initial degrees: pan means 'X'-direction and tilt means 'Y'-direction.
pan_init = 90
tilt_init = 135
# servo move degrees
pan = 90
tilt = 135

kit.servo[0].angle = pan_init
time.sleep(.5)
kit.servo[1].angle = tilt_init
time.sleep(.5)


print(cv2.__version__)

# screen size
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
screen_width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
screen_height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
print('screen_width: ',screen_width, 'screen_height: ',screen_height)

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
                
        # center of the face_rectangle, h means object height, w means object width
        objX_cent = x + int(w/2)
        objY_cent = y + int(h/2)
        
        # mofidy distance = the offset between the "screen-center-position" and the "face_rectangle-center-position".
        # screen_width/2 means the screen-center-position pixel-X, and screen_height/2 means the screen-center-position pixel-Y.
        # so errorPan means offset move in 'X'-direction, errorTilt means move in 'Y'-direction.
        # define servo move left is minus, servo move right is plus, 
        errorPan = objX_cent - int(screen_width/2)
        errorTilt = objY_cent - int(screen_height/2)

        # move slow or quick base on errorPan/errorTilt offset value
        # don't want servo to move too fast -- means over shoot, than adjust(debounce) again and again
        if abs(errorPan) > 15:            
            pan = pan - int(errorPan/50)  #  errorPan/n means change(slow) the servo move by n-times
        if abs(errorTilt) > 15:
            tilt = tilt - int(errorTilt/50)

        # if offset value is small, servo can move quickly
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
            print('pan out of left-range')
        if pan < 0:
            pan = 0
            print('pan out of right-range')
        if tilt > 180:
            tilt = 180
            print('tilt out of up-range')
        if tilt < 0:
            tilt = 0    
            print('tilt out of down-range')  

        kit.servo[0].angle = pan
        kit.servo[1].angle = tilt

        # in face area to find eyes
        roi_gray = gray[y:y+h,x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        # use the original frame to display the found eye_circles
        Roi_frame = frame[y:y+h,x:x+w]
        for (xEye,yEye,wEye,hEye) in eyes:
            print('eye x1,y1,w1,h1: ',xEye,yEye,wEye,hEye)
            # use the original frame to display the found eye_circles
            cv2.circle(Roi_frame, (int(xEye+wEye/2),int(yEye+hEye/2)),12,(255,0,0),-1)

        # if only want to focus the first face, just put the 'break' here to jump out the cycle
        break

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        time.sleep(1)
        kit.servo[0].angle = pan_init
        time.sleep(1)
        kit.servo[1].angle = tilt_init
        break
cam.release()
cv2.destroyAllWindows()