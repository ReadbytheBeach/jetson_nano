import cv2
import numpy as np
print(cv2.__version__)
dispW=480
dispH=360
flip=2  # change camera play direction
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
blank = np.zeros([360,480,1],np.uint8)  # 1 means grayscale


while True:
    ret, frame = cam.read()
    # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # print('frame.shape= ', frame.shape)
    # print('gray.shape= ',gray.shape)
    # print('gray.size= ', gray.size)
    # print('frame.size= ', frame.size)
    # print(frame[50,45,1])

    # b= cv2.split(frame)[0]
    # g= cv2.split(frame)[1]
    # r= cv2.split(frame)[2]
    b,g,r = cv2.split(frame)
    
    # cv2.merge(B,G,R): BGR channel merge function
    blue_channel = cv2.merge((b,blank,blank))
    green_channel = cv2.merge((blank,g,blank))
    red_channel = cv2.merge((blank,blank,r))

    # make blue more blue
    b[:] = b[:]*1.2 
    # r[:] = r[:]*1.3

    merge_channle = cv2.merge((b,g,r))
    # merge_channle = cv2.merge((g,r,b))

    cv2.imshow('blue',blue_channel)
    cv2.moveWindow('blue',dispW+10,0) 
    cv2.imshow('green',green_channel)
    cv2.moveWindow('green',0,dispH+10)
    cv2.imshow('red',red_channel)
    cv2.moveWindow('red',dispW+10,dispH+10)

    cv2.imshow('Merge',merge_channle)
    cv2.moveWindow('Merge',2*(dispW)+10,0)
    cv2.imshow('nanoCam',frame) # will show (480,640,3), 3 means: R-G-B three channels.
    cv2.moveWindow('nanoCam',0,0)

    # cv2.imshow('blank', blank)
    # cv2.moveWindow('blank', 1200,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()