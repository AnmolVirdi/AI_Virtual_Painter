from Brush import Brush

class PositionHistory:
    def __init__(self, size):
        self.size = size
        self.last_positions = [] #list of positions

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
        distances = [((a[0]-b[0])**2 + (a[1]-b[1])**2) for a, b in zip(index_history, thumb_history)]
        derivative = [distances[i+1]-distances[i] for i in range(len(distances)-1)]
        if derivative:
            return min(derivative)
        else:
            return 0
        
    def reset(self):
        self.last_positions = []

class Hand:
    history = PositionHistory(5)

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

    def update_positions(self, positions, fingers_up):
        self.parse_positions(positions)
        self.fingers_up = fingers_up
        self.history.add(self.finger_positions)

    def indicator_up(self):
        return self.fingers_up[1:5] == [0,1,1,1]

    def indicator_and_midle_up(self):
        return self.fingers_up[1]==0 and self.fingers_up[2]==0

    def middle_finger(self):
        return self.fingers_up[2]==0 and not(False in [self.fingers_up[x]==1 for x in [1, 3, 4]])

    def count_fingers_up(self):
        return self.fingers_up[1:5].count(0)

    def clicked(self):
        thumb_x, thumb_y = self.finger_positions[0]
        indicator_x, indicator_y = self.finger_positions[1]

        if (indicator_x-thumb_x)**2 + (indicator_y-thumb_y)**2 < 1500:
            if(self.history.derivative() < -1500):
                print("Clicked!")
                self.history.reset()
                return True
        return False

    def update_reference_points(self):
        self.last_drawn = self.finger_positions[1]

    def blur(self):
        print("asd")

