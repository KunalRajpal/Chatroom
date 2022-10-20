#******************************
#
#
#******************************

#Imports
import json
import socket
import threading 


#Variables
SERVER_HOST = "127.0.0.1" #Local host
SERVER_PORT = 8080

MAXIMUM_CAPACITY = 5 #Max capacity of the chat rooms

# server set up
#create a server connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # The first parameter indicates we are using internet socket and the second parameter indicates we are using TCP and not UDP
server.bind((SERVER_HOST, SERVER_PORT))                     # bind it to our (local) host with a tuple containing our host and port
server.listen()                                             # listening mode

print("Listening on %s:%d" % (SERVER_HOST, SERVER_PORT))

#Lists
list_of_clients = []        #list of clients connecting to the server
client_nicknames = []       #list of client nicknames
chat_rooms = []             #list of all existing chart rooms


#Functions

#Broadcast: A helper function to send messages to a particular list of clients
def broadcast(message, targetClients, broadcaster):
    for targetClient in targetClients:
        if targetClient != broadcaster:
            try:
                targetClient.send(message)
            except:
                targetClient.close()
                remove(targetClient)

#remove: Helper function to remove a client from our client list
def remove(thisClient):
    if thisClient in list_of_clients:
        list_of_clients.remove(thisClient)

def welcome(newNickName, conn):
    print("A new user joined the chat! Welcome: " + newNickName)
    client_nicknames.append(newNickName)

    reply = {
        "reply-type":"welcome-reply",
        "msg": "Hello! Welcome to the awesome chat room, we hope you brought pizza XD" #TODO
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")


def existing_rooms(conn):
    
    reply = {
        "reply-type":"existing-rooms-reply",
        "list_of_rooms": chat_rooms
    }

    conn.send(json.dumps(reply).encode())
    print(chat_rooms)

def room_info(conn):

    reply = {
        "reply-type":"room-info-reply"
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")

def join_room(conn):

    reply = {
        "reply-type":"join-room-reply"
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")

def create_room(conn, newRoom):

    reply = {
        "reply-type":"create-room-reply"
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")

def send_message(conn):

    reply={
        "reply-type":"send-message-reply"
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")


def leave_room(conn):

    reply={
        "reply-type":"leave-room-reply"
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")

def client_handler(client, address):

    while True:
        try:
            message = client.recv(1024)

            data_json = json.loads(message.decode('UTF-8'))

            if data_json["type"] == "welcome":
                welcome(data_json["nick-name"], client)

            if data_json["type"] == "existing-rooms":
                #View list of existing chat rooms
                existing_rooms(client)

            if data_json["type"] == "room-info":
                #view the number and list of connected users for each room
                room_info(client)

            if data_json["type"] == "join-room":
                #Join existing chat rooms if the room capacity is not full
                join_room(client)

            if data_json["type"] == "create-room":
                #Create chat-rooms
                create_room(client, roomName)

            if data_json["type"] == "send-message":
                #Send messages to chat-rooms
                send_message(client)
            
            if data_json["type"] == "leave-room":
                #Leave a chat-room
                leave_room(client)

        except Exception as e:
            continue

#infinite loop to listen for clients
while True:
    client, address = server.accept()
    #print("Connected to %s:%d" % (address[0], address[1])) 
    list_of_clients.append(address)

    handler = threading.Thread(target = client_handler, args=(client,address))
    handler.start()

