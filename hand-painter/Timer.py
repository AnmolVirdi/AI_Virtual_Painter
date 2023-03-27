import time
import math

class Timer:
    def __init__(self, duration) -> None:
        self.final = time.time() + duration
        self.duration = duration

    @property
    def value(self):
        return self.final - time.time()
    
    @property
    def overlay(self):
        return self.value * 0.7 / self.duration 
    
    @property
    def completed(self):
        return time.time() >= self.final
