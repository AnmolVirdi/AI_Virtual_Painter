"""
AI VIRTUAL PAINTER
By Anmol Virdi (Self-Authored)
Created on 17/06/21
"""


#Importing OpenCV, numpy, time, os libraries
import cv2
import numpy as np
import time
import os
import handtrackingmodule as htm #mediapipe library used in this module

#Importing header images using os functions
folder_location = "Utilities/Header"
myList = os.listdir(folder_location)
print(myList) #displays name of all those images that will be used in the header

#Creating a list to store all those images as variables
overlayList=[]
for imPath in myList:
    image = cv2.imread(f'{folder_location}/{imPath}')
    overlayList.append(image) #adding images to the list, one by one.

headerImage = overlayList[0] #setting default header image
drawColor = (0,0,255) #Default color
xx,yy=0,0 #used as reference coordinates during drawing mode


#Variable to store video using cv2.VideoCapture() function
vCap = cv2.VideoCapture(0)
#Setting video resolution to 1280x720
vCap.set(3,1280)
vCap.set(4,720)

#Creating an instance from the handtrackingmodule
#Setting the detection confidence to 85% for accurate performance
detector = htm.handDetector(detectionCon=0.85)

#Canvas: It'll be like an invisible screen on our video, on which drawing functions will be implemented.
#Numpy array with zeros(representing black screen) similar to the dimensions of original video frames
imageCanvas = np.zeros((720,1280,3),np.uint8)

#Displaying the video, frame by frame
while True:
    #Importing main image using read() function
    success, img = vCap.read()
    img = cv2.flip(img, 1) #flipping the video, to compensate lateral inversion

    #Finding Hand Landmarks using handtrackingmodule
    img = detector.findHands(img)
    landmarkList = detector.findPosition(img, draw=False)

    if (len(landmarkList) != 0):
        #print(landmarkList)

        #index finger tip coordinates(landmark number 8)
        x1,y1 = landmarkList[8][1],landmarkList[8][2]

        #Middle finger tip coordinates(landmark number 12)
        x2,y2 = landmarkList[12][1],landmarkList[12][2]

        #Checking which Fingers are up
        fingers = detector.fingersUp()
        #For each finger, it returns 0 if it's up and 1 if it's not.
        #print(fingers)

        #If two fingers(index and mid) are up, selection mode(no drawing)
        if fingers[1]==0 and fingers[2]==0:
            #Selection mode
            cx,cy = (x1+x2)//2,(y1+y2)//2

            #color selections(In the header)
            #Whichever brush_color(region) is selected, it'll get updated in the main window
            if y1<125:
                #Now we'll divide the whole header(1280 width) into the regions of those brushes and eraser, and change our color accordingly.
                #Whichever region is selected, the corresponding color as well as headerImage is opted.
                if 20<x1<150:
                    imageCanvas = np.zeros((720,1280,3),np.uint8) #clears the canvas
                elif 250<x1<450:
                    headerImage=overlayList[0]
                    drawColor=(0,0,255)
                elif 550<x1<750:
                    headerImage=overlayList[1]
                    drawColor=(255, 150, 0)
                elif 800<x1<900:
                    headerImage=overlayList[2]
                    drawColor=(255,105,180)
                elif 950<x1<1200:
                    headerImage=overlayList[3]
                    drawColor=(0,0,0)
            #Updating the selected color
            cv2.circle(img, (cx,cy), 25, drawColor, cv2.FILLED)

        #Drawing mode when only index finger is Up
        if fingers[1]==0 and fingers[2]==1:
            cv2.circle(img,(x1,y1), 15,drawColor,cv2.FILLED)
            #Drawing mode
            #Basically, we'll be drawing random lines which are actually tiny cv2.lines on loop

            #Initialising reference points
            if xx==0 and yy==0:
                xx,yy=x1,y1;

            #Eraser functionality
            if drawColor==(0,0,0):
                cv2.line(img,(xx,yy),(x1,y1),drawColor,25)
                cv2.line(imageCanvas,(xx,yy),(x1,y1),drawColor,25)
            #Color functionality
            else:
                cv2.line(img,(xx,yy),(x1,y1),drawColor,15)
                cv2.line(imageCanvas,(xx,yy),(x1,y1),drawColor,15)

        #updating the reference points
        xx,yy=x1,y1

    ##########################################################################################

    #COMBINING BOTH THE IMAGES(Original video frame and the Canvas)

    #For thresholding, the first argument is the source image, which should be a grayscale image.
    imageGray = cv2.cvtColor(imageCanvas, cv2.COLOR_BGR2GRAY) #converted to grayscale
    #Converting it into binary image(Thresholding)
    _, imgBinary = cv2.threshold(imageGray,50,255,cv2.THRESH_BINARY_INV)
    imgBinary = cv2.cvtColor(imgBinary, cv2.COLOR_GRAY2BGR) #imgBinary: Inverted and B&W version of imageCanvas

    #Inscribing the black region of imgBinary to main image(img) using bitwise_and operations
    img = cv2.bitwise_and(img, imgBinary)

    #Adding the original color to the inscribed region using bitwise_or operations
    img = cv2.bitwise_or(img,imageCanvas)

    ##########################################################################################

    #Setting the header image in the main window
    #Inserting header image on the main window (Header size:1280x125)
    img[0:125,0:1280]=headerImage

    cv2.imshow("Painter",img)

    #TO TERMINATE THE PROGRAM, PRESS q
    if cv2.waitKey(1) & 0xFF == ord('q'):
          break
