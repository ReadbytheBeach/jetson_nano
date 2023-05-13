# Python
import cv2
print(cv2.__version__)
dispW=640   # Frame size(points number) impact video play speed = computer speed 
dispH=480
flip=0
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet) # getting the video from camera
# cam= cv2.VideoCapture('videos/myCam1.avi') # getting the video from avi

# capture the video
# framerate=21, same as 'camSet' frame-rate 
# also set the same size with 'camSet', for example set (dispW, dispH)
# XVID means open quote XV ID
outVid = cv2.VideoWriter('videos/myCam2.avi', cv2.VideoWriter_fourcc(*'XVID'),21,(dispW,dispH))

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCame',0,0)

    # write the frame
    outVid.write(frame)

    if cv2.waitKey(5)==ord('q'):
        break
cam.release()
outVid.release()
cv2.destroyAllWindows()