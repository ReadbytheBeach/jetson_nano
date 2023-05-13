# Python
import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=0 # change the direction
#Uncomment These next Two Line for Pi Camera

def nothing(x):
    pass

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
cv2.namedWindow('nanoCam')
cv2.createTrackbar('myTrackBar_xVal', 'nanoCam', 25,dispW, nothing)  # callback function = nothing
cv2.createTrackbar('myTrackBar_yVal', 'nanoCam', 25,dispH, nothing)  # callback function = nothing
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()

    xVal = cv2.getTrackbarPos('myTrackBar_xVal','nanoCam')
    yVal = cv2.getTrackbarPos('myTrackBar_yVal','nanoCam')
    cv2.circle(frame,(xVal,yVal),5,(255,0,0),-1)  # -1 means solid circle

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCame',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()