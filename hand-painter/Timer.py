import time


class Timer:
    def __init__(self, duration) -> None:
        self.final = time.time() + duration

    @property
    def value(self):
        return self.final - time.time()

    @property
    def completed(self):
        return time.time() >= self.final
