#******************************
#
#
#******************************

#Imports
import socket
import threading 


#Variables
SERVER_HOST = "127.0.0.1" #Local host
SERVER_PORT = 8080

MAXIMUM_CAPACITY = 5 #Max capacity of the chat rooms

# server set up
#create a server connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # The fir parameter indicates we are using internet socket and the second parameter indicates we are using TCP and not UDP
server.bind((SERVER_HOST, SERVER_PORT)) #bind it to our (local) host with a tuple containing our host and port
server.listen() #listening mode

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


#infinite loop to listen for clients
while True:
    client, address = server.accept()
    print("Connected to %s:%d" % (address[0], address[1]))

    data,addr = mySocket.recvfrom(1024)
        
    data_json = json.loads(data.decode())


    if data_json["type"] == "FLOOD-REPLY":
            

    if data_json["type"] == "FLOOD":


    if data_json["type"] == "GET_BLOCK":


    if data_json["type"] == "STATS":

        
    if data_json["type"] == "ANNOUNCE":


    if data_json["type"] == "CONSENSUS":

