import numpy as np

class ImageCanvas:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.canvas = np.zeros((self.height,self.width,3),np.uint8)
