import cv2
from Hand import Hand
from Text import Text

BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

class Button:
    def __init__(self, x, y, text, width = 350, height = 80):
        self.x = x
        self.y = y
        self.text = text
        self.w = width
        self.h = height

        if len(text) > 10 and (30 * len(text) + 60) > width:
            self.w = 30 * len(text) + 60

    def draw(self, img):
        # cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), BACKGROUND_COLOR, -1)
        border_radius = 5

        cv2.ellipse(
            img,
            (self.x + border_radius, self.y + border_radius),
            (border_radius, border_radius),
            180,
            0,
            90,
            BACKGROUND_COLOR,
            -1,
        )
        cv2.ellipse(
            img,
            (self.x + self.w - border_radius, self.y + border_radius),
            (border_radius, border_radius),
            270,
            0,
            90,
            BACKGROUND_COLOR,
            -1,
        )
        cv2.rectangle(
            img,
            (self.x + border_radius, self.y),
            (self.x + self.w - border_radius, self.y + border_radius),
            BACKGROUND_COLOR,
            -1,
        )
        cv2.rectangle(
            img,
            (self.x, self.y + border_radius),
            (self.x + self.w, self.y + self.h),
            BACKGROUND_COLOR,
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
        # align text in the middle
        #cv2.putText(img, self.text, (self.x, self.y), cv2.FONT_HERSHEY_SIMPLEX, 3, TEXT_COLOR, 2)
        return Text.putTextBox(img, self.text, (self.x, self.y), self.w, self.h, color=TEXT_COLOR)

    def click(self, hand: Hand):
        pos = hand.index_tip_position

        # Check if the mouse is inside the button
        return self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h and hand.clicked()
