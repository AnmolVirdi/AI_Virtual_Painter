from Brush import Brush

class Hand:
    def __init__(self, brush: Brush, finger_positions, fingers_up) -> None:
        self.brush = brush
        self.update_positions(finger_positions, fingers_up)
        self.last_drawn = None

    def parse_positions(self, positions):
        self.wrist_position = positions[0][1:3]
        #tipIDs=[4,8,12,16,20] #Finger tip IDs
        self.finger_positions = [
            #Thumb finder tip coordinates(landmark number 4)
            positions[4][1:3],
            #Index finger tip coordinates(landmark number 8)
            positions[8][1:3],
            #Middle finger tip coordinates(landmark number 12)
            positions[12][1:3],
            #Ring finger tip coordinates(landmark number 16)
            positions[16][1:3],
            #Pinky finger tip coordinates(landmark number 20)
            positions[20][1:3],
        ]
        self.all_positions = positions

    @property
    def thumb_tip_position(self):
        return self.finger_positions[0]
    
    @property
    def index_tip_position(self):
        return self.finger_positions[1]

    @property
    def middle_tip_position(self):
        return self.finger_positions[2]

    @property
    def ring_tip_position(self):
        return self.finger_positions[3]

    @property
    def pinky_tip_position(self):
        return self.finger_positions[4]

    def update_positions(self, positions, finger_positions):
        self.parse_positions(positions)
        self.fingers_up = finger_positions

    def indicator_up(self):
        return self.fingers_up[1:5] == [0,1,1,1]

    def indicator_and_midle_up(self):
        return self.fingers_up[1]==0 and self.fingers_up[2]==0

    def middle_finger_up(self):
        return self.fingers_up[2]==0 and not(False in [self.fingers_up[x]==1 for x in [1, 3, 4]])

    def count_fingers_up(self):
        return self.fingers_up[1:5].count(0)

    # Converging or State machine
    def clicked(self):
        thumb_x, thumb_y = self.finger_positions[0]
        indicator_x, indicator_y = self.finger_positions[1]

        return (indicator_x-thumb_x)**2 + (indicator_y-thumb_y)**2 < (1500)

    def update_reference_points(self):
        self.last_drawn = self.finger_positions[1]

    def get_bounding_box(self):
        x_coordinates = [x[1] for x in self.all_positions]
        y_coordinates = [x[2] for x in self.all_positions]
        x_min, x_max = min(x_coordinates), max(x_coordinates)
        y_min, y_max = min(y_coordinates), max(y_coordinates)

        extra = 10
        x_min -= extra
        x_max += extra
        y_min -= extra
        y_max += extra
        
        return x_min, x_max, y_min, y_max
