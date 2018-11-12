import yolo_opencv3 as yolo
import socket                   # Import socket module
import os

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
#host = socket.gethostname()     # Get local machine name
host = '192.168.1.103'
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

IMAGE_ID = "send_image"
TY_CON = 'Thank you for connecting'
BEGIN = "begin\n"
QUIT = "quit\n"

image_path = "images/received_file.jpg"
config_path = "yolov3.cfg"
weights_path = "yolov3.weights"
classes_path = "yolov3.txt"


print('Server listening....')

while True:
    con, cliente = s.accept()
    print('Concetado por', cliente)
   
    with open('images/received_file.jpg', 'wb') as f:
       print('receiving data...')
       while True:
          data = con.recv(1024)
          if not data:
             break
          # write data to a file
          f.write(data)
    f.close()
    print('Successfully get the file')
    #os.system("python3 yolo_opencv2.py --image images/received_file.jpg --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt")

    list_result = yolo.start_yolo(image_path,config_path,weights_path,classes_path)
    #print(list[0])


    con.send(BEGIN.encode())
    for raw in list_result:
        print(raw)
        con.send(raw.encode())
    con.send(QUIT.encode())

    print('Done sending')
    #con.send(TY_CON.encode())
    del list_result[:]
    con.close()       
