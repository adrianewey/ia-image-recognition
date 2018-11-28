import yolo_opencv3 as yolo	# Import yolo_opencv script
import socket                   # Import socket module
import os

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
#host = socket.gethostname()    # Get local machine name
host = '10.144.210.86'	 	# set local ip
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.


#Variaveis de controle
BEGIN = "begin\n"
QUIT = "quit\n"
PULAR = "\n"

image_path = "images/received_file.jpg" #local onde a imagem recebida sera salva 
config_path = "yolov3.cfg"              #local onde a cfg do yolo está
weights_path = "yolov3.weights"         #local onde os pesos do yolo estão
classes_path = "yolov3.txt"             #local onde arquivo txt para classes do yolo estão
list_result = []

print('Server listening....')

first_server = True     #Variavel para controle

while True:
    con, cliente = s.accept()                           #Recebe a conexão do cliente
    print('Concetado por', cliente)
   
    with open('images/received_file.jpg', 'wb') as f:   #cria arquivo da imagem
       print('receiving data...')
       while True:
          data = con.recv(1024)                         #recebe a imagem
          if not data:
             break
          f.write(data)                                 #escreve no arquivo criado
    f.close()                                           #fecha conexão com o arquivo
    print('Successfully get the file')

    #Usado para detectar objetos apenas para visualização
    #os.system("python3 yolo_opencv.py --image images/received_file.jpg --config yolov3.cfg --weights yolov3.weights --classes yolov3.txt")

    # Retorno do método que identifica e textualiza os objetos encontrados
    list_result = []
    list_result = yolo.start_yolo(image_path,config_path,weights_path,classes_path,first_server)
    #print(list[0])


    # Código para enviar o texto para o cliente
    con.send(BEGIN.encode())        # envia variavel de controle
    for raw in list_result:
        print(raw)
        con.send(raw.encode())      # envia o texto
    con.send(PULAR.encode())        # envia variavel de controle
    con.send(QUIT.encode())         # envia variavel de controle

    print('Done sending')
    first_server = False   # variavel de controle
    del list_result[:]      # reseta lista de texto
    con.close()             #fecha conexão com cliente