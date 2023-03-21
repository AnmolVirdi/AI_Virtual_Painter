from typing import ClassVar
from Brush import Brush

FingerPosition = int

UP = 0
DOWN = 1


class Hand:
    THUMB: ClassVar[FingerPosition] = 0
    INDEX: ClassVar[FingerPosition] = 1
    MIDDLE: ClassVar[FingerPosition] = 2
    RING: ClassVar[FingerPosition] = 3
    PINKY: ClassVar[FingerPosition] = 4

    def __init__(self, brush: Brush, finger_positions, fingers_up) -> None:
        self.brush = brush
        self.update_positions(finger_positions, fingers_up)
        self.last_drawn = None

    def parse_positions(self, positions):
        self.wrist_position = positions[0][1:3]
        # tipIDs=[4,8,12,16,20] #Finger tip IDs
        self.finger_positions = [
            # Thumb finder tip coordinates(landmark number 4)
            positions[4][1:3],
            # Index finger tip coordinates(landmark number 8)
            positions[8][1:3],
            # Middle finger tip coordinates(landmark number 12)
            positions[12][1:3],
            # Ring finger tip coordinates(landmark number 16)
            positions[16][1:3],
            # Pinky finger tip coordinates(landmark number 20)
            positions[20][1:3],
        ]

    @property
    def thumb_tip_position(self):
        return self.finger_positions[Hand.THUMB]

    @property
    def index_tip_position(self):
        return self.finger_positions[Hand.INDEX]

    @property
    def middle_tip_position(self):
        return self.finger_positions[Hand.MIDDLE]

    @property
    def ring_tip_position(self):
        return self.finger_positions[Hand.RING]

    @property
    def pinky_tip_position(self):
        return self.finger_positions[Hand.PINKY]

    def update_positions(self, positions, finger_positions):
        self.parse_positions(positions)
        self.fingers_up = finger_positions

    def finger(self, finger: FingerPosition):
        return self.fingers_up[finger]

    def finger_up(self, finger: FingerPosition):
        return self.finger(finger) == UP

    def finger_down(self, finger: FingerPosition):
        return self.finger(finger) == DOWN

    def indicator_up(self):
        return (
            self.finger_up(Hand.INDEX)
            and self.finger_down(Hand.MIDDLE)
            and self.finger_down(Hand.RING)
            and self.finger_down(Hand.PINKY)
        )

    def indicator_and_middle_up(self):
        return (
            self.finger_up(Hand.INDEX)
            and self.finger_up(Hand.MIDDLE)
            and self.finger_down(Hand.RING)
            and self.finger_down(Hand.PINKY)
        )

    def middle_finger(self):
        return (
            self.finger_down(Hand.INDEX)
            and self.finger_up(Hand.MIDDLE)
            and self.finger_down(Hand.RING)
            and self.finger_down(Hand.PINKY)
        )

    def count_fingers_up(self):
        return self.fingers_up[1:5].count(UP)

    # Converging or State machine
    def clicked(self):
        thumb_x, thumb_y = self.finger_positions[0]
        indicator_x, indicator_y = self.finger_positions[1]

        return (indicator_x - thumb_x) ** 2 + (indicator_y - thumb_y) ** 2 < (1500)

    def set_brush(self, brush: Brush):
        self.brush = brush

    def update_reference_points(self):
        self.last_drawn = self.finger_positions[1]

    def blur(self):
        print("asd")
