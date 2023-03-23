import threading
from TextField import TextField
from abc import ABC, abstractmethod
from typing import ClassVar

from Mail import Mail
from Timer import Timer
from Keyboard import Keyboard, KeyboardState
import math
import cv2
from Brush import Brush
from Ranking import Ranking
import numpy as np
from cv2 import Mat
import cvzone
from ImageCanvas import ImageCanvas
from Button import Button
import sys
from Hand import Hand


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
        self.back_btn = Button(100, 250, "VOLTAR ATRAS")
        self.exit_btn = Button(900, video_height - 100, "SAIR")
        self.picture_btn = Button(25, video_height - 100, "FOTO")
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
        # return self.emailState()
        self.imageCanvas.reset()
        return FreeModeState(
            self.headerImage,
            self.ni_logo,
            self.ni_banner,
            self.ranking_img,
            self.ranking,
            self.video_height,
            self.imageCanvas,
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

        text_field_ui = Button(50, 50, self.text_field.parsed_value, 800)
        text_field_ui.draw(img)

        for hand in hands:
            cv2.circle(
                img,
                (hand.index_tip_position[0], hand.index_tip_position[1]),
                1,
                self.NI_COLOR_RED,
                hand.brush.size + 15,
            )

            kbd_mod = self.keyboard.modifier
            if self.keyboard.alt_btn.click(hand): 
                self.keyboard.modifier = KeyboardState.NORMAL if kbd_mod == KeyboardState.ALT else KeyboardState.ALT
            elif self.keyboard.shift_btn.click(hand):
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
    ERASER_SMALL: ClassVar[Brush] = Brush(70)
    ERASER_BIG: ClassVar[Brush] = Brush(100)
    RED_BRUSH: ClassVar[Brush] = Brush(20, (45, 45, 240))
    PINK_BRUSH: ClassVar[Brush] = Brush(20, (230, 78, 214))
    YELLOW_BRUSH: ClassVar[Brush] = Brush(20, (15, 245, 245))
    GREEN_BRUSH: ClassVar[Brush] = Brush(20, (13, 152, 35))
    BLUE_BRUSH: ClassVar[Brush] = Brush(20, (250, 160, 15))

    def paint(self, img, hands):
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
                if hand.previous_brush is not None:
                    hand.set_brush(hand.previous_brush)
                    hand.previous_brush = None

                cv2.circle(img, (x1, y1), 1, hand.brush.color, hand.brush.size + 15)
                # Drawing mode
                # Basically, we'll be drawing random lines which are actually tiny cv2.lines on loop

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

            elif 3 <= (hand_count_up := hand.count_fingers_up()) <= 4:
                # get previous size/previous color
                if hand.previous_brush not in (
                    PaintingState.ERASER_SMALL,
                    PaintingState.ERASER_BIG,
                ):
                    hand.previous_brush = hand.brush

                if hand_count_up == 3:
                    hand.set_brush(PaintingState.ERASER_SMALL)
                else:
                    hand.set_brush(PaintingState.ERASER_BIG)

                if not hand.last_drawn:
                    hand.update_reference_points()

                x, y = hand.last_drawn

                cv2.circle(img, (x2, y2), hand.brush.size, hand.brush.color)
                cv2.circle(
                    self.imageCanvas.canvas,
                    (x2, y2),
                    hand.brush.size,
                    hand.brush.color,
                    -1,  # any negative value should suffice
                )

                """                 cv2.circle(
                    self.imageCanvas.canvas,
                    (x2, y2),
                    (x, y),
                    hand.brush.color,
                    hand.brush.size,
                ) """

            # Updating the selected color
            # cv2.circle(img, (x, y), 1, hand.brush.color, hand.brush.size + hand.indicator_up()*15)
            hand.update_reference_points()

    def draw_menu(self, img, hands):
        img = cvzone.overlayPNG(img, self.headerImage, (0, 20))

        # Merge Video capture and Canvas
        img = self.imageCanvas.merge(img)
        
        # Logo
        img = cvzone.overlayPNG(img, self.ni_logo, (20, 20))

        self.exit_btn.draw(img)

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
        self.picture_btn.draw(img)

        for hand in hands:
            if self.picture_btn.click(hand):
                return self.pictureTimerState(), img

        return state, img

class MainMenuState(State):
    def run(self, img, hands: list[Hand]) -> tuple[State, Mat]:
        # create a black overlay with opacity 0.2
        black_overlay = np.zeros((720, 1280, 3), np.uint8)
        img = cv2.addWeighted(img[0:720, 0:1280], 0.5, black_overlay, 0.5, 1)

        # Logo
        img = cvzone.overlayPNG(img, self.ni_banner, [20, 20])

        # Buttons
        self.free_mode_btn.draw(img)
        self.challenge_mode_btn.draw(img)
        self.controls_btn.draw(img)
        self.ranking_btn.draw(img)
        self.exit_btn.draw(img)

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
        x, y, h = 650, 150, 48
        cv2.putText(
            img,
            "Ranking",
            (x, y - h),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            self.NI_COLOR_RED,
            4,
            cv2.LINE_AA,
        )
        for person in self.ranking.top:
            cv2.putText(
                img,
                person["name"],
                (x, y + h * self.ranking.top.index(person)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                str(person["score"]),
                (x + 400, y + h * self.ranking.top.index(person)),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

        # Button
        self.back_btn.draw(img)

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
