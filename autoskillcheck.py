import numpy as np 
from PIL import ImageGrab, Image
import cv2
from pynput.keyboard import Key, Controller
import time
from mss import mss

sct = mss();
keyboard = Controller()
mon = {'top' : 440, 'left' : 810, 'width' : 250, 'height' : 250}
lastWhiteCounts = [0,0,0,0,0]
skillCheck = False

def processFrame(frame):
    global skillCheck
    processedFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #processedFrame = cv2.Canny(processedFrame, threshold1=20, threshold2=300)
    ret, thresh = cv2.threshold(processedFrame, 252, 255, cv2.THRESH_BINARY)
    processedFrame[thresh != 255] = 0
    greatSkillcheckPx = np.sum(thresh == 255)
    lastWhiteCounts[0] = lastWhiteCounts[1]
    lastWhiteCounts[1] = lastWhiteCounts[2]
    lastWhiteCounts[2] = lastWhiteCounts[3]
    lastWhiteCounts[3] = lastWhiteCounts[4]
    lastWhiteCounts[4] = greatSkillcheckPx
    averageLWC = np.mean(lastWhiteCounts)
    if(averageLWC > 20 and averageLWC < 300):
        skillCheck = True
    if(skillCheck and lastWhiteCounts[4]+5 < lastWhiteCounts[3]):
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        skillCheck = False
        time.sleep(0.5)

    return processedFrame
    

def getScreenCenter():
    while(True):
        lasttime = time.time()
        #printscreen =  np.array(ImageGrab.grab(bbox=(810,440,1060,690)))
        sct.get_pixels(mon)
        printscreen = Image.frombytes( 'RGB', (sct.width, sct.height), sct.image )
        printscreen = np.array(printscreen)
        new_screen = processFrame(printscreen)
        #cv2.imshow('window2',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        cv2.imshow('window', new_screen)
        print("Loop took {}".format(time.time()-lasttime))
        if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

getScreenCenter()
