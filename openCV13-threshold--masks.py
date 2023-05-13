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
cvLogo = cv2.imread('cv.jpg')
cvLogo = cv2.resize(cvLogo,(320,240))

# change the frame colur to Gray
cvLogoGray = cv2.cvtColor(cvLogo, cv2.COLOR_BGR2GRAY)
cv2.imshow('cv Logo Gray',cvLogoGray)
cv2.moveWindow('cv Logo Gray', 0,285)

# background mask: separate by black or white
# cv2.threshold(img, thresh, maxVal, cv2.xxx), maxVal means: if value > mavVal should be set to value
_, BGMask = cv2.threshold(cvLogoGray, 225, 255, cv2.THRESH_BINARY)  # cv2.THRESH_BINARY, means black or white
cv2.imshow('BG Mask', BGMask)
cv2.moveWindow('BG Mask', 385,0)

# foreground mask
FGMask = cv2.bitwise_not(BGMask)    # opposite the BGMask --> white in symbol, black in background
cv2.imshow('FG Mask', FGMask)
cv2.moveWindow('FG Mask', 385, 285)
FG = cv2.bitwise_and(cvLogo,cvLogo,mask=FGMask) # white AND symbol = symbol, black with everything = black
cv2.imshow('FG', FG)
cv2.moveWindow('FG',703,285)

#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)
 
#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
# cam=cv2.VideoCapture(0)
while True:
    ret, frame = cam.read()

    # create the background img
    # cv2.bitwise_and(src, dest, mask=xxx)
    BG = cv2.bitwise_and(frame,frame,mask=BGMask)  # white vs me will be me, black vs me will be black, that's cv2.THRESH_BINARY
    cv2.imshow('BG',BG)
    cv2.moveWindow('BG',703,0)

    # add the background with foreground
    # cv2.add(img1, img2): add two images,  two pic size should be same. 
    # If pixels value > 255, than count as 255
    # BG.pixel_value + FG.pixel_value (saturate), for example 15 + 255 = 255
    compImage = cv2.add(BG,FG)  # add black to everything = everything
    cv2.imshow('compImage',compImage)
    cv2.moveWindow('compImage', 1017,0)

    # get the value of Trackbar:"BlendedValue"
    BV = cv2.getTrackbarPos('BlendedValue','Blended')/100  # put the value between 1 ~ 100
    BV2 = 1- BV 
    # create the watermask
    blended = cv2.addWeighted(frame, BV,cvLogo,BV2,0)
    cv2.imshow('Blended',blended)
    cv2.moveWindow('Blended',1017,285)

    FG2=cv2.bitwise_and(blended,blended,mask=FGMask)
    cv2.imshow('FG Blended',FG2)
    cv2.moveWindow('FG Blended',1324,0)

    compFinal = cv2.add(FG2,BG)
    cv2.imshow('comFinal', compFinal)
    cv2.moveWindow('comFinal',1324,285)

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()