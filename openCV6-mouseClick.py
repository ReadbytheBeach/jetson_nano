# Python
import cv2
import numpy as np

print(cv2.__version__)
evt = -1
coord = []
img = np.zeros((250, 250, 3), np.uint8) # use numpy create a matrix, type=uint8

def click(event, x, y, flags, params):
    global pnt
    global evt
    # show the left click BGR number in 'nanoCam' window, 
    # and collect all the click point BGR into a 2d-array coord
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Mouse Event was: ', event)
        print(x,',',y) 
        pnt = (x,y)
        coord.append(pnt)
        print(coord)
        # evt = event
    
    # show the right click BGR number in 'rClickColor' window
    if event == cv2.EVENT_RBUTTONDOWN:  
        print(x,y)
        # a frame is a 2-dimension matrix: row & column, y is row, x is column
        # a frame pixel with B-G-R tuple color
        blue = frame[y,x,0] # one pixel has B-G-R tuple, tuple[0] = Blue
        green= frame[y,x,1]
        red  = frame[y,x,2]
        print(blue, green, red)
        colorString = 'b: '+str(blue)+' ' +'g: '+ str(green) + ' '+ 'r: ' + str(red)
        img[:] = [blue,green,red]   # img a np array, output every pixel out
        fnt = cv2.FONT_HERSHEY_PLAIN
        r = 255-int(red) # reverse the color
        g = 255-int(green)
        b = 255-int(blue)
        tp = (b,g,r)  # the color which will show in cv2.putText
        cv2.putText(img,colorString,(10,25),(fnt),1,tp,2)
        cv2.imshow('rClickColor',img)
        
dispW=640
dispH=480
flip=2  # change camera play direction
cv2.namedWindow('nanoCam')
cv2.setMouseCallback('nanoCam',click)  # listen to the mouse special action: click. check the click is right click or left click
#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    for pnts in coord:
        cv2.circle(frame,pnts,5,(0,0,255),-1)  # at pnts position create a circle
        font = cv2.FONT_HERSHEY_PLAIN
        myStr=str(pnts)
        cv2.putText(frame,myStr,pnts,font,1.5,(255,0,0),2)
    # if evt == 1: # mouse click trigger to paint a circle
    #     cv2.circle(frame, pnt,5,(0,0,255),-1)
    #     font = cv2.FONT_HERSHEY_PLAIN
    #     myStr=str(pnt)
    #     cv2.putText(frame,myStr,pnt,font,1.5,(255,0,0),2)
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCame',0,0)

    keyEvent = cv2.waitKey(1)
    if keyEvent ==ord('q'):
        break
    if keyEvent ==ord('c'):
        coord=[]  # clear all the coord values, then screen without any circles

cam.release()
cv2.destroyAllWindows()