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

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',700,460)
# hue setup
# cv2.createTrackbar('hueLower', 'Trackbars',59,179,nothing)
# cv2.createTrackbar('hueUpper', 'Trackbars',101,179,nothing)
# following default value set for 'blue' color
cv2.createTrackbar('hueLower', 'Trackbars',96,179,nothing)
cv2.createTrackbar('hueUpper', 'Trackbars',120,179,nothing)

# hue2Lower and hueUpper only use for detection red color
cv2.createTrackbar('hue2Lower', 'Trackbars',50,179,nothing)
cv2.createTrackbar('hue2Upper', 'Trackbars',0,179,nothing)

# saturation setup
cv2.createTrackbar('satLow', 'Trackbars',100,255,nothing)
cv2.createTrackbar('satHigh', 'Trackbars',255,255,nothing)

# value(brightness) setup
cv2.createTrackbar('valLow','Trackbars',100,255,nothing)
cv2.createTrackbar('valHigh','Trackbars',255,255,nothing)


dispW=640
dispH=480
flip=0
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

while True:
    ret, frame = cam.read()
    #frame=cv2.imread('smarties.png')

    # transfer color area
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hueLow=cv2.getTrackbarPos('hueLower', 'Trackbars')
    hueUp=cv2.getTrackbarPos('hueUpper', 'Trackbars')

    hue2Low=cv2.getTrackbarPos('hue2Lower', 'Trackbars')
    hue2Up=cv2.getTrackbarPos('hue2Upper', 'Trackbars')

    Ls=cv2.getTrackbarPos('satLow', 'Trackbars')
    Us=cv2.getTrackbarPos('satHigh', 'Trackbars')

    Lv=cv2.getTrackbarPos('valLow', 'Trackbars')
    Uv=cv2.getTrackbarPos('valHigh', 'Trackbars')

    l_b=np.array([hueLow,Ls,Lv])
    u_b=np.array([hueUp,Us,Uv])

    l_b2=np.array([hue2Low,Ls,Lv])
    u_b2=np.array([hue2Up,Us,Uv])

    # select the area, if not been choosen: was transferred to '0'
    # cv2.inRange(pixel, lowerLimit, upperLimit), pixel transfer to binaray solution, in range: white, out of range: black
    FGmask=cv2.inRange(hsv,l_b,u_b)
    FGmask2=cv2.inRange(hsv,l_b2,u_b2)
    # because red has two area, so need use "AND" to combine two area
    FGmaskComp=cv2.add(FGmask,FGmask2)
    cv2.imshow('FGmaskComp',FGmaskComp)
    cv2.moveWindow('FGmaskComp',700,0)

    # find the contours
    contours,_=cv2.findContours(FGmaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
    for cnt in contours:
        # find the max one 
        area=cv2.contourArea(cnt)
        # find the left-up point and width & height
        (x,y,w,h)=cv2.boundingRect(cnt)
        if area>=50: # bigger than 50 pixels
            # draw the rectangle by using cv2.drawContours(frame,[cnt],0,(255,0,0),3)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)

            # center of the rectangle, h means object height, w means object width
            objX = x + w/2
            objY = y + h/2
            # mofidy distance = the offset of the "screen center position" and the "rectangle center position" 
            # width/2 means the window center pixel-X, height/2 means the window center pixel-Y
            errorPan = objX - width/2
            errorTilt = objY - height/2
            # move slow or quick base on errorPan/errorTilt offset value
            
            # move quick strategy, if Pixels <= 15, not change
            if abs(errorPan) > 15:
                pan = pan - errorPan/75  # 1 degree = n pixeles, n can be change like a threshold
            if abs(errorTilt) > 15:
                tilt = tilt - errorTilt/75

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