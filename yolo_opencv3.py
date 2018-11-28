#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################


import cv2
import argparse
import numpy as np

'''
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
'''
def start_yolo(image_path,config_path,weights_path,classes_path,first_server):

    cena = False

    global number_image 
    global distance 
    global image_ 
    global config_ 
    global weights_ 
    global classes_ 
    global KNOWN_DISTANCE   
    global KNOWN_WIDTH   
    global KNOWN_WPADRAO 
    global px_width  
    global px_wpadrao 
    focalLength = (px_width * KNOWN_DISTANCE) / KNOWN_WIDTH
    global focalLength_wpadrao 
    global W_IMAGE  
    global H_IMAGE  
    global error_rate
    global return_array 
    global image 
    global Width 
    global Height 
    global scale 
    global classes 
    global person_class_id 
    global COLORS 
    global net 
    global blob 
    global outs 
    global class_ids 
    global confidences 
    global boxes 
    global conf_threshold 
    global nms_threshold 
    global indices 
    return_array = []
    compare_array = []

    number_image = 0
    distance = 0

    image_ = None
    config_ = None
    weights_ = None
    classes_ = None

    #####FOR THE FIRST IMAGE

    # initialize the known distance from the camera to the object, which
    # in this case is 24 inches
    KNOWN_DISTANCE = 64  #1.65 metros = 165 cm

    # initialize the known object width, which in this case, the piece of
    # paper is 12 inches wide
    KNOWN_WIDTH = 66.0  #1.7 metros = 170 cm
    KNOWN_WPADRAO = 16  #40.64 cm

    px_width = 494 #pixel homem imagem
    px_wpadrao = 140 #pixel largura homem

    #focalLength = (px_width * KNOWN_DISTANCE) / KNOWN_WIDTH
    focalLength_wpadrao = (px_wpadrao * KNOWN_DISTANCE) / KNOWN_WPADRAO

    W_IMAGE = 468 #px
    H_IMAGE = 624 #px

    error_rate = 10 #px

    #####END FIRST IMAGE



    image = None


    Width = None
    Height = None
    scale = 0.00392

    classes = None
    person_class_id = 0

    COLORS = None
    net = None
    blob = None
    outs = None



    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
                

    indices = None


    image_ = image_path
    config_ = config_path
    weights_ = weights_path
    classes_ = classes_path

    return_array.clear()
    compare_array.clear()

    image = cv2.imread(image_)

    Width = image.shape[1]
    Height = image.shape[0]

    with open(classes_, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))


    net = cv2.dnn.readNet(weights_, config_)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    for out in outs:
        for detection in out:
           scores = detection[5:]
           class_id = np.argmax(scores)
           confidence = scores[class_id]
           if confidence > 0.5 and class_id == person_class_id:
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

    count = 0
    for i in indices:
       count = count +1 
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
       distance = distance_to_camera(KNOWN_WIDTH,focalLength, (round(y+h) - round(y)) )
       distance = inche_to_cm(distance)
       print(distance)
       if cena:
          print("on cena 01")
          compare_array.append(distance)
       elif distance < 1 and distance > 0:
          print("on <>")
          #print("%.2f" % distance)
          #distance = "%.2f" % distance
          compare_array.append(distance)
          #append_array(distance,return_array)
       else:
          print("on else")
          return_array.append("nothing\n") #longe
         
       draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))
       
    if cena:
        print("on cena")
        text = ""
        people = len(compare_array)
        if(people > 1): 
            text = "%d pessoas a " % people
        else: 
            text = "Uma pessoa a "

        for obj in compare_array:
            distance = "%.2f" % obj
            if obj == compare_array[-1]:
                text = text + " e %s metros." % distance
            else: 
                text = text + " %s metros," % distance
        return_array.append(text)
        return return_array
    
    if count == 0:
        print("nothing")
        return_array.append("nothing\n") #nothing
        return return_array

    if not compare_array:
        return_array.append("nothing\n") #longe
        return return_array
    else:
        menor_dist = float("inf")
        for menor in compare_array:
            if menor < menor_dist:
                menor_dist = menor
        distance = "%.2f" % menor_dist
        return_array.append("Uma pessoa a %s metros\n" % distance)
    
 
    #cv2.imshow("object detection", image)
    #cv2.waitKey(0)
    
    #cv2.imwrite("object-detection.jpg", image)
    #cv2.destroyAllWindows()

    if first_server:
        return start_yolo(image_path,config_path,weights_path,classes_path,False)

    return return_array

def append_array(distance_,return_array_):
    if(distance_ == ""):
       return_array_.append("longe\n")
    else:
       return_array_.append("Uma pessoa a %s metros\n" % distance_)

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])
    label = label + str(number_image) + " " + str(distance)

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

def inche_to_cm(inche):
    return (inche / 0.39370) / 100

def verify_height(x,y,h,w):
    h_ = round(y+h) - round(y)
    #w_ = round(x+w) - round(x)
    #if h_ >= H_IMAGE:
    #   return distance_to_camera(KNOWN_WPADRAO,focalLength_wpadrao, w_)
    #elif h_ < px_width:
    #   return analyze_width(w_,h_)
    #else:
    #   return distance_to_camera(KNOWN_WIDTH,focalLength, h_)
    return distance_to_camera(KNOWN_WIDTH,focalLength, h_)

def analyze_width(w_,h_):
    if w_ > (px_wpadrao + error_rate):
       distance_h = distance_to_camera(KNOWN_WIDTH,focalLength, h_)
       distance_w = distance_to_camera(KNOWN_WPADRAO,focalLength_wpadrao, w_)
       return (distance_h + distance_w) / 2
    else:
       return distance_to_camera(KNOWN_WIDTH,focalLength, h_)


number_image = 0
distance = 0

image_ = None
config_ = None
weights_ = None
classes_ = None

#####FOR THE FIRST IMAGE

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 64  #1.65 metros = 165 cm

# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 66.0  #1.7 metros = 170 cm
KNOWN_WPADRAO = 16  #40.64 cm

px_width = 494 #pixel homem imagem
px_wpadrao = 140 #pixel largura homem

#focalLength = (px_width * KNOWN_DISTANCE) / KNOWN_WIDTH
focalLength_wpadrao = (px_wpadrao * KNOWN_DISTANCE) / KNOWN_WPADRAO

W_IMAGE = 468 #px
H_IMAGE = 624 #px

error_rate = 10 #px

#####END FIRST IMAGE



image = None


Width = None
Height = None
scale = 0.00392

classes = None
person_class_id = 0

COLORS = None
net = None
blob = None
outs = None



class_ids = []
confidences = []
boxes = []
conf_threshold = 0.5
nms_threshold = 0.4
            

indices = None



