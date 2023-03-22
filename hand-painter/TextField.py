import time

class TextField:
    def __init__(self) -> None:
        self.value = []

    @property
    def parsed_value(self):
        return str.join(self.value)

    def type(self, s):
        self.value.append(s)
    
    def delete(self, s):
        if len(self.value) > 0:
            self.value.pop()
