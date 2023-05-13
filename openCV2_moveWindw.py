import cv2
print(cv2.__version__)
dispW = 640
dispH = 480
flip = 2
# camSet = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=1848, format=NV12, framerate=55/1 ! nvvidconv flit-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format = BRGx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# PiCam=cv2.VideoCapture(camSet)  # this line for raspi camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
WebCam = cv2.VideoCapture(0)  # this line for other cameras
while True:
    ret, frame = WebCam.read()

    cv2.imshow('WebCam', frame)
    cv2.moveWindow('webCam',0,0)
    

    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('grayVideo',gray)
    cv2.moveWindow('grayVideo',0,500)
    if cv2.waitKey(1) ==ord('e'):
        break

cam.release()
cv2.destroyAllWindows()
