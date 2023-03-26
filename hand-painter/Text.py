import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np

class Text:
    font = ImageFont.truetype("./Skrapbook.ttf", 35)
    NI_COLOR_RED = (179, 54, 54)

    @staticmethod
    def putText(img, text, coordinates, scale=1, color=(255, 255, 255), thickness=2):
        pil_image = Text.cv2pillow(img)

        color = (color[2], color[1], color[0])

        draw = ImageDraw.Draw(pil_image)
        draw.text((coordinates), text, font=Text.font, fill=color)

        return Text.pillow2cv(pil_image)
    
    @staticmethod
    def putTextCenter(img, text, y, offsetX=0, scale=1, color=(255, 255, 255), thickness=2):
        width = 1280 - offsetX

        color = (color[2], color[1], color[0])

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

        color = (color[2], color[1], color[0])

        _, _, textWidth, textHeight = draw.textbbox((0, 0), text, font=Text.font)
        startX = int((width - textWidth) / 2) + coordinates[0]
        startY = int((height - textHeight) / 2) + coordinates[1]
        draw.text((startX, startY), text, font=Text.font, fill=color)

        return Text.pillow2cv(pil_image)

    def drawRanking(img, top, color=(255, 255, 255)):
        pil_image = Text.cv2pillow(img)
        draw = ImageDraw.Draw(pil_image)

        x, y, h = 650, 150, 48

        draw.text((x, y - h), "Ranking", font=Text.font, fill=Text.NI_COLOR_RED)
        
        for person in top:
            draw.line((x, y + h * top.index(person)-7, x + 480, y + h * top.index(person) - 7), fill=(30, 30, 30), width=1)

            draw.text((x, y + h * top.index(person)), person["name"], font=Text.font, fill=color)
            draw.text((x + 270, y + h * top.index(person)), str(person["score"]), font=Text.font, fill=color)
            draw.text((x + 340, y + h * top.index(person)), person["draw"], font=Text.font, fill=color)

        return Text.pillow2cv(pil_image)

    def cv2pillow(img):
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image)
    
    def pillow2cv(img):
        image = np.asarray(img)
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
