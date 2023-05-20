import cv2

print(cv2.__version__)
dispW=960
dispH=720
flip=0  # change camera play direction
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam=cv2.VideoCapture(0)

# step1: load the algorithm 
face_cascade = cv2.CascadeClassifier("/home/xj/Desktop/pyPro/cascade/face_alt2.xml")
eye_cascade = cv2.CascadeClassifier("/home/xj/Desktop/pyPro/cascade/eye.xml")

while True:
    ret, frame = cam.read()
    #step2: pre-deal with the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #step3: in gray-frame to find a face. store the result in 'faces' object
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #step4: draw the result date in original frame
    for (x,y,w,h) in faces:
        print('face x,y,w,h: ',x,y,w,h)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        # in face area to find an eye
        roi_gray = gray[y:y+h,x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        Roi_frame = frame[y:y+h,x:x+w]
        for (xEye,yEye,wEye,hEye) in eyes:
            print('eye x1,y1,w1,h1: ',xEye,yEye,wEye,hEye)
            cv2.circle(Roi_frame, (int(xEye+wEye/2),int(yEye+hEye/2)),12,(255,0,0),-1)

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()