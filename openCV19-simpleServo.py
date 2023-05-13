
from adafruit_servokit import ServoKit
import time
import cv2

myKit = ServoKit(channels=16)
myKit.servo[1].angle =180
time.sleep(1)
myKit.servo[0].angle =90

while True:
    for i in range(0,180,1):
        myKit.servo[0].angle =i
        time.sleep(.01)
    for j in range(180,0,-1):
        myKit.servo[0].angle =j
        time.sleep(.01)
    if cv2.waitKey(1)==ord('q'):
        break
