class Brush:
    def __init__(self, size):
        self.size = size
    def increase(self):
        if self.size < 180:
            self.size += 5
    def decrease(self):
        if self.size > 10:
            self.size -= 5