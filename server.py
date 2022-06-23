#server.py
import socket
import threading
import json
import os
import random

#command socket creation
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT = 420
ADDRESS = "0.0.0.0"
my_socket.bind((ADDRESS, PORT))
valid_commands = ['deduct', 'add', 'listing', 'help']
broadcast_list = []

#command functions below

def create_txt_files():
    with open('users/users.txt', 'r') as users:
        for line in users:
            if not os.path.exists(f'users_score/{trim(line, 1)}.txt'):
                with open(f'users_score/{trim(line, 1)}.txt', 'w') as f:
                    f.write('0')

def accept_loop():
    while True:
        my_socket.listen()
        client, client_address = my_socket.accept()
        broadcast_list.append(client)
        print('Client Connected : ', client, client_address)
        start_listenning_thread(client)
        
def start_listenning_thread(client):
    client_thread = threading.Thread(
            target=listen_thread,
            args=(client,) #the list of argument for the function
        )
    client_thread.start()

def listen_thread(client):
    while True:
        try:
            cmd = recieve(client)
            if cmd[0] not in valid_commands:
                   send(client, 'That is not a valid command')
            else:
                if cmd[0] == valid_commands[0]:
                    deduct_credit(client, cmd)
                elif cmd[0] == valid_commands[1]:
                    add_credit(client, cmd)
                elif cmd[0] == valid_commands[2]:
                    list_credit(client)
                elif cmd[0] == valid_commands[3]:
                    help_them(client)
        except socket.error:
            print(f"Client removed : {client}")
            return

def broadcast(message):
    for client in broadcast_list:
        try:
            send(client, message)
        except:
            broadcast_list.remove(client)
            print(f"Client removed : {client}")

def trim(string, x):
    length = len(string)
    string_minus_return = string[:length - x]
    return string_minus_return

def add_credit(client, cmd):
    if is_name_in_list(client, cmd):
        with open(f'users_score/{cmd[1]}.txt', 'r+') as f:
            score = int(f.read())
            score += random.randint(1, 4999)
            broadcast(f'{cmd[1]}\'s New Score is {score}')
            f.truncate(0)
            f.seek(0)
            f.write(str(score))
        return

def deduct_credit(client, cmd):
    if is_name_in_list(client, cmd):
        with open(f'users_score/{cmd[1]}.txt', 'r+') as f:
            score = int(f.read())
            score += random.randint(-4998, -1)
            broadcast(f'{cmd[1]}\'s New Score is {score}')
            f.truncate(0)
            f.seek(0)
            f.write(str(score))
        return

def list_credit(client):
    count = 0
    full_listing = 'Social Credit Scores Are:\n'
    
    for filename in os.listdir('users_score'):
        with open(f'users_score/{filename}', 'r') as f:
            full_listing += f'{trim(filename, 4)}: {f.read()}\n'
    send(client, full_listing)
    return

def help_them(client):
    with open('help.txt', 'r') as f:
        send(client, f.read())
    return

def recieve(socket):
    return json.loads(socket.recv(1024).decode())

def send(socket, values):
    return socket.send(json.dumps(values).encode())

def is_name_in_list(client, cmd):
    with open('users/users.txt', 'r') as users:
        if cmd[1] in users.read():    #checks if stated user is in list of users
            return True
        else:
            send(client, 'Command does not have a valid user')
            return False


create_txt_files()
accept_loop()

