# Python
import cv2
import numpy as np
print(cv2.__version__)
dispW=480
dispH=360
flip=0  # change camera play direction
img1 = np.zeros((360,480,1),np.uint8) # row=480, column=640, grayscale=1, type=np.uint8
img1[0:360,0:240]=[255] # 255 means color=white, white means 1, black means 0
img2 = np.zeros((360,480,1),np.uint8)
img2[140:220,200:280]=[255]
bitAnd = cv2.bitwise_and(img1,img2)
bitOr = cv2.bitwise_or(img1,img2)
bitXor = cv2.bitwise_xor(img1,img2)
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()

    cv2.imshow('img1', img1)
    cv2.moveWindow('img1', 0,370)
    cv2.imshow('img2', img2)
    cv2.moveWindow('img2', 490,0)
    cv2.imshow('AND', bitAnd)
    cv2.moveWindow('AND', 490,370)
    cv2.imshow('OR', bitOr)
    cv2.moveWindow('OR', 970,0)
    cv2.imshow('Xor', bitXor)
    cv2.moveWindow('Xor', 490,370)
    frame = cv2.bitwise_and(frame, frame,mask = bitXor)
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()