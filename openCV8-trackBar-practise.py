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
cv2.createTrackbar('xVal', 'nanoCam', 1,dispW, nothing)  # callback function = nothing
cv2.createTrackbar('yVal', 'nanoCam', 1,dispH, nothing)  # callback function = nothing
cv2.createTrackbar('width', 'nanoCam', 0,dispW, nothing)  # callback function = nothing
cv2.createTrackbar('height', 'nanoCam', 0,dispH, nothing)  # callback function = nothing

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()

    xVal = cv2.getTrackbarPos('xVal','nanoCam')
    yVal = cv2.getTrackbarPos('yVal','nanoCam')
    wVal = cv2.getTrackbarPos('width','nanoCam')
    hVal = cv2.getTrackbarPos('height','nanoCam')
    # create a circle
    # cv2.circle(frame,(xVal,yVal),5,(255,0,0),-1)  # -1 means solid circle
    # create a rectangle
    # (xVal+32,yVal+24): means original size; (xVal+32 +'widht',yVal+24 +'height'): means change the rectangle
    frame = cv2.rectangle(frame,(xVal,yVal),(xVal+8 +wVal,yVal+6 +hVal),(0,255,0),5)  # (startPoint, stopPoint, color, boldSize)

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCame',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()