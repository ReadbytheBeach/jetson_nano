# Python
import cv2
print(cv2.__version__)
dispW=640
dispH=480
flip=0  # change camera play direction
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()
    # region of interests
    # .copy(): create a new one, not just index the old
    roi = frame[50:250,200:400].copy()
    # print('roi= ', roi)
    roiGray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    roiGray = cv2.cvtColor(roiGray,cv2.COLOR_GRAY2BGR) # from gray picture to set the ROI in original frame
    frame[50:250,200:400]=roiGray   # change the frame color to white in area [50:250,200:400]

    cv2.imshow('ROI',roi)
    cv2.imshow('GRAY',roiGray)
    cv2.imshow('nanoCam',frame)

    cv2.moveWindow('nanoCam',0,0)
    cv2.moveWindow('ROI',720,0)
    cv2.moveWindow('GRAY',720,250)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()