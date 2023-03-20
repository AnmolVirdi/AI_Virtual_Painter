import numpy as np
import cv2

class ImageCanvas:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.canvas = np.zeros((self.height,self.width,3),np.uint8)

    def merge(self, img):
        # Converting to grayscale
        imageGray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY) 

        # Converting to binary
        _, imgBinary = cv2.threshold(imageGray, 50, 255, cv2.THRESH_BINARY_INV) 

        # Inverted and B&W version of canvas
        imgBinary = cv2.cvtColor(imgBinary, cv2.COLOR_GRAY2BGR)

        #Inscribing the black region of imgBinary to img
        img = cv2.bitwise_and(img, imgBinary)

        #Adding the original color to the inscribed region using bitwise_or operations
        img = cv2.bitwise_or(img, self.canvas)
        
        return img

