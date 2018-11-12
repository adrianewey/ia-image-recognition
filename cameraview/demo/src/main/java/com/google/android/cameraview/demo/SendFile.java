package com.google.android.cameraview.demo;

import android.os.AsyncTask;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.net.Socket;
import java.util.ArrayList;

public class SendFile extends AsyncTask {
    private Socket socket;
    private File file;
    public String status = "default";
    public MainActivity mainActivity;

    private String host = "192.168.1.103";
    private int port = 60000;



    public SendFile(){

        /*try {
            socket = new Socket(host,port);
            System.out.println("Connected");
        } catch (IOException e) {
            System.out.println("Not Connected");
            e.printStackTrace();
        }*/
    }

    @Override
    protected Boolean doInBackground(Object[] objects) {
        try {
            connectSocket();

            sendPicture();

            receiveAnswer();
            socket.close();

            //mainActivity.mCameraView.takePicture();
            return true;
        } catch (IOException e) {
            e.printStackTrace();
        }


        return null;
    }

    private boolean wait = true;
    private ArrayList<String> answers;

    private void receiveAnswer(){
        answers = new ArrayList<>();
        String raw = "";
        try {
            DataInputStream dis = new DataInputStream(socket.getInputStream());

            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            System.out.println("Passou buffer");
            while(wait) {
                String message = input.readLine();

                if (message.equals("begin")) {
                    System.out.println("BEGIN RECEIVED");
                    while (true) {
                        System.out.println("BEFORE");
                        raw = input.readLine();
                        if (raw.equals("quit")){
                            System.out.println("BREAK");
                            wait = false;
                            break;
                        }
                        answers.add(raw);
                        System.out.println(raw);
                    }
                    wait = false;
                    mainActivity.speechResult(answers);
                    socket.shutdownInput();
                    socket.close();
                }
                //System.out.println(message);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    private void connectSocket(){
        try {
            socket = new Socket(host,port);
            System.out.println("Connected");
        } catch (IOException e) {
            e.printStackTrace();
            System.out.println("FAIL CONE");
        }

    }

    public void setFile(File file){
        this.file = file;
    }

    public void sendPicture() throws IOException{
        DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
        FileInputStream fis = new FileInputStream(file);
        byte[] buffer = new byte[4096];

        while (fis.read(buffer) > 0) {
            dos.write(buffer);
        }

        fis.close();
        socket.shutdownOutput();


    }

    public void closeConnection(){
        try {
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
