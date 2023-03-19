from abc import ABC, abstractmethod

import cv2
from Ranking import Ranking
import numpy as np
from cv2 import Mat
import cvzone
from ImageCanvas import ImageCanvas
from Button import Button
import sys
from Hand import Hand

class State:
    def __init__(self, headerImage, ni_logo, ni_banner, ranking_img, ranking: Ranking, video_height, imageCanvas: ImageCanvas) -> None:
        self.free_mode_btn = Button(250, 300, "MODO LIVRE") 
        self.challenge_mode_btn = Button(700, 300, "DESAFIO")
        self.ranking_btn = Button(500, 500, "RANKING") 
        self.controls_btn = Button(900, 100, "CONTROLOS")
        self.back_btn = Button(100, 250, "VOLTAR ATRAS")
        self.menu_btn = Button(15, video_height - 100, "SAIR")
        self.exit_btn = Button(900, video_height - 120, "SAIR")
        self.headerImage = headerImage
        self.ni_logo = ni_logo
        self.ni_banner = ni_banner
        self.ranking_img = ranking_img
        self.NI_COLOR_RED = (54, 54, 179)
        self.ranking = ranking
        self.video_height = video_height
        self.imageCanvas = imageCanvas

    def mainMenuState(self):
        return MainMenuState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas
        )

    def paintingState(self):
        self.imageCanvas.reset()
        return PaintingState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas
        )

    def rankingState(self):
        return RankingState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas
        )

    @abstractmethod
    def run(self,
            img,
            hand: Hand) -> tuple["State", Mat]:
        pass


class PaintingState(State):
    def paint(self, img, hands):
        # Add limits parameter for square limits in challenge mode
        for hand in hands:
            #index finger tip coordinates(landmark number 8)
            x1,y1 = hand.index_tip_position

            #Middle finger tip coordinates(landmark number 12)
            x2,y2 = hand.middle_tip_position

            #Checking which Fingers are up
            #For each finger, it returns 0 if it's up and 1 if it's not.
            #print(fingers)

            if hand.indicator_and_midle_up():
                #Selection mode
                cx,cy = (x1+x2)//2,(y1+y2)//2

                #color selections(In the header)
                #Whichever brush_color(region) is selected, it'll get updated in the main window
                if y1<100:
                    #Now we'll divide the whole header(1280 width) into the regions of those brushes and eraser, and change our color accordingly.
                    #Whichever region is selected, the corresponding color as well as headerImage is opted.
                    if 244<x1<330:
                        hand.brush.decrease()
                    elif 330<x1<420:
                        hand.brush.increase()
                    elif 460<x1<552:
                        hand.brush.setColor(45,45,240)
                    elif 552<x1<650:
                        hand.brush.setColor(230,78,214)
                    elif 650<x1<741:
                        hand.brush.setColor(15, 245, 245)
                    elif 741<x1<832:
                        hand.brush.setColor(13,152,35)
                    elif 832<x1<925:
                        hand.brush.setColor(250,160,15)
                    elif 962<x1<1051:
                        hand.brush.setColor(0,0,0)
                    elif 1087<x1<1175:
                        self.imageCanvas.reset() #clears the canvas

                #Updating the selected color
                cv2.circle(img, (cx,cy), 1, hand.brush.color, hand.brush.size)

            #Drawing mode: Index finger up
            if hand.indicator_up():
                cv2.circle(img,(x1,y1), 1, hand.brush.color, hand.brush.size + 15)
                #Drawing mode
                #Basically, we'll be drawing random lines which are actually tiny cv2.lines on loop

                #Initialising reference points
                if not hand.last_drawn:
                    hand.update_reference_points()
                
                xx, yy = hand.last_drawn

                cv2.line(self.imageCanvas.canvas,(xx,yy),(x1,y1),hand.brush.color, hand.brush.size)
            hand.update_reference_points()

    def draw_menu(self, hands, img):
        overlay=cv2.addWeighted(img[0:100, 0:1280],0.2, self.headerImage,0.8, 1)
        img[0:100, 0:1280] = overlay

        #COMBINING BOTH THE IMAGES(Original video frame and the Canvas)

        #For thresholding, the first argument is the source image, which should be a grayscale image.
        imageGray = cv2.cvtColor(self.imageCanvas.canvas, cv2.COLOR_BGR2GRAY) #converted to grayscale
        #Converting it into binary image(Thresholding)
        _, imgBinary = cv2.threshold(imageGray,50,255,cv2.THRESH_BINARY_INV)
        imgBinary = cv2.cvtColor(imgBinary, cv2.COLOR_GRAY2BGR) #imgBinary: Inverted and B&W version of self.imageCanvas

        #Inscribing the black region of imgBinary to main image(img) using bitwise_and operations
        img = cv2.bitwise_and(img, imgBinary)

        #Adding the original color to the inscribed region using bitwise_or operations
        img = cv2.bitwise_or(img,self.imageCanvas.canvas)

        self.menu_btn.draw(img)


        # TODO CHANGE THIS TO ABOVE UI?
        for hand in hands:
            if hand.clicked():
                if self.menu_btn.click(hand.index_tip_position):
                    return self.mainMenuState(), img

        return img

    def run(self,
            img,
            hands: list[Hand]) -> tuple[State, Mat]:
        self.paint(img, hands)
        img = self.draw_menu(hands, img)

        return self, img

class MainMenuState(State):
    def run(self,
            img,
            hands: list[Hand]) -> tuple[State, Mat]:
      #create a black overlay with opacity 0.2
        black_overlay = np.zeros((720, 1280, 3), np.uint8)
        img = cv2.addWeighted(img[0:720, 0:1280],0.5,black_overlay,0.5, 1)

        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, [20, 20])

        # Buttons
        self.free_mode_btn.draw(img)
        self.challenge_mode_btn.draw(img)
        self.controls_btn.draw(img)
        self.ranking_btn.draw(img)
        self.exit_btn.draw(img)


        for hand in hands:
            cv2.circle(img,(hand.index_tip_position[0], hand.index_tip_position[1]), 1, self.NI_COLOR_RED, hand.brush.size + 15)

            if not hand.clicked():
                continue

            if(self.free_mode_btn.click(hand.index_tip_position)):
                return self.paintingState(), img
            
            if(self.ranking_btn.click(hand.index_tip_position)):
                return self.rankingState(), img
            
            if(self.exit_btn.click(hand.index_tip_position)):
                sys.exit(0)

        return self, img

class RankingState(State):
    def run(self,
            img,
            hands: list[Hand]) -> tuple[State, Mat]:
        black_overlay = np.zeros((720, 1280, 3), np.uint8)
        img = cv2.addWeighted(img[0:720, 0:1280],0.3,black_overlay,0.5, 1)

        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, (20, 20))
        
        # Ranking image
        img = cvzone.overlayPNG(img, self.ranking_img, (170, self.video_height - self.ranking_img.shape[0]))

        # Ranking
        x, y, h = 650, 150, 48
        cv2.putText(img, "Ranking", (x, y - h), cv2.FONT_HERSHEY_SIMPLEX, 1.5, self.NI_COLOR_RED, 4, cv2.LINE_AA)
        for person in self.ranking.top:
            cv2.putText(img, person['name'], (x, y + h * self.ranking.top.index(person)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(img, str(person['score']), (x + 400, y + h * self.ranking.top.index(person)), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

        # Button
        self.back_btn.draw(img)

        for hand in hands:
            cv2.circle(img,(hand.index_tip_position[0], hand.index_tip_position[1]), 1, self.NI_COLOR_RED, hand.brush.size + 15)

            if not hand.clicked():
                continue
            if self.back_btn.click(hand.index_tip_position):
                return self.mainMenuState(), img

        return self, img