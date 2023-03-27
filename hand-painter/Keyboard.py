from enum import Enum
from Button import Button


class KeyboardKey:
    def __init__(self, key) -> None:
        self.key = key


class KeyboardState(Enum):
    NORMAL = 0
    SHIFT = 1


class Keyboard:
    def __init__(self, callback) -> None:
        self.callback = callback

    keys = [
        ["\\", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
        ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "+", "'"],
        ["a", "s", "d", "f", "g", "h", "j", "k", "l", "ç", "@"],
        ["<", "z", "x", "c", "v", "b", "n", "m", ",", ".", "-"],
    ]
    shift = [
        ["|", "!", '"', "#", "$", "%", "&", "/", "(", ")", "?"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "O", "*", "="],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ç", "@"],
        [">", "Z", "X", "C", "V", "B", "N", "M", ";", ":", "_"],
    ]

    modifier = KeyboardState.NORMAL

    shift_btn = Button(50, 600, "Shift", 150)
    space_btn = Button(250, 600, "Space", 300)
    delete_btn = Button(1040, 200, "Delete", 170)
    submit_btn = Button(960, 600, "Enviar", 240)

    start_x = 50
    start_y = 200

    def draw(self, img, hands):
        match self.modifier:
            case KeyboardState.NORMAL:
                keys = self.keys
            case KeyboardState.SHIFT:
                keys = self.shift

        for y, keyset in enumerate(keys):
            for x, key in enumerate(keyset):
                if not key:
                    continue
                button = Button(
                    self.start_x + x * 90, self.start_y + y * 90, key, 80, 80
                )
                button.drawSimple(img, hands)
                for hand in hands:
                    if button.click(hand):
                        self.callback(key)

        self.shift_btn.drawSimple(img, hands)
        self.space_btn.drawSimple(img, hands)
        self.delete_btn.drawSimple(img, hands)
        self.submit_btn.drawSimple(img, hands)

        return img
