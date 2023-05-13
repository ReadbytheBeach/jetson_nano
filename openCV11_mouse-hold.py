import cv2
print(cv2.__version__)

goFlag = 0
def mouse_click(event,x,y,flags,params):
    global x1,y1,x2,y2
    global goFlag
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        goFlag = 0  # click the button down, goFlag set to zero
        
    if event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        goFlag = 1

cv2.namedWindow('nanoCam')
cv2.setMouseCallback('nanoCam',mouse_click)  # listen to the mouse special action: click. check the click is right click or left click
dispW=640
dispH=480
flip=2  # change camera play direction     
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()    
    cv2.imshow('nanoCam',frame)
    
    if goFlag == 1: # means button down
        frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),3)
        roi_frame = frame[y1:y2,x1:x2]
        cv2.imshow('COPY ROI',roi_frame)
        cv2.moveWindow('COPY ROI',705,0)

    cv2.moveWindow('nanoCame',0,0)

    keyEvent = cv2.waitKey(1)
    if keyEvent ==ord('q'):
        break
    if keyEvent ==ord('c'):
        coord=[]  # clear all the coord values, then screen without any circles

cam.release()
cv2.destroyAllWindows()
