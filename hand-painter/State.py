import threading
from Text import Text
from TextField import TextField
from abc import ABC, abstractmethod
from typing import ClassVar
import math
import cv2
import numpy as np
from cv2 import Mat
import cvzone

from Mail import Mail
from Timer import Timer
from Keyboard import Keyboard, KeyboardState
from Brush import Brush, BigEraser, SmallEraser
from Ranking import Ranking
from ImageCanvas import ImageCanvas
from Button import Button
from Hand import Hand
from Dataset import Dataset

folder_location = "Utilities"
normal_keyboard_set = cv2.imread(f"{folder_location}/normal_layout.png", cv2.IMREAD_UNCHANGED)
shift_keyboard_set = cv2.imread(f"{folder_location}/shift_layout.png", cv2.IMREAD_UNCHANGED)

class State:
    def __init__(
        self,
        headerImage,
        ni_logo,
        ni_banner,
        ranking_img,
        ranking: Ranking,
        video_height,
        imageCanvas: ImageCanvas,
    ) -> None:
        self.free_mode_btn = Button(250, 300, "MODO LIVRE")
        self.challenge_mode_btn = Button(700, 300, "DESAFIO")
        self.ranking_btn = Button(500, 500, "RANKING")
        self.controls_btn = Button(900, 100, "CONTROLOS")
        self.back_btn = Button(100, 250, "VOLTAR ATRÁS")
        self.exit_btn = Button(900, video_height - 100, "SAIR")
        self.picture_btn = Button(25, video_height - 100, "FOTO")
        self.headerImage = headerImage
        self.ni_logo = ni_logo
        self.ni_banner = ni_banner
        self.ranking_img = ranking_img
        self.NI_COLOR_RED = (54, 54, 179) #BGR NIAEFEUP color
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
            self.imageCanvas,
        )

    def pictureTimerState(self):
        return PictureTimerState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas
        )

    def emailState(self):
        return EmailState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas
        )

    def freeModeState(self):
        self.imageCanvas.reset()
        return FreeModeState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas,
            (0, 130, 1280, 720)
        )
        
    def challengeModeState(self):
        self.imageCanvas.reset()
        return ChallengeModeState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas,
            (240, 140, 720, 610)
        )

    def rankingState(self):
        return RankingState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas,
        )

    @abstractmethod
    def run(self, img, hand: Hand) -> tuple["State", Mat]:
        pass

class EmailState(State):
    def __init__(self, headerImage, ni_logo, ni_banner, ranking_img, ranking: Ranking, video_height, imageCanvas: ImageCanvas) -> None:
        super().__init__(headerImage, ni_logo, ni_banner, ranking_img, ranking, video_height, imageCanvas)
        self.text_field = TextField()
        self.keyboard = Keyboard(lambda x : self.text_field.type(x))

    def run(self, img, hands: list[Hand]) -> tuple["State", Mat]:
        self.keyboard.draw(img, hands)

        text_field_ui = Button(200, 50, self.text_field.parsed_value, 800)
        img = text_field_ui.draw(img)

        if self.keyboard.modifier == KeyboardState.NORMAL:
            img = cvzone.overlayPNG(img, normal_keyboard_set, (0, 0))
        else:
            img = cvzone.overlayPNG(img, shift_keyboard_set, (0, 0))

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            kbd_mod = self.keyboard.modifier
            if self.keyboard.shift_btn.click(hand):
                self.keyboard.modifier = KeyboardState.NORMAL if kbd_mod == KeyboardState.SHIFT else KeyboardState.SHIFT
            elif self.keyboard.delete_btn.click(hand):
                self.text_field.delete()
            elif self.keyboard.submit_btn.click(hand):
                threading.Thread(target=lambda: Mail().send(self.text_field.parsed_value, ["foto.png", "desenho.png"])).start()
                return self.mainMenuState(), img

        return self, img

class PictureTimerState(State):
    def __init__(self, headerImage, ni_logo, ni_banner, ranking_img, ranking: Ranking, video_height, imageCanvas: ImageCanvas) -> None:
        super().__init__(headerImage, ni_logo, ni_banner, ranking_img, ranking, video_height, imageCanvas)

        self.timer = Timer(5)

    def run(self, img, hand: Hand) -> tuple["State", Mat]:
        img = self.imageCanvas.merge(img)
        cv2.putText(img, f"Sorri! {math.ceil(self.timer.value)}", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, self.NI_COLOR_RED, 2)

        if self.timer.completed:
            cv2.imwrite("desenho.png", self.imageCanvas.white_canvas())
            cv2.imwrite("foto.png", self.imageCanvas.merge_camera())
            return self.emailState(), img

        return self, img

class PaintingState(State):
    def __init__(self, headerImage, ni_logo, ni_banner, ranking_img, ranking: Ranking, video_height, imageCanvas: ImageCanvas, limits) -> None:
        super().__init__(headerImage, ni_logo, ni_banner, ranking_img, ranking, video_height, imageCanvas)
        self.limits = limits #tuple[int, int, int, int]

    RED_BRUSH: ClassVar[Brush] = Brush(20, (45, 45, 240))
    PINK_BRUSH: ClassVar[Brush] = Brush(20, (230, 78, 214))
    YELLOW_BRUSH: ClassVar[Brush] = Brush(20, (15, 245, 245))
    GREEN_BRUSH: ClassVar[Brush] = Brush(20, (13, 152, 35))
    BLUE_BRUSH: ClassVar[Brush] = Brush(20, (250, 160, 15))

    def paint(self, img, hands):

        if self.limits:
            overlay = img.copy()
            x1, y1, x2, y2 = self.limits
            x1, y1 = x1 - 1, y1 - 1
            x2, y2 = x2 + 1, y2 + 1
            cv2.rectangle(overlay, (0, 0), (x1, img.shape[0]), (0, 0, 0), -1)
            cv2.rectangle(overlay, (x2, 0), (img.shape[1], img.shape[0]), (0, 0, 0), -1)
            cv2.rectangle(overlay, (x1, 0), (x2, y1), (0, 0, 0), -1)
            cv2.rectangle(overlay, (x1, y2), (x2, img.shape[0]), (0, 0, 0), -1)
            cv2.addWeighted(overlay, 0.5, img, 1 - 0.5, 0, img)

        # Add limits parameter for square limits in challenge mode
        for hand in hands:
            # index finger tip coordinates(landmark number 8)
            x1, y1 = hand.index_tip_position

            # Middle finger tip coordinates(landmark number 12)
            x2, y2 = hand.middle_tip_position

            # Checking which Fingers are up
            # For each finger, it returns 0 if it's up and 1 if it's not.
            # print(fingers)

            x, y = 0, 0

            if hand.indicator_and_middle_up():
                # Selection mode
                x, y = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x, y), 1, hand.brush.color, hand.brush.size)

                # color selections(In the header)
                # Whichever brush_color(region) is selected, it'll get updated in the main window
                if y1 < 100:
                    # Now we'll divide the whole header(1280 width) into the regions of those brushes and eraser, and change our color accordingly.
                    # Whichever region is selected, the corresponding color as well as headerImage is opted.
                    if 244 < x1 < 330:
                        hand.brush.decrease()
                    elif 330 < x1 < 420:
                        hand.brush.increase()
                    elif 460 < x1 < 552:
                        hand.set_brush(PaintingState.RED_BRUSH)
                    elif 552 < x1 < 650:
                        hand.set_brush(PaintingState.PINK_BRUSH)
                    elif 650 < x1 < 741:
                        hand.set_brush(PaintingState.YELLOW_BRUSH)
                    elif 741 < x1 < 832:
                        hand.set_brush(PaintingState.GREEN_BRUSH)
                    elif 832 < x1 < 925:
                        hand.set_brush(PaintingState.BLUE_BRUSH)
                    elif 962 < x1 < 1051:
                        self.imageCanvas.reset()  # clears the canvas

            # Drawing mode: Index finger up
            elif hand.indicator_up():

                cv2.circle(img, (x1, y1), 1, hand.brush.color, hand.brush.size + 15)
                
                # Drawing mode

                # Initialising reference points
                if not hand.last_drawn:
                    hand.update_reference_points()

                x, y = hand.last_drawn

                cv2.line(
                    self.imageCanvas.canvas,
                    (x, y),
                    (x1, y1),
                    hand.brush.color,
                    hand.brush.size,
                )

                # Create a mask with the limiits
                mask = np.zeros_like(self.imageCanvas.canvas)
                mask = cv2.rectangle(mask, (self.limits[0], self.limits[1]), (self.limits[2], self.limits[3]), (255, 255, 255), -1)
                self.imageCanvas.canvas = cv2.bitwise_and(self.imageCanvas.canvas, mask)

            elif 3 <= (hand_count_up := hand.count_fingers_up()) <= 4:
                eraser = SmallEraser() if hand_count_up == 3 else BigEraser()

                if not hand.last_drawn:
                    hand.update_reference_points()

                x, y = hand.last_drawn

                cv2.circle(img, (x2, y2), eraser.size, eraser.color)
                cv2.circle(
                    self.imageCanvas.canvas,
                    (x2, y2),
                    eraser.size,
                    eraser.color,
                    -1,  # any negative value should suffice
                )

            # Updating the selected color
            # cv2.circle(img, (x, y), 1, hand.brush.color, hand.brush.size + hand.indicator_up()*15)
            hand.update_reference_points()

    def draw_menu(self, img, hands):
        img = cvzone.overlayPNG(img, self.headerImage, (0, 20))

        # Merge Video capture and Canvas
        img = self.imageCanvas.merge(img)
        
        # Logo
        img = cvzone.overlayPNG(img, self.ni_logo, (20, 20))

        img = self.exit_btn.draw(img, hands)

        # TODO CHANGE THIS TO ABOVE UI?
        for hand in hands:
            if self.exit_btn.click(hand):
                return self.mainMenuState(), img

        return self, img

    @abstractmethod
    def run(self, img, hands: Hand) -> tuple["State", Mat]:
        pass

class FreeModeState(PaintingState):
    def run(self, img, hands: Hand) -> tuple["State", Mat]:
        self.paint(img, hands)
        state, img = self.draw_menu(img, hands)
        img = self.picture_btn.draw(img, hands)

        for hand in hands:
            if self.picture_btn.click(hand):
                return self.pictureTimerState(), img

        return state, img
    
class ChallengeModeState(PaintingState):
    def __init__(self, headerImage, ni_logo, ni_banner, ranking_img, ranking: Ranking, video_height, imageCanvas: ImageCanvas, limits) -> None:
        super().__init__(headerImage, ni_logo, ni_banner, ranking_img, ranking, video_height, imageCanvas, limits)
        self.word_to_draw = Dataset().get_random_word()

    def run(self, img, hands: Hand) -> tuple["State", Mat]:
        square_size = 470
        top, left = 140, 240

        self.paint(img, hands)

        offsetX = (left + square_size + 20)
        text1 = "Desenha esta palavra"
        text2 = self.word_to_draw["name_pt"]

        img = Text.putTextCenter(img, text1, top+50, offsetX)
        img = Text.putTextCenter(img, text2, top+100, offsetX)

        state, img = self.draw_menu(img, hands)

        for hand in hands:
            continue

        return state, img

class MainMenuState(State):
    def run(self, img, hands: list[Hand]) -> tuple[State, Mat]:

        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, [20, 20])

        # Buttons
        img = self.free_mode_btn.draw(img, hands)
        img = self.challenge_mode_btn.draw(img, hands)
        img = self.controls_btn.draw(img, hands)
        img = self.ranking_btn.draw(img, hands)
        img = self.exit_btn.draw(img, hands)

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            if(self.free_mode_btn.click(hand)):
                return self.freeModeState(), img
            
            if(self.challenge_mode_btn.click(hand)):
                return self.challengeModeState(), img

            if(self.ranking_btn.click(hand)):
                return self.rankingState(), img

            if(self.exit_btn.click(hand)):
                cv2.destroyAllWindows()
                exit()

        return self, img


class RankingState(State):
    def run(self, img, hands: list[Hand]) -> tuple[State, Mat]:
        black_overlay = np.zeros((720, 1280, 3), np.uint8)
        img = cv2.addWeighted(img[0:720, 0:1280], 0.3, black_overlay, 0.5, 1)

        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, (20, 20))

        # Ranking image
        img = cvzone.overlayPNG(
            img, self.ranking_img, (170, self.video_height - self.ranking_img.shape[0])
        )

        # Ranking
        img = Text.drawRanking(img, self.ranking.top)

        # Button
        img = self.back_btn.draw(img, hands)

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            if self.back_btn.click(hand):
                return self.mainMenuState(), img

        return self, img
