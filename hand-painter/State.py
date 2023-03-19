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
    def run(self,
            img,
            hands: list[Hand]) -> tuple[State, Mat]:
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
            if not hand.clicked():
                continue
            if self.back_btn.click(hand.index_tip_position):
                return self.mainMenuState(), img

        return self, img