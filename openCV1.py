import cv2
print(cv2.__version__)
dispW = 320
dispH = 240
flip = 2
camSet = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3264, height=1848, format=NV12, framerate=55/1 ! nvvidconv flit-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format = BRGx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)  # this line for raspi camera
# cam = cv2.VideoCapture(0)  # this line for other cameras
while True:
    ret, frame = cam.read()
    cv2.imshow('piCam', frame)
    if cv2.waitKey(1) ==ord('e'):
        break

cam.release()
cv2.destroyAllWindows()
