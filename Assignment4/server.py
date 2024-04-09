# I used the python documentation in help: 
# https://docs.python.org/3.9/library/socket.html
# https://docs.python.org/3.9/library/threading.html
# https://www.neuralnine.com/tcp-chat-in-python/

import socket
import threading

# handling the connection data
HOST = '127.0.0.1'
PORT = 3000

# server side is started 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")

# dictionary for saving the connected client(s) 
clients = {}

# dictionary for storing channels and their connected clients
channels = {"general": []}  

# handling the client's connections
def handle_client(client_socket, address):

    # receiving the nickname from the client
    nickname_message = client_socket.recv(1024).decode()
    nickname = nickname_message.split(':')[0].strip()

    # making sure that nicknames are unique
    if nickname in clients:
        client_socket.send("Nickname already taken. Please reconnect with a different nickname.".encode())
        client_socket.close()
        return

    # adding the clients to the dictionary with their nickname as key
    clients[nickname] = client_socket
    channels["general"].append(nickname)

    broadcast("general", f"\n{nickname} has joined the chat.", client_socket)

    # Set the default channel
    current_channel = "general"  

    while True:
        try:
            message = client_socket.recv(1024).decode()

            # check of the quitting
            if message.lower() == '/quit':
                client_socket.send('/quit'.encode())
                remove_client(nickname)
                break

            # check of dm message
            elif message.startswith('/dm'):
                parts = message.split(' ', 2)
                if len(parts) >= 3:
                    recipient, dm_message = parts[1], parts[2]
                    send_dm(nickname, recipient, dm_message)
                else:
                    client_socket.send("\nInvalid /dm command format. Usage: /dm *nickname* *message*".encode())

            # check for the channel joining
            elif message.startswith('/join'):
                parts = message.split(' ')
                if len(parts) == 2:
                    new_channel = parts[1].strip()
                    join_channel(new_channel, nickname)
                    # Update current channel
                    current_channel = new_channel  
                else:
                    client_socket.send("\nInvalid /join command format. Usage: /join channel_name".encode())
            
            # sending the message to all the clients in the current channel
            else:
                broadcast(current_channel, f"{nickname}: {message}", client_socket)
        except:
            remove_client("general", nickname)
            break

# sending a private message
def send_dm(nickname, recipient, dm_message):
    # searching the user if its online
    if recipient in clients:

        # user cannot dm theirselves
        if recipient != nickname:
            try:
                clients[recipient].send(f'(DM) {nickname}: {dm_message}\n'.encode())
                clients[nickname].send(f'***Sent DM to {recipient}: {dm_message}***\n'.encode())
            except:
                clients[nickname].send(f"***Failed to send DM to {recipient}.***\n".encode())
        else:
            clients[nickname].send("***You cannot send a direct message to yourself.***\n".encode())
    else: 
        client_socket.send("***User not found or offline.***\n".encode())

# sending the message to all the (connected) clients except the message sender
def broadcast(channel, message, sender_socket):
    for user in channels[channel]:
        if clients[user] != sender_socket:

            # sending the message to client(s) & removing the client if it cannot be sent
            try:
                clients[user].send(message.encode())
            except:
                remove_client(channel, user)             

# removing the client from the list and the socket is closed
def remove_client(channel, nickname):
    if nickname in channels[channel]:
        channels[channel].remove(nickname)
        broadcast(channel, f"{nickname} has left the chat.", None)
        del clients[nickname]

# adding client to a channel
def join_channel(channel, nickname):

    # the channel is created if its not already
    if channel not in channels:
        channels[channel] = []

    # adding the client to the channel
    if nickname not in channels[channel]:
        channels[channel].append(nickname)
        channels["general"].remove(nickname)
        broadcast("general", f"{nickname} has left the chat.", None)
        broadcast(channel, f"{nickname} has joined the chat.", None)

try:
    while True:
        # accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Connected with: {client_address}")

        # a new thread is created for the handling of the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("Server is shutting down...")
    server_socket.close()