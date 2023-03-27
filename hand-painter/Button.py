import cv2
from Hand import Hand
from Text import Text

BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_HOVER_COLOR = (220, 220, 220)
TEXT_COLOR = (0, 0, 0)


class Button:
    def __init__(self, x, y, text, width=350, height=80):
        self.x = x
        self.y = y
        self.text = text
        self.w = width
        self.h = height

        if len(text) > 10 and (30 * len(text) + 60) > width:
            self.w = 30 * len(text) + 60

    def drawSimple(self, img, hands: list[Hand] = [], color=BACKGROUND_COLOR):
        border_radius = 5

        # check if one hand is inside the button
        for hand in hands:
            if self.hover(hand):
                color = BACKGROUND_HOVER_COLOR

        cv2.ellipse(
            img,
            (self.x + border_radius, self.y + border_radius),
            (border_radius, border_radius),
            180,
            0,
            90,
            color,
            -1,
        )
        cv2.ellipse(
            img,
            (self.x + self.w - border_radius, self.y + border_radius),
            (border_radius, border_radius),
            270,
            0,
            90,
            color,
            -1,
        )
        cv2.rectangle(
            img,
            (self.x + border_radius, self.y),
            (self.x + self.w - border_radius, self.y + border_radius),
            color,
            -1,
        )
        cv2.rectangle(
            img,
            (self.x, self.y + border_radius),
            (self.x + self.w, self.y + self.h),
            color,
            -1,
        )

        # Bottom border
        cv2.line(
            img,
            (self.x, self.y + self.h),
            (self.x + self.w, self.y + self.h),
            (54, 54, 179),
            3,
        )

    def draw(self, img, hands: list[Hand] = []):
        self.drawSimple(img, hands)

        return Text.putTextBox(
            img, self.text, (self.x, self.y), self.w, self.h, color=TEXT_COLOR
        )

    def click(self, hand: Hand):
        pos = hand.index_tip_position
        return (
            self.x < pos[0] < self.x + self.w
            and self.y < pos[1] < self.y + self.h
            and hand.clicked()
        )

    def hover(self, hand: Hand):
        index = hand.index_tip_position
        thumb = hand.thumb_tip_position

        # Medium point between the index finger tip and the thumb tip
        pos = (index[0] + thumb[0]) / 2, (index[1] + thumb[1]) / 2

        return self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h
