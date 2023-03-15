import cv2

BACKGROUND_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

class Button:
    w = 350
    h = 80

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, img):
        # draw button with openCV
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), BACKGROUND_COLOR, -1)
        # align text in the middle
        font = cv2.FONT_HERSHEY_PLAIN
        text_size = cv2.getTextSize(self.text, font, 3, 1)[0]
        text_x = int((self.w - text_size[0]) / 2) + self.x
        text_y = int((self.h + text_size[1]) / 2) + self.y
        cv2.putText(img, self.text, (text_x, text_y), font, 3, TEXT_COLOR, 2)

    def click(self, pos):
        # check if the mouse is inside the button
        return self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h
    