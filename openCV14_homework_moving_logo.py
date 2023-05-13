import cv2
print(cv2.__version__)

def nothing():
    pass

cv2.namedWindow('Blended')
cv2.createTrackbar('BlendedValue','Blended',50,100,nothing)

dispW=320
dispH=240
flip=2  # change camera play direction

# read the image and resize
pyLogo = cv2.imread('pl.jpg')
pyLogo = cv2.resize(pyLogo,(36,48))

BW = 36 # rectangle width: same as pyLogo resize width
BH = 48 # rectangle height: same as pyLogo resize height
posX = 100 # rectangle X-position start point
posY = 100 # rectangle Y-position start point
dx = 2 # each x move step
dy = 2 # each y move step

#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)

# show pylogo
cv2.imshow('py Logo', pyLogo)
cv2.moveWindow('py Logo', 410,0)

# change the frame colur to Gray
pyLogoGray = cv2.cvtColor(pyLogo, cv2.COLOR_BGR2GRAY)
cv2.imshow('py Logo Gray',pyLogoGray)
cv2.moveWindow('py Logo Gray', 450,0)

# background mask: separate by black or white
# cv2.threshold(img, thresh, maxVal, cv2.xxx), maxVal means: if value > mavVal should be set to value
_, BGMask = cv2.threshold(pyLogoGray, 225, 255, cv2.THRESH_BINARY)  # cv2.THRESH_BINARY, means black or white
cv2.imshow('BG Mask', BGMask)
cv2.moveWindow('BG Mask', 490,0)

# oppsite background mask, use cv2.bitwise_not(background mask)
FGMask = cv2.bitwise_not(BGMask)    # opposite the BGMask --> white in symbol, black in background
cv2.imshow('FG Mask', FGMask)
cv2.moveWindow('FG Mask', 530, 0)

# foreground mask: white AND symbol = symbol, black with everything = black
FG = cv2.bitwise_and(pyLogo,pyLogo,mask=FGMask) 
cv2.imshow('FG', FG)
cv2.moveWindow('FG',570,0)



#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()

    # create a new move frame, which should be same size as pyLogo resize 
    frame_move = frame[posY:posY+BH,posX:posX+BW]
  
    # create the background img: BGMask AND Frame(you can defined the size)
    # cv2.bitwise_and(src, dest, mask=xxx)
    BG_img = cv2.bitwise_and(frame_move,frame_move,mask = BGMask)
    cv2.imshow('BG_img', BG_img)
    cv2.moveWindow('BG_img',610,0)

    # create the foreground img: backgroud_image add foreground, saturate = black + color = color
    FG_img = cv2.add(BG_img, FG)
    cv2.imshow('FG_img',FG_img)
    cv2.moveWindow('FG_img', 650,0)

    # embeded the FG_img into Frame, means replace the Frame area by FG_img
    frame[posY:posY+BH,posX:posX+BW]=FG_img

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)

    # move the window before next cycle
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

    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()