# I used these in help: 
# https://www.w3schools.com/python/ref_string_encode.asp

import socket
import threading

HOST = '127.0.0.1'
PORT = 3000

# creating the client socket and the connection to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print("'/quit' to quit,\n '/join *channelname*' to join a channel,\n and '/dm *nickname* *message*' to send a private message \n")
nickname = input("Enter your nickname (and press enter to continue): ")

# Sending the nickname to the server
client_socket.send(f"{nickname}: ".encode())

# Initializing current channel to "general"
current_channel = "general"  
print(f'Welcome to the chat! Channel: {current_channel}\n')

# receiving the message(s) from the server
def message_receive(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Closing...")
            client_socket.close()
            break

# sending message(s) to the server
def message_send():
    while True:
        message = input()

        # handling the quitting
        if message.lower() == '/quit':
            print("Disconnecting from the server...")
            client_socket.send('/quit'.encode())
            client_socket.close()
            break

        # handling the sending of private message(s)
        elif message.startswith('/dm'):
            parts = message.split(' ', 2)
            if len(parts) >= 3:
                recipient, dm_message = parts[1], parts[2]
                
                # empty messages cannot be sent
                if dm_message.strip():
                    client_socket.send(f'/dm {recipient} {dm_message}'.encode())
                else:
                    print("\nEmpty message cannot be sent.")
            else:
                print("\nInvalid /dm command format. Usage: /dm *nickname* *message*")

        # handling the joining of channel(s)
        elif message.startswith('/join'):
            parts = message.split(' ')
            if len(parts) == 2:
                new_channel = parts[1].strip()
                client_socket.send(f'/join {new_channel}'.encode())
                print(f"\nYou've joined the '{new_channel}' channel.")
            else:
                print("\nInvalid /join command format. Usage: /join channel_name")
        elif message.strip():
            client_socket.send(message.encode())
        else:
            print("\nEmpty message cannot be sent.")

# creating the thread for receiving message and starting it
receive_thread = threading.Thread(target=message_receive, args=(client_socket,))
receive_thread.start()

# creating the thread for sending message and starting it
send_thread = threading.Thread(target=message_send)
send_thread.start()