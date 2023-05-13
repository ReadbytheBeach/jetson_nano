import cv2
print(cv2.__version__)
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',0,0)

# cv2.createTrackbar(name,Trackbars,default,max value, function)
# HRV, Hue:0~179, Saturation:0~255, Value:0~255
cv2.createTrackbar('hue_lower','Trackbars',50,179, nothing)  
cv2.createTrackbar('hue_high','Trackbars',179,179, nothing) 

# create new Trackbars for special color
cv2.createTrackbar('hue_lower2','Trackbars',50,179, nothing)  
cv2.createTrackbar('hue_high2','Trackbars',179,179, nothing)

cv2.createTrackbar('saturation_lower','Trackbars',100,255, nothing) 
cv2.createTrackbar('saturation_high','Trackbars',266,255, nothing) 
cv2.createTrackbar('value_lower','Trackbars',100,255, nothing) 
cv2.createTrackbar('value_high','Trackbars',255,255, nothing) 


dispW=640
dispH=480
flip=0  # change camera play direction
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    # frame= cv2.imread('smarties.png')
    # cv2.imshow('nanoCam',frame)
    # cv2.moveWindow('nanoCam',0,0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # cv2.getTrackbarPos(name, in where)
    hue_lower = cv2.getTrackbarPos('hue_lower','Trackbars')
    hue_up = cv2.getTrackbarPos('hue_high','Trackbars')

    hue2_lower = cv2.getTrackbarPos('hue_lower2','Trackbars')
    hue2_up = cv2.getTrackbarPos('hue_high2','Trackbars')

    sat_lower = cv2.getTrackbarPos('saturation_lower','Trackbars')
    sat_up = cv2.getTrackbarPos('saturation_high','Trackbars')

    val_lower = cv2.getTrackbarPos('value_lower','Trackbars')
    val_up = cv2.getTrackbarPos('value_high','Trackbars') 


    # create the bounds for lower and higher
    l_b = np.array([hue_lower,sat_lower,val_lower])
    u_b = np.array([hue_up,sat_up,val_up])

    l_b2 = np.array([hue2_lower,sat_lower,val_lower])
    u_b2 = np.array([hue2_up,sat_up,val_up])

    # create foreground mask
    # cv2.inRange(frame, min value, max value), 
    # if value < min value or value > max value, then the pixel will turn in black, others will turn in white.
    FGMask = cv2.inRange(hsv, l_b,u_b)
    # create FGMask2
    FGMask2 = cv2.inRange(hsv,l_b2,u_b2)
    FGMaskComp=cv2.add(FGMask,FGMask2)
    cv2.imshow('FGMaskComp',FGMaskComp)
    cv2.moveWindow('FGMaskComp',0,410)

    # create foreground
    # cv2.bitwise_and(src,dest,mask)
    FG = cv2.bitwise_and(frame,frame,mask=FGMaskComp)
    cv2.imshow('FG',FG)
    cv2.moveWindow('FG',480,0)

    # create background mask
    # cv2.bitwise_not is an oppsite function 
    bgMask = cv2.bitwise_not(FGMaskComp)
    cv2.imshow('BGMask',bgMask)
    cv2.moveWindow('BGMask',480, 410)

    # create background
    # follow step is not make the color, 
    # cv2.COLOR_GRAY2BGR just make the matrix the right size    BG = cv2.cvtColor(bgMask,cv2.COLOR_GRAY2BGR)
    # before is just with grayscale value, after GRAY2BGR each pixel with B-G-R three values, then we can work with it
    BG = cv2.cvtColor(bgMask,cv2.COLOR_GRAY2BGR)

    final = cv2.add(FG,BG)
    cv2.imshow('Final',final)
    cv2.moveWindow('Final',900,0)
    
    if cv2.waitKey(1)==ord('q'):
          break
cam.release()
cv2.destroyAllWindows()