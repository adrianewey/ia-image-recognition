import cv2
import argparse
import numpy as np
number_image = 0
distance = 0
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'path to input image')
ap.add_argument('-c', '--config', required=True,
                help = 'path to yolo config file')
ap.add_argument('-w', '--weights', required=True,
                help = 'path to yolo pre-trained weights')
ap.add_argument('-cl', '--classes', required=True,
                help = 'path to text file containing class names')
args = ap.parse_args()


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])
    #label = label + str(number_image) + " " + str(distance)

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

def inche_to_cm(inche):
    return (inche / 0.39370) / 100


#####FOR THE FIRST IMAGE

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 64  #1.65 metros = 165 cm

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 66.0  #1.7 metros = 170 cm

px_width = 494 #pixel homem imagem

focalLength = (px_width * KNOWN_DISTANCE) / KNOWN_WIDTH



#####END FIRST IMAGE


image = cv2.imread(args.image)

Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

classes = None
person_class_id = 0

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


net = cv2.dnn.readNet(args.weights, args.config)

blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

net.setInput(blob)

outs = net.forward(get_output_layers(net))

class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4


for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * Width)
            center_y = int(detection[1] * Height)
            w = int(detection[2] * Width)
            h = int(detection[3] * Height)
            x = center_x - w / 2
            y = center_y - h / 2
            print(class_id)
            class_ids.append(class_id)
            confidences.append(float(confidence))
            boxes.append([x, y, w, h])
            px_width = (x + y) #pixel distance for distance calculation
            
            
            #print(px_width)
            


indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

for i in indices:
    i = i[0]
    box = boxes[i]
    x = box[0]
    y = box[1]
    w = box[2]
    h = box[3]
    print(number_image)
    print(round(y+h) - round(y))
    print(round(x+w) - round(x))
    number_image = number_image + 1
    distance = distance_to_camera(KNOWN_WIDTH,focalLength, (round(y+h) - round(y)) )
    distance = "%.2f" % inche_to_cm(distance)
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

cv2.imshow("object detection", image)
cv2.waitKey(0)
    
cv2.imwrite("object-detection.jpg", image)
cv2.destroyAllWindows()
