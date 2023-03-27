class Brush:
    def __init__(self, size, color=(0, 0, 0)):
        self.size = size
        self.color = color

    def setSize(self, size: int):
        assert 0 <= size < 180

        self.size = size

    def increase(self):
        if self.size < 180:
            self.size += 5

    def decrease(self):
        if self.size > 10:
            self.size -= 5

    def setColor(self, color_b, color_g, color_r):
        self.color = (color_b, color_g, color_r)


class BigEraser(Brush):
    def __init__(self):
        super().__init__(100, (0, 0, 0))


class SmallEraser(Brush):
    def __init__(self):
        super().__init__(70, (0, 0, 0))
