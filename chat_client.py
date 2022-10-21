#******************************
#
#
#******************************

#Imports
import json
import socket
import threading


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

welcome = "Welcome! To the awesome chat room\nLet's get Started\n************************************"
print (welcome)

nickname = input("Please enter the nickname you wish to be identified with: ")

#setting up TCp with our server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

introduction  = {
    "type":"welcome",
    "nick-name":nickname
}

# as soon as the server is joined our client send out a new nick name
client.send(json.dumps(introduction).encode())

def handle_messages():
    while True:
        try:
            message = client.recv(1024)

            data_json = json.loads(message.decode('UTF-8'))

            if data_json["reply-type"] == "welcome-reply":

                print(data_json["output"])

            if data_json["reply-type"] == "existing-rooms-reply":

                print(data_json["list_of_rooms"])

            if data_json["reply-type"] == "room-info-reply":

                print(data_json["output"])
                print(data_json["peers"])

            if data_json["reply-type"] == "join-room-reply":
                print(data_json["output"])
                print(data_json["peers"])

            if data_json["reply-type"] == "create-room-reply":

                print(data_json["output"])


            if data_json["reply-type"] == "send-message-reply":

                print(data_json["list_of_rooms"])
            
            if data_json["reply-type"] == "leave-room-reply":

                print(data_json["output"])
                print(data_json["list_of_rooms"])

        except Exception as e:
            continue





handler = threading.Thread(target = handle_messages)
handler.start()

cmd = """This is the list of commands you can utilize:\n
[*]ROOMS: to get a list of all existing chat rooms
[*]ROOM-INFO: Use this command followed by the name of the room to get the number and list of all connected users for the room
[*]JOIN-ROOM: Use this command followed by the name of the room you wish to join to join the room
[*]CREATE-ROOM: Use this command followed by the name of the room you wish to create
[*]LEAVE-ROOM: Use this command followed by the name of the room you wish to leave
[*]SEND: Use this command followed by the name of the chatroom you wish to send your message in and your message"""

print(cmd)

while True:
    command = input("Enter Command: ")
    words = command.split(" ")
    n = len(words)
    if n <=0:
        print("Empty command entered")
    else:
        if words[0] == "ROOMS":

            request = {
                "type":"existing-rooms"
            }

            client.send(json.dumps(request).encode())

        elif words[0] == "ROOM-INFO":

            request = {
                "type":"room-info",
                "room-name":words[1]
            }

            client.send(json.dumps(request).encode())

        elif words[0] == "JOIN-ROOM":

            request = {
                "type":"join-room",
                "nick-name":nickname,
                "room-name":words[1]
            }

            client.send(json.dumps(request).encode())

        elif words[0] == "CREATE-ROOM":

            request = {
                "type":"create-room",
                "nick-name":nickname,
                "room-name":words[1]
            }

            client.send(json.dumps(request).encode())

        elif words[0] == "LEAVE-ROOM":

            request = {
                "type":"leave-room",
                "nick-name":nickname,
                "room-name":words[1]
            }

            client.send(json.dumps(request).encode())

        elif words[0] == "SEND":

            request = {
                "type": ""
            }

            client.send(json.dumps(request).encode())
        else:
            print("Invalid command entered, please try again!")
