import numpy as np
import time
import tensorflow as tf
import random
import cv2
import json

# Saved array of labels
# labels = ['The Eiffel Tower', 'The Great Wall of China', 'The Mona Lisa', 'aircraft carrier', 'airplane', 'alarm clock', 'ambulance', 'angel', 'animal migration', 'ant', 'anvil', 'apple', 'arm', 'asparagus', 'axe', 'backpack', 'banana', 'bandage', 'barn', 'baseball', 'baseball bat', 'basket', 'basketball', 'bat', 'bathtub', 'beach', 'bear', 'beard', 'bed', 'bee', 'belt', 'bench', 'bicycle', 'binoculars', 'bird', 'birthday cake', 'blackberry', 'blueberry', 'book', 'boomerang', 'bottlecap', 'bowtie', 'bracelet', 'brain', 'bread', 'bridge', 'broccoli', 'broom', 'bucket', 'bulldozer', 'bus', 'bush', 'butterfly', 'cactus', 'cake', 'calculator', 'calendar', 'camel', 'camera', 'camouflage', 'campfire', 'candle', 'cannon', 'canoe', 'car', 'carrot', 'castle', 'cat', 'ceiling fan', 'cell phone', 'cello', 'chair', 'chandelier', 'church', 'circle', 'clarinet', 'clock', 'cloud', 'coffee cup', 'compass', 'computer', 'cookie', 'cooler', 'couch', 'cow', 'crab', 'crayon', 'crocodile', 'crown', 'cruise ship', 'cup', 'diamond', 'dishwasher', 'diving board', 'dog', 'dolphin', 'donut', 'door', 'dragon', 'dresser', 'drill', 'drums', 'duck', 'dumbbell', 'ear', 'elbow', 'elephant', 'envelope', 'eraser', 'eye', 'eyeglasses', 'face', 'fan', 'feather', 'fence', 'finger', 'fire hydrant', 'fireplace', 'firetruck', 'fish', 'flamingo', 'flashlight', 'flip flops', 'floor lamp', 'flower', 'flying saucer', 'foot', 'fork', 'frog', 'frying pan', 'garden', 'garden hose', 'giraffe', 'goatee', 'golf club', 'grapes', 'grass', 'guitar', 'hamburger', 'hammer', 'hand', 'harp', 'hat', 'headphones', 'hedgehog', 'helicopter', 'helmet', 'hexagon', 'hockey puck', 'hockey stick', 'horse', 'hospital', 'hot air balloon', 'hot dog', 'hot tub', 'hourglass', 'house', 'house plant', 'hurricane', 'ice cream', 'jacket', 'jail', 'kangaroo', 'key', 'keyboard', 'knee', 'knife', 'ladder', 'lantern', 'laptop', 'leaf', 'leg', 'light bulb', 'lighter', 'lighthouse', 'lightning', 'line', 'lion', 'lipstick', 'lobster', 'lollipop', 'mailbox', 'map', 'marker', 'matches', 'megaphone', 'mermaid', 'microphone', 'microwave', 'monkey', 'moon', 'mosquito', 'motorbike', 'mountain', 'mouse', 'moustache', 'mouth', 'mug', 'mushroom', 'nail', 'necklace', 'nose', 'ocean', 'octagon', 'octopus', 'onion', 'oven', 'owl', 'paint can', 'paintbrush', 'palm tree', 'panda', 'pants', 'paper clip', 'parachute', 'parrot', 'passport', 'peanut', 'pear', 'peas', 'pencil', 'penguin', 'piano', 'pickup truck', 'picture frame', 'pig', 'pillow', 'pineapple', 'pizza', 'pliers', 'police car', 'pond', 'pool', 'popsicle', 'postcard', 'potato', 'power outlet', 'purse', 'rabbit', 'raccoon', 'radio', 'rain', 'rainbow', 'rake', 'remote control', 'rhinoceros', 'rifle', 'river', 'roller coaster', 'rollerskates', 'sailboat', 'sandwich', 'saw', 'saxophone', 'school bus', 'scissors', 'scorpion', 'screwdriver', 'sea turtle', 'see saw', 'shark', 'sheep', 'shoe', 'shorts', 'shovel', 'sink', 'skateboard', 'skull', 'skyscraper', 'sleeping bag', 'smiley face', 'snail', 'snake', 'snorkel', 'snowflake', 'snowman', 'soccer ball', 'sock', 'speedboat', 'spider', 'spoon', 'spreadsheet', 'square', 'squiggle', 'squirrel', 'stairs', 'star', 'steak', 'stereo', 'stethoscope', 'stitches', 'stop sign', 'stove', 'strawberry', 'streetlight', 'string bean', 'submarine', 'suitcase', 'sun', 'swan', 'sweater', 'swing set', 'sword', 'syringe', 't-shirt', 'table', 'teapot', 'teddy-bear', 'telephone', 'television', 'tennis racquet', 'tent', 'tiger', 'toaster', 'toe', 'toilet', 'tooth', 'toothbrush', 'toothpaste', 'tornado', 'tractor', 'traffic light', 'train', 'tree', 'triangle', 'trombone', 'truck', 'trumpet', 'umbrella', 'underwear', 'van', 'vase', 'violin', 'washing machine', 'watermelon', 'waterslide', 'whale', 'wheel', 'windmill', 'wine bottle', 'wine glass', 'wristwatch', 'yoga', 'zebra', 'zigzag']


class Dataset:
    def __init__(self):
        f = open("data/labels2.json", "r")
        self.labels_obj = json.load(f)
        self.labels = list(self.labels_obj.keys())
        f.close()

    def get_random_word(self):
        choice = random.choice(self.labels)
        name_pt = self.labels_obj[choice]
        name_pt = name_pt[0].upper() + name_pt[1:]  # Capitalize first letter

        return {
            "index": self.labels.index(choice),
            "name": choice,
            "name_pt": name_pt,
        }

    def get_compare_percentage(self, predictions, object_id):
        return int(float(predictions[object_id]) * 100)

    def get_top3(self, predictions):
        top3_indices = np.argsort(predictions)[::-1][
            :3
        ]  # Get the indices of top 3 predictions

        top3 = list(
            map(
                lambda x: {
                    "index": x,
                    "probability": int(float(predictions[x]) * 100),
                    "name": self.labels[x],
                    "name_pt": self.labels_obj[self.labels[x]],
                },
                top3_indices,
            )
        )

        top3.sort(
            key=lambda x: x["probability"], reverse=True
        )  # Sort top 3 predictions by probability

        print(top3)
        return top3

    def get_predicts(self, canvas):
        try:
            square_size = 470
            top, left = 140, 240
            # Cut, convert to grayscale, resize
            canvas = canvas[top : (top + square_size), left : (left + square_size)]
            canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
            canvas = cv2.bitwise_not(canvas)
            canvas = cv2.resize(canvas, (28, 28))

            # read image from images/pear.png
            # canvas = cv2.imread('images/pear.png', cv2.IMREAD_GRAYSCALE)

            timestamp = time.time()
            filename = f"images/{timestamp}.png"
            cv2.imwrite(filename, canvas)

            # Reshape
            canvas = canvas.reshape(1, 28, 28, 1)
            canvas = canvas.astype("float32")

            # Load TFLite model and allocate tensors
            interpreter = tf.lite.Interpreter(model_path="cnn-model/model2.tflite")
            interpreter.allocate_tensors()

            # Set input tensor
            input_details = interpreter.get_input_details()
            interpreter.set_tensor(input_details[0]["index"], canvas)

            # Run inference
            interpreter.invoke()

            # Get output tensor
            output_details = interpreter.get_output_details()
            output_data = interpreter.get_tensor(output_details[0]["index"])
            predictions = output_data.reshape(-1)  # Flatten the output tensor
            return predictions

        except Exception as e:
            print(f"Error: {e}")
