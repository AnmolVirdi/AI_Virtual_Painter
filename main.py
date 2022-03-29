import cv2
import numpy as np
import time
import handtrackingmodule as htm #mediapipe library used in this module
import pygame

pygame.init()

#Importing header images using os functions
folder_location = "Utilities/Header"

headerImage = cv2.imread(f'{folder_location}/header.png') #setting default header image

drawColor = (45,45,240) #Default color
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

def save_image(matrix):
    timestamp = time.time()
    filename = f'images/{timestamp}.png'
    cv2.imwrite(filename, matrix)
    return 

class Brush:
    def __init__(self, size):
        self.size = size
    def increase(self):
        if self.size < 180:
            self.size += 5
    def decrease(self):
        if self.size > 10:
            self.size -= 5

brush = Brush(20)

#Displaying the video, frame by frame
running = True
while running:
    #keyboard events
    for event in pygame.event.get():
        #Save image
        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 's':
            save_image(imageCanvas)
        #Quit
        if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == 'q':
            running = False

    #increase/decrease brush size
    key_input = pygame.key.get_pressed()   
    if key_input[pygame.K_UP]: brush.increase()
    if key_input[pygame.K_DOWN]: brush.decrease()

    #Importing main image using read() function
    success, img = vCap.read()
    captImg = cv2.flip(img, 1)
    img = captImg #flipping the video, to compensate lateral inversion

    #Finding Hand Landmarks using handtrackingmodule
    img = detector.findHands(img, img, draw=False)
    landmarkList = detector.findPosition(img, draw=False)

    #Setting the header image in the main window
    #Inserting header image on the main window (Header size:1280x100)

    overlay=cv2.addWeighted(img[0:100, 0:1280],0.2,headerImage,0.8, 1)
    img[0:100, 0:1280] = overlay

    if (len(landmarkList) != 0):
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
            if y1<100:
                #Now we'll divide the whole header(1280 width) into the regions of those brushes and eraser, and change our color accordingly.
                #Whichever region is selected, the corresponding color as well as headerImage is opted.
                if 244<x1<330:
                    brush.decrease()
                elif 330<x1<420:
                    brush.increase()
                elif 460<x1<552:
                    drawColor=(45,45,240)
                elif 552<x1<650:
                    drawColor=(230,78,214)
                elif 650<x1<741:
                    drawColor=(15, 245, 245)
                elif 741<x1<832:
                    drawColor=(13,152,35)
                elif 832<x1<925:
                    drawColor=(250,160,15)
                elif 962<x1<1051:
                    drawColor=(0,0,0)
                elif 1087<x1<1175:
                    imageCanvas = np.zeros((720,1280,3),np.uint8) #clears the canvas

            #Updating the selected color
            cv2.circle(img, (cx,cy), 1, drawColor, brush.size)

        #Drawing mode when only index finger is Up
        if fingers[1]==0 and fingers[2]==1:
            cv2.circle(img,(x1,y1), 1, drawColor, brush.size + 15)
            #Drawing mode
            #Basically, we'll be drawing random lines which are actually tiny cv2.lines on loop

            #Initialising reference points
            if xx==0 and yy==0:
                xx,yy=x1,y1;

            cv2.line(img,(xx,yy),(x1,y1),drawColor, brush.size)
            cv2.line(imageCanvas,(xx,yy),(x1,y1),drawColor, brush.size)

        #midle finder up
        if fingers[2]==0 and not(False in [fingers[x]==1 for x in [0, 1, 3, 4]]):
            print("mal comportado")

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

    #Adding hand landmarks
    img = detector.findHands(img, captImg)

    ##########################################################################################


    cv2.imshow("Painter",img)

pygame.quit()
exit()
