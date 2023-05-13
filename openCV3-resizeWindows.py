# Python
import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=0
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
# cam=cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FRAME_WIDTH,dispW)  # set webCam resize
# cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dispH)
while True:
    ret, frame = cam.read()
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',700,0)

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # change color

    nanoSmall = cv2.resize(frame,(320,240))    # change size
    graySmall = cv2.resize(gray,(320,240)) 

    cv2.imshow('BlackWhite', graySmall) # show window
    cv2.imshow('NanoSmall',nanoSmall)
    cv2.imshow('BlackWhite2', graySmall) 
    cv2.imshow('NanoSmall2',nanoSmall)

    cv2.moveWindow('BlackWhite',0,265) # change location
    cv2.moveWindow('NanoSmall',0,0) 
    cv2.moveWindow('BlackWhite2',360,265) # change location
    cv2.moveWindow('NanoSmall2',360,0) 

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()