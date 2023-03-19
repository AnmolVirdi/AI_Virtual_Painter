import cv2
import numpy as np
import time
import tensorflow as tf

labels = ['lollipop', 'apple', 'diamond', 'helmet', 'skull', 'lipstick', 'cat', 'rhinoceros', 'peanut', 'pond', 'ant', 'jacket', 'blueberry', 'microwave', 'tree', 'paintbrush', 'butterfly', 'crown', 'leaf', 'boomerang', 'drill', 'toaster', 'lightning', 'toe', 'sword', 'fork', 'pear', 'hand', 'fireplace', 'sandwich', 'strawberry', 'raccoon', 'bench', 'piano', 'basket', 'chandelier', 'The Mona Lisa', 'elbow', 'coffee cup', 'sun', 'cactus', 'car', 'crab', 'cello', 'peas', 'pig', 'tractor', 'hammer', 'ocean', 'hockey puck', 'smiley face', 'canoe', 'screwdriver', 'river', 'picture frame', 'feather', 'hot air balloon', 'snail', 'sleeping bag', 'eye', 'bed', 'violin', 'tooth', 'yoga', 'rain', 'cup', 'calendar', 'stereo', 'radio', 'angel', 'trombone', 'snowman', 'sweater', 'frying pan', 'microphone', 'calculator', 'camouflage', 'shovel', 'television', 'hourglass', 'saw', 'rollerskates', 'bottlecap', 'steak', 'donut', 'hot tub', 'eraser', 'mushroom', 'squiggle', 'stethoscope', 'rifle', 'dog', 'clarinet', 'bee', 'belt', 'face', 'couch', 'foot', 'spreadsheet', 'dolphin', 'washing machine', 'The Eiffel Tower', 'alarm clock', 'scorpion', 'postcard', 'onion', 'garden', 'candle', 'speedboat', 'paper clip', 'giraffe', 'bear', 'grass', 'flower', 'harp', 'potato', 'bridge', 'mailbox', 'penguin', 'zebra', 'camera', 'drums', 'underwear', 'moustache', 'baseball', 'animal migration', 'sheep', 'square', 'floor lamp', 'panda', 'hockey stick', 'mosquito', 'lobster', 'diving board', 'duck', 'shoe', 'moon', 'trumpet', 'church', 'camel', 'owl', 'tiger', 'baseball bat', 'rake', 'blackberry', 'lantern', 'firetruck', 'van', 'streetlight', 'whale', 'stitches', 'oven', 'crayon', 'ice cream', 'crocodile', 'guitar', 'chair', 'wheel', 'sink', 'windmill', 'helicopter', 'school bus', 'bus', 'headphones', 'dishwasher', 'triangle', 'dresser', 'matches', 'ladder', 'nose', 'mouth', 'snowflake', 'sailboat', 'roller coaster', 'key', 'motorbike', 'hexagon', 'snorkel', 'basketball', 'ambulance', 'paint can', 'power outlet', 'vase', 'zigzag', 'submarine', 'megaphone', 'watermelon', 'beard', 'passport', 'stop sign', 'telephone', 'tent', 'mouse', 'ear', 'saxophone', 'pants', 'pickup truck', 'bowtie', 'toilet', 'tornado', 'stove', 'envelope', 'teddy-bear', 'star', 'flip flops', 'hospital', 'pillow', 'garden hose', 't-shirt', 'map', 'truck', 'campfire', 'barn', 'bucket', 'bird', 'parachute', 'wristwatch', 'cooler', 'sock', 'palm tree', 'shorts', 'line', 'table', 'waterslide', 'soccer ball', 'grapes', 'octagon', 'fence', 'skyscraper', 'parrot', 'see saw', 'nail', 'airplane', 'tennis racquet', 'kangaroo', 'skateboard', 'cloud', 'wine glass', 'mug', 'book', 'rainbow', 'string bean', 'leg', 'dragon', 'syringe', 'suitcase', 'train', 'jail', 'umbrella', 'house', 'spider', 'binoculars', 'broom', 'brain', 'monkey', 'flashlight', 'golf club', 'eyeglasses', 'broccoli', 'spoon', 'bread', 'lighthouse', 'circle', 'hat', 'rabbit', 'scissors', 'ceiling fan', 'mermaid', 'bathtub', 'cookie', 'compass', 'asparagus', 'bat', 'bush', 'fan', 'knee', 'flying saucer', 'cannon', 'cruise ship', 'banana', 'swan', 'octopus', 'beach', 'axe', 'castle', 'hamburger', 'backpack', 'toothpaste', 'bicycle', 'police car', 'aircraft carrier', 'arm', 'frog', 'laptop', 'The Great Wall of China', 'wine bottle', 'mountain', 'marker', 'hurricane', 'lighter', 'computer', 'birthday cake', 'hedgehog', 'anvil', 'purse', 'pizza', 'sea turtle', 'hot dog', 'toothbrush', 'horse', 'swing set', 'popsicle', 'pool', 'house plant', 'light bulb', 'flamingo', 'fish', 'stairs', 'pineapple', 'squirrel', 'goatee', 'bracelet', 'traffic light', 'finger', 'cow', 'remote control', 'pencil', 'teapot', 'keyboard', 'cake', 'pliers', 'lion', 'clock', 'bulldozer', 'necklace', 'cell phone', 'carrot', 'shark', 'door', 'snake', 'knife', 'elephant', 'bandage', 'fire hydrant', 'dumbbell']
labels.sort()

def predict_image(canvas):
    try:
        # Cut, convert to grayscale, resize
        canvas = canvas[0:300, 0:300]
        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        canvas = cv2.bitwise_not(canvas)
        canvas = cv2.resize(canvas, (28, 28))

        # Save 28x28 image to file
        timestamp = time.time()
        filename = f'images/{timestamp}.png'
        cv2.imwrite(filename, canvas)

        # Reshape
        canvas = canvas.reshape(1, 28, 28, 1)
        canvas = canvas.astype('float32')

        # Load TFLite model and allocate tensors
        interpreter = tf.lite.Interpreter(model_path="cnn-model/model.tflite")
        interpreter.allocate_tensors()

        # Set input tensor
        input_details = interpreter.get_input_details()
        interpreter.set_tensor(input_details[0]['index'], canvas)

        # Run inference
        interpreter.invoke()

        # Get output tensor
        output_details = interpreter.get_output_details()
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predictions = output_data.reshape(-1)  # Flatten the output tensor

        # Get the top 3 predictions
        top3_indices = np.argsort(predictions)[::-1][:3]  # Get the indices of top 3 predictions
        top3 = []
        for i in top3_indices:
            top3.append({
                'probability': float(predictions[i]),
                'object': labels[i],
                'index': i
            })

        top3.sort(key=lambda x: x['probability'], reverse=True)  # Sort top 3 predictions by probability
        
        print(top3)
        return top3
        
    except Exception as e:
        print(f"Error: {e}")

