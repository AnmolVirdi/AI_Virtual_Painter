import cv2
import time

# from predict import predict_image
import handtrackingmodule as htm #mediapipe library used in this module

from Hand import Hand
from Button import Button
from ImageCanvas import ImageCanvas
from Brush import Brush
from Ranking import Ranking
from State import State, MainMenuState

import math

NI_COLOR_RED = (54, 54, 179) #BGR

STATE = "main_menu"

cv2.namedWindow("Painter", cv2.WINDOW_AUTOSIZE)
#Importing header images using os functions
folder_location = "Utilities/Header"

ratio = 16/9
video_width = 1280
video_height = int(video_width/ratio)
headerImage = cv2.imread(f'{folder_location}/header.png')
ni_logo = cv2.imread('Utilities/logo.png')
ni_banner = cv2.imread('Utilities/banner.png', cv2.IMREAD_UNCHANGED)
ranking_img = cv2.imread('Utilities/ranking.png', cv2.IMREAD_UNCHANGED)
#ranking_img = cv2.resize(ranking_img, (100, 100))

ranking = Ranking()

#Variable to store video using cv2.VideoCapture() function
vCap = cv2.VideoCapture(0)
#Setting video resolution to 1280x720
vCap.set(3,video_width)
vCap.set(4,video_width*ratio)

#Creating an instance from the handtrackingmodule
#Setting the detection confidence to 85% for accurate performance
detector = htm.handDetector(detectionCon=0.85)

#Canvas: It'll be like an invisible screen on our video, on which drawing functions will be implemented.
#Numpy array with zeros(representing black screen) similar to the dimensions of original video frames
imageCanvas = ImageCanvas(1280, 720)

state: State = MainMenuState(
    headerImage,
    ni_logo,
    ni_banner,
    ranking_img,
    ranking,
    video_height,
    imageCanvas
)

def save_image(matrix):
    timestamp = time.time()
    filename = f'images/{timestamp}.png'
    cv2.imwrite(filename, matrix)
    return 

free_mode_btn = Button(250, 300, "MODO LIVRE") 
challenge_mode_btn = Button(700, 300, "DESAFIO")
ranking_btn = Button(500, 500, "RANKING") 
controls_btn = Button(900, 100, "CONTROLOS")
back_btn = Button(100, 250, "VOLTAR ATRAS")

hands_list: list[Hand] = []

def sqrd_distance(pos1, pos2):
    return math.dist(pos1, pos2)

def merge_hands(previous_hands: list[Hand], landmarks, fingers_up):
    new_list = []
    for idx, landmark in enumerate(landmarks):
        match = None
        best_dist = 10000
        for hand in previous_hands:
            dist = math.dist((landmark[0][1], landmark[0][2]), (hand.wrist_position[0], hand.wrist_position[1]))
            if dist > 50:
                continue
            if dist < best_dist:
                match = hand
                best_dist = dist

        if match:
            match.update_positions(landmark, fingers_up[idx])
        else:
            match = Hand(Brush(20), landmark, fingers_up[idx])

        new_list.append(match)
    return new_list

#Displaying the video, frame by frame
while True:
    #Importing main image using read() function
    success, img = vCap.read()
    captImg = cv2.flip(img, 1)
    img = captImg #flipping the video, to compensate lateral inversion

    #Finding Hand Landmarks using handtrackingmodule
    img = detector.findHands(img, img) 
    landmarkList = detector.findPositions(img, draw=False)
    hand_fingers = detector.fingersUp()

    hands_list = merge_hands(hands_list, landmarkList, hand_fingers)

    state, img = state.run(img, hands_list)

    cv2.imshow("Painter",img)
    key = cv2.waitKey(1)

    # Keyboard Shortcuts
    if key == ord('p'):
        predict_image(imageCanvas)
    elif key == ord('s'):
        save_image(img)
    elif key == ord('q'):
        break
    # elif key == ord('+'): #remove this? or change in all hands?
    #     brush.increase()
    # elif key == ord('-'):
    #     brush.decrease()

cv2.destroyAllWindows()
exit()
