"""
HAND TRACKING MODULE USING OPENCV AND MEDIAPIPE
By Anmol Virdi (Self-Authored)
Created on 17/06/21
"""

#Importing openCV, mediapipe and time libraries
import cv2
import mediapipe as mp
import time
import numpy as np

#Creating a Class/prototype
class handDetector():

    #Constructor, with some default values
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon=trackCon

        #Assigning the hand detector as well as hand landmarks(points) detector funtions to variables of the class
        self.mpHands= mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    #function to detect hands and place/draw landmarks on them
    def findHands(self, img, videoCap, draw=True):
        img1 = cv2.cvtColor(videoCap, cv2.COLOR_BGR2RGB)
        self.results =  self.hands.process(img1)

        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks: # Usar lenght aqui
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, 
                        self.mpDraw.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), #color of points
                        self.mpDraw.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)) #color of connections
        return img

    #Function to find coordinates of all the landmarks of a particular hand(default= hand number 0). Returns a list of all of them.
    def findPositions(self, img, draw=True):

        self.lmList = []
        if not self.results.multi_hand_landmarks:
            return self.lmList

        for myHand in self.results.multi_hand_landmarks:
            l = []
            for id, lm in enumerate(myHand.landmark):

                #To draw those handlandmarks on the video frames
                #The coordinates recieved in lm are actually relative, i.e, 0-1. So, we need to convert them as per the size of original image.

                #Getting height, width and the number of channels of the original images using the .shape function
                height, width, channels = img.shape

                #Converting the relative coordinates(x,y) from lms to original coordinates(cx,cy)
                cx,cy = int(lm.x*width), int(lm.y*height)

                #print(id, cx, cy)
                l.append([id, cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy), 10, (255,255,0), cv2.FILLED)
                self.lmList.append(l)

        return self.lmList

    def fingersUp(self): #checks whether the finger are up or not
        fingers=[]
        tipIDs=[4,8,12,16,20] #Finger tip IDs

        #thumb
        if self.lmList[tipIDs[0]][1]< self.lmList[tipIDs[0]-1][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        print(len(self.lmList))

        # Other fingers
        for id in range(1,5):
            if self.lmList[tipIDs[id]][2]> self.lmList[tipIDs[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
        #it returns a list (0 if it's up and 1 if it's not).

#Note: To change the color of Landmark joining lines
#Use this below mentioned instead of line number 31
#self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS, self.mpDraw.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=4),self.mpDraw.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=4))

#Implementation/Check
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList)!=0:
            print(lmList[4])
        #FRAME RATE
        cTime = time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0),3)

        cv2.imshow("Hello", img)
        #TO TERMINATE THE PROGRAM, PRESS Q
        if cv2.waitKey(1) & 0xFF == ord('q'):
              break

if __name__=="__main__":
    main()
