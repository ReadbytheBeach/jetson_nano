# Python
import cv2
print(cv2.__version__)
flip=2  # change camera play direction
dispW = 640
dispH = 480

camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH)) # screen width
dispH = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) # screen height
print(f'window size = {dispW}Width x {dispH}Height')

BW = int(.05 * dispW) # rectangle width
BH = int(.10 * dispH) # rectangle height 
posX = 10 # rectangle X-position start point
posY = 270 # rectangle Y-position start point
dx = 2 # each x move step
dy = 2 # each y move step


while True:
    ret, frame = cam.read()
    cv2.moveWindow('nanoCam',0,0)
    frame = cv2.rectangle(frame, (posX, posY),(posX+BW, posY+BH),(255,posX,posY),-1)
    cv2.imshow('nanoCam', frame)

    posX += dx
    posY += dy

    if posX <= 0: # left boundary
        dx = dx*(-1) # change direction
    if posX + BW >= dispW: # right boundary
        dx = dx*(-1)
    if posY <= 0:  # upper boundary
        dy = dy*(-1)
    if posY + BH >= dispH: # bottom boundary
        dy = dy*(-1)   

    if cv2.waitKey(5)==ord('q'):
        break


cam.release()
cv2.destroyAllWindows()