# ia-image-recognition
Trabalho de Medida de Eficiência da disciplina de Inteligência Artificial

Integrantes do Grupo: <br/>
Adrian Newey Santos, <br/>
André Arthur da Rocha, <br/>
Breno Souza Costa, <br/>
Elder de Jesus Sales.<br/>
<br/>
O projeto tem como finalidade auxiliar deficientes visuais na identificacao de obstaculos a sua frente. O app utiliza vocalizacao para comunicacao, informando o usuario se ha um obstaculo proximo.
<br/>
Utiliza-se de conceitos como:<br/>
-Redes Neurais Convulacionais<br/>
-Identificacao de Objetos utilizando framework YOLO<br/>
-Detectar distancia de objetos da camera<br/>

## Pre-requisites

Python 3 with Numpy - https://www.python.org/ 
<br/>
OpenCV and OpenCV Python bindings- https://opencv.org/
<br/>
Java - https://www.java.com/pt_BR/

#### Yolo: Real-Time Object Detection

Link: https://pjreddie.com/darknet/yolo/
<br/>
Baixar arquivos Weights e Cfg - "yolov3.weights, yolov3.cfg" - e colocar no mesmo diretorio do repositorio.
<br/>
E possivel em utilizar GPU com o YOLO. Para poder utilizar com placas Nvidia baixe o CUDA.

#### Android

Possuir Android Studio e Android SDK

## Usage

Instale em um dispositivo o app CameraView

Rode o script server.py

Abra o app em um smartphone.

Obs: É preciso alterar no código o ip do servidor e do socket (server.py e sendFile.java).
