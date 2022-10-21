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
chat_rooms = {}             #list of all existing chart rooms


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

    if newNickName in client_nicknames:
        msg = "Error: Sorry the nickname already exists!"
    else:
        msg = "*****************************************\n\nHello %s! Welcome to the awesome chat room, we hope you brought pizza\n\n*****************************************"%newNickName
        print("A new user joined the chat! Welcome: " + newNickName)
        client_nicknames.append(newNickName)

    reply = {
        "reply-type":"welcome-reply",
        "output": msg 
    }

    conn.send(json.dumps(reply).encode())


def existing_rooms(conn):
    
    reply = {
        "reply-type":"existing-rooms-reply",
        "list_of_rooms": chat_rooms # you will need to parse this in the client side to get a list of all the names of the chat rooms #TODO
    }

    conn.send(json.dumps(reply).encode())

def room_info(conn, room):
    if room in chat_rooms:
        theList = chat_rooms[room]
        length = len(theList)
        msg = "The chat room %s has %d users"%(room, length)
    else:
        msg = "The room does not exist"

    reply = {
        "reply-type":"room-info-reply",
        "peers": theList,
        "output": msg
    }

    conn.send(json.dumps(reply).encode())


def join_room(conn, roomToJoin, nick):

    if roomToJoin in chat_rooms:
        #we join
        theList = chat_rooms[roomToJoin]
        length = len(theList)
        if length <5:
            #we can join
            theList.append(nick)
            msg= "Room joining successful. Now you're in the chat room %s"%roomToJoin
        else:
            msg = "Room joining Failed: The room has reached its maximum capacity"
    else:
        msg= "Room joining Failed. The room does not exist, please try again" #TODO

    reply = {
        "reply-type":"join-room-reply",
        "list_of_rooms": chat_rooms,
        "peers": theList,
        "output": msg
    }

    conn.send(json.dumps(reply).encode())

def create_room(conn, room_name, nick):

    if room_name in chat_rooms:
        
        msg = "Please pick a different room name, another room with the same name already exists"

    else:
        #add the name as the key and the list of nicknames as value in the dictionary
        chat_rooms[room_name] = []
        msg = "The room %s has been created. You can now look at the updated list of chat rooms using the appropriate command"%room_name

    reply = {
        "reply-type":"create-room-reply",
        "list_of_rooms": chat_rooms,
        "output": msg
    }

    conn.send(json.dumps(reply).encode())
    print("A new room %s has been created by the user %s"%room_name%nick)

def send_message(conn):

    reply={
        "reply-type":"send-message-reply"
    }

    conn.send(json.dumps(reply).encode())
    print("reply sent")


def leave_room(conn, roomToBeLeft, nick):
    
    if roomToBeLeft in chat_rooms:
        if nick in chat_rooms[roomToBeLeft]:
            (chat_rooms[roomToBeLeft]).remove(nick)
            msg = "Leaving room successful"      
    else:
        msg = "The room does not exist"

    reply={
        "reply-type":"leave-room-reply",
        "list_of_rooms": chat_rooms,
        "output": msg
    }

    conn.send(json.dumps(reply).encode())

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
                room_info(client, data_json["room-name"])

            if data_json["type"] == "join-room":
                #Join existing chat rooms if the room capacity is not full
                join_room(client, data_json["room-name"], data_json["nick-name"])

            if data_json["type"] == "create-room":
                #Create chat-rooms
                create_room(client, data_json["room-name"], data_json["nick-name"])

            if data_json["type"] == "send-message":
                #Send messages to chat-rooms
                send_message(client)
            
            if data_json["type"] == "leave-room":
                #Leave a chat-room
                leave_room(client, data_json["room-name"], data_json["nick-name"])

        except Exception as e:
            continue

#infinite loop to listen for clients
while True:
    client, address = server.accept()
    #print("Connected to %s:%d" % (address[0], address[1])) 
    list_of_clients.append(address)

    handler = threading.Thread(target = client_handler, args=(client,address))
    handler.start()

