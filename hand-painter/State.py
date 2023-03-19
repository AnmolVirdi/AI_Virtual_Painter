from abc import ABC, abstractmethod

import cv2
from Ranking import Ranking
import numpy as np
from cv2 import Mat
import cvzone
from numpy import ndarray, uint8
from Button import Button

class State:
    def __init__(self, headerImage, ni_logo, ni_banner, ranking_img, ranking: Ranking, video_height) -> None:
        self.free_mode_btn = Button(250, 300, "MODO LIVRE") 
        self.challenge_mode_btn = Button(700, 300, "DESAFIO")
        self.ranking_btn = Button(500, 500, "RANKING") 
        self.controls_btn = Button(900, 100, "CONTROLOS")
        self.back_btn = Button(100, 250, "VOLTAR ATRAS")
        self.exit_btn = Button(15, video_height - 100, "SAIR")
        self.headerImage = headerImage
        self.ni_logo = ni_logo
        self.ni_banner = ni_banner
        self.ranking_img = ranking_img
        self.NI_COLOR_RED = (54, 54, 179)
        self.ranking = ranking
        self.video_height = video_height

    def mainMenuState(self):
        return MainMenuState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height
        )

    def paintingState(self):
        return PaintingState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height
        )

    def rankingState(self):
        return RankingState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height
        )

    @abstractmethod
    def run(self, 
            detector, 
            captImg, 
            imageCanvas: ndarray,
            landmarkList) -> "State":
        pass


class PaintingState(State):
    def run(self,
            img,
            detector, 
            captImg, 
            imageCanvas: ndarray,
            landmarkList) -> tuple[State, Mat]:

        overlay=cv2.addWeighted(img[0:100, 0:1280],0.2, self.headerImage,0.8, 1)
        img[0:100, 0:1280] = overlay

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

        self.exit_btn.draw(img)


        # TODO CHANGE THIS TO ABOVE UI?
        if len(landmarkList) != 0:
            x1, y1 = landmarkList[8][1], landmarkList[8][2]
            x0, y0 = landmarkList[4][1], landmarkList[4][2]
            if (x1-x0)**2 + (y1-y0)**2 < (1500):
                if self.exit_btn.click([x1, y1]):
                    return self.mainMenuState(), img

        #Adding hand landmarks
        img = detector.findHands(img, captImg)

        return self, img

class MainMenuState(State):
    def run(self,
            img,
            detector, 
            captImg, 
            imageCanvas: ndarray,
            landmarkList) -> tuple[State, Mat]:
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

        if len(landmarkList) != 0:
            x1, y1 = landmarkList[8][1], landmarkList[8][2]
            x0, y0 = landmarkList[4][1], landmarkList[4][2]
            if (x1-x0)**2 + (y1-y0)**2 < (1500):
                if(self.free_mode_btn.click([x1, y1])):
                    return self.paintingState(), img
                
                if(self.ranking_btn.click([x1, y1])):
                    return self.rankingState(), img

        return self, img

class RankingState(State):
    def run(self,
            img,
            detector, 
            captImg, 
            imageCanvas: ndarray,
            landmarkList) -> tuple[State, Mat]:
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

        if len(landmarkList) != 0:
            x1, y1 = landmarkList[8][1], landmarkList[8][2]
            x0, y0 = landmarkList[4][1], landmarkList[4][2]
            if (x1-x0)**2 + (y1-y0)**2 < (1500):
                if self.back_btn.click([x1, y1]):
                    return self.mainMenuState(), img
        
        return self, img