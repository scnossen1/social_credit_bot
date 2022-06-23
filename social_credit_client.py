#client.py
import socket
import threading
import json
import tkinter
import time

#command socket creation
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "35.223.77.93"
port = 420
my_socket.connect((host, port))


#command functions below
def thread_sending():
    while True:
        cmd = input().lower()
        cmd = cmd.split(" ")
        send(my_socket, cmd)
        time.sleep(.5)

def recieve(socket):
    return json.loads(socket.recv(1024).decode())

def send(socket, values):
    return socket.send(json.dumps(values).encode())

def thread_receiving():
    while True:
        message = recieve(my_socket)
        print(message)
        

print('Enter Commands Below:')

thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_send.start()
thread_receive.start()
