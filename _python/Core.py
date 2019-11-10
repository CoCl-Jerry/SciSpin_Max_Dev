import socket
from time import sleep
from picamera import PiCamera

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = "10.0.5.2"
server_address = (ip_address, 23456)
sock.bind(server_address)

sock.listen(1)

while True:
    connection, client_address = sock.accept()

    while True:
        recieved = connection.recv(1024).decode("utf-8")

        CMD = recieved.split('~', 6)

        if(CMD[0]=='A'):
            with PiCamera() as camera:
                camera.resolution = (int(CMD[1]),int(CMD[2]))
                if(int(CMD[5])==1):
                    camera.zoom = (1, 1, 0.5, 0.5)
                camera._set_rotation(90*int(CMD[3]))
                sleep(2)
                if(int(CMD[4])==1):
                    camera.capture("out.jpg")
                else:
                    camera.capture("out.png")
            
            if(int(CMD[4])==1):
                f = open ("out.jpg", "rb")
            else:
                f = open ("out.png", "rb")
            l = f.read(512)
            while (l):
                connection.send(l)
                l = f.read(512)
            f.close()
            break

    connection.close()
    



