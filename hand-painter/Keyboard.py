from enum import Enum
from Button import Button

class KeyboardKey:
    def __init__(self, key, alt) -> None:
        self.key = key
        self.alt = alt

class KeyboardState(Enum):
    NORMAL = 0
    SHIFT = 1
    ALT = 2

class Keyboard:


    keys = [
        ["\\", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "'", "«"],
        ["q","w","e","r","t","y","u","i","o","p", "+", "'"],
        ["a","s","d","f","g","h","j","k","l","ç"],
        ["<","z","x","c","v","b","n","m",",",".","-"],
    ]
    shift = [
        ["|","!","\"","#", "$", "%", "&", "/", "(", ")", "=", "?", "»",],
        ["Q","W","E","R","T","Y","U","I","O","O", "*", "`"],
        ["A","S","D","F","G","H","J","K","L","Ç"],
        [">","Z","X","C","V","B","N","M",";",":","_"],
    ]

    alt = [
        [None, None, "@", "£", "§", None, None, "{", "[", "]", "}", None, "«"],
        [None, None, None, None, None, None, None, None, None, None]
    ]

    modifier = KeyboardState.NORMAL

    shift_btn = Button(50, 600, "Shift", 150)
    space_btn = Button(250, 600, "Space", 150)
    alt_btn = Button(450, 600, "Alt", 100)
    delete_btn = Button(600, 600, "Delete", 150)
    submit_btn = Button(1000, 600, "Submit", 200)

    start_x = 50
    start_y = 200

    def draw(self, img):
        match self.modifier:
            case KeyboardState.NORMAL:
                keys = self.keys
            case KeyboardState.SHIFT:
                keys = self.shift
            case KeyboardState.ALT:
                keys = self.alt

        for y, keyset in enumerate(keys):
            for x, key in enumerate(keyset):
                if not key:
                    continue
                button = Button(self.start_x + x*90, self.start_y +y * 90, key, 80, 80)
                button.draw(img)
    
        text_field_ui = Button(50, 50, "andre.julio.moreira@hotmail.com") # ?????
        text_field_ui.draw(img)

        self.shift_btn.draw(img)
        self.space_btn.draw(img)
        self.alt_btn.draw(img)
        self.delete_btn.draw(img)
        self.submit_btn.draw(img)

        return img
