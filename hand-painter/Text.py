import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

class Text:
    font = ImageFont.truetype("./Skrapbook.ttf", 35)

    @staticmethod
    def putText(img, text, coordinates, scale=1, color=(255, 255, 255), thickness=2):
        pil_image = Text.cv2pillow(img)

        draw = ImageDraw.Draw(pil_image)
        draw.text((coordinates), text, font=Text.font, fill=color)

        return Text.pillow2cv(pil_image)
    
    @staticmethod
    def putTextCenter(img, text, y, offsetX=0, scale=1, color=(255, 255, 255), thickness=2):
        width = 1280 - offsetX

        pil_image = Text.cv2pillow(img)
        draw = ImageDraw.Draw(pil_image)
        _, _, textWidth, _ = draw.textbbox((0, 0), text, font=Text.font)
        medium = int((width - textWidth) / 2)
        draw.text((( medium + offsetX ), y), text, font=Text.font, fill=color)

        return Text.pillow2cv(pil_image)
    
    @staticmethod
    def putTextBox(img, text, coordinates, width, height, scale=1, color=(255, 255, 255), thickness=2):
        pil_image = Text.cv2pillow(img)
        draw = ImageDraw.Draw(pil_image)

        _, _, textWidth, textHeight = draw.textbbox((0, 0), text, font=Text.font)
        print(width, textWidth, height, textHeight, coordinates)
        startX = int((width - textWidth) / 2) + coordinates[0]
        startY = int((height - textHeight) / 2) + coordinates[1]
        draw.text((startX, startY), text, font=Text.font, fill=color)

        return Text.pillow2cv(pil_image)

    def cv2pillow(img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image)
    
    def pillow2cv(img):
        image = np.asarray(img)
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
