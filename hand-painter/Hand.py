from typing import ClassVar
from Brush import Brush


class PositionHistory:
    def __init__(self, size):
        self.size = size
        self.last_positions = []  # list of positions

    def add(self, positions):
        self.last_positions.append(positions)
        if len(self.last_positions) > self.size:
            self.last_positions.pop(0)
        self.derivative()

    def get(self):
        return self.last_positions

    def derivative(self):
        thumb_history = [x[0] for x in self.last_positions]
        index_history = [x[1] for x in self.last_positions]
        distances = [
            ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
            for a, b in zip(index_history, thumb_history)
        ]
        derivative = [distances[i] - distances[i - 1] for i in range(1, len(distances))]

        if derivative:
            return min(derivative)
        else:
            return 0

    def reset(self):
        self.last_positions = []


FingerPosition = int

UP = 0
DOWN = 1


class Hand:
    THUMB: ClassVar[FingerPosition] = 0
    INDEX: ClassVar[FingerPosition] = 1
    MIDDLE: ClassVar[FingerPosition] = 2
    RING: ClassVar[FingerPosition] = 3
    PINKY: ClassVar[FingerPosition] = 4

    def __init__(
        self, brush: Brush, finger_positions, fingers_up, hand_offset_ratio=(1, 1)
    ) -> None:
        self.brush = brush
        self.update_positions(finger_positions, fingers_up, hand_offset_ratio)
        self.last_drawn = None
        self.history = PositionHistory(5)
        self.previous_brush = None

    def parse_positions(self, positions, offset_ratio=(0, 0)):
        offset_x_ratio, offset_y_ratio = offset_ratio

        self.wrist_position = (
            positions[0][1] * offset_x_ratio,
            positions[0][2] * offset_y_ratio,
        )
        # tipIDs=[4,8,12,16,20] #Finger tip IDs
        self.finger_positions = [
            # Thumb finder tip coordinates(landmark number 4)
            (
                int(positions[4][1] * offset_x_ratio),
                int(positions[4][2] * offset_y_ratio),
            ),
            # Index finger tip coordinates(landmark number 8)
            (
                int(positions[8][1] * offset_x_ratio),
                int(positions[8][2] * offset_y_ratio),
            ),
            # Middle finger tip coordinates(landmark number 12)
            (
                int(positions[12][1] * offset_x_ratio),
                int(positions[12][2] * offset_y_ratio),
            ),
            # Ring finger tip coordinates(landmark number 16)
            (
                int(positions[16][1] * offset_x_ratio),
                int(positions[16][2] * offset_y_ratio),
            ),
            # Pinky finger tip coordinates(landmark number 20)
            (
                int(positions[20][1] * offset_x_ratio),
                int(positions[20][2] * offset_y_ratio),
            ),
        ]
        self.all_positions = positions
        self.offset_ratio = offset_ratio

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

    def update_positions(self, positions, fingers_up, offset=(1, 1)):
        self.parse_positions(positions, offset)
        self.fingers_up = fingers_up
        if not hasattr(self, "history"):
            self.history = PositionHistory(5)
        self.history.add(self.finger_positions)

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

    def clicked(self):
        thumb_x, thumb_y = self.finger_positions[0]
        indicator_x, indicator_y = self.finger_positions[1]

        if (indicator_x - thumb_x) ** 2 + (indicator_y - thumb_y) ** 2 < 1500:
            if self.history.derivative() < -1500:
                print("Clicked!")
                self.history.reset()
                return True
        return False

    def set_brush(self, brush: Brush):
        self.brush = brush

    def update_reference_points(self):
        self.last_drawn = self.finger_positions[1]

    def get_bounding_box(self):
        offset_x, offset_y = self.offset_ratio

        x_coordinates = [int(x[1] * offset_x) for x in self.all_positions]
        y_coordinates = [int(x[2] * offset_y) for x in self.all_positions]
        x_min, x_max = min(x_coordinates), max(x_coordinates)
        y_min, y_max = min(y_coordinates), max(y_coordinates)

        extra = 10
        x_min -= extra
        x_max += extra
        y_min -= extra
        y_max += extra

        return x_min, x_max, y_min, y_max
