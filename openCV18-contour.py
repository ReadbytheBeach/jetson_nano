import cv2
print(cv2.__version__)
import numpy as np


dispW=320
dispH=240
flip=2  # change camera play direction
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam= cv2.VideoCapture(camSet)

def nothing(x):
    pass

cv2.namedWindow('Trackbars')
cv2.moveWindow('Trackbars',3*dispW+10,0)

# cv2.createTrackbar(name,Trackbars,default,max value, function)
# HRV, Hue:0~179, Saturation:0~255, Value:0~255
cv2.createTrackbar('hue_lower','Trackbars',177,179, nothing)  
cv2.createTrackbar('hue_high','Trackbars',179,179, nothing) 

# create new Trackbars for special color
cv2.createTrackbar('hue_lower2','Trackbars',0,179, nothing)  
cv2.createTrackbar('hue_high2','Trackbars',1,179, nothing)

cv2.createTrackbar('saturation_lower','Trackbars',100,255, nothing) 
cv2.createTrackbar('saturation_high','Trackbars',266,255, nothing) 
cv2.createTrackbar('value_lower','Trackbars',100,255, nothing) 
cv2.createTrackbar('value_high','Trackbars',255,255, nothing) 


 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    # frame= cv2.imread('smarties.png')  # choose use real frame or just and png 


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
    cv2.moveWindow('FGMaskComp',0,dispH+200)

    # contours is array, each contours is an array of interest objectq
    # change color to show the different RGB interest object
    # cv2.findContour: return 2 parameters, contours, hierachy
    # cv3.findContour: return 3 parameters, image, contours, hierachy     # RETR_EXTERNAl: return external contour
    # cv2.CHAIN_APPROX_SIMPLE: only keep the final coodr, remove the horizontal,vertical,cross elements. For example, rectrangel only keep 4 corners

    contours,_ = cv2.findContours(FGMaskComp,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # show the biggest one
    # reverse = TRUE, means sorted from the biggest one
    contours = sorted(contours,key = lambda x:cv2.contourArea(x), reverse=True)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # give the left-up corner point, and the width & height to descript a rectangle
        (x,y,w,h) = cv2.boundingRect(cnt)
        if area >= 50: # 50 means 50 pixels:
            # cv2.drawContours(frame,[cnt],0,(255,0,0),2)
            cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),3)
    
    # cv2.drawContours(frame,draw contours, -1=all contours,BGR color, font)
    # 0 = show the biggest contour


    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

    if cv2.waitKey(1)==ord('q'):
          break
cam.release()
cv2.destroyAllWindows()