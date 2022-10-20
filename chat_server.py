#******************************
#
#
#******************************

#Imports
import socket
import threading 


#Server details
SERVER_HOST = "127.0.0.1" #Local host
SERVER_PORT = 8080

# server set up
#create a server connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # The fir parameter indicates we are using internet socket and the second parameter indicates we are using TCP and not UDP
server.bind((SERVER_HOST, SERVER_PORT)) #bind it to our (local) host with a tuple containing our host and port


server.listen() #listening mode

#Lists
list_of_clients = []        #list of clients connecting to the server
client_names = []           #list of client nicknames
chat_rooms = []             #list of all existing chart rooms


MAXIMUM_CAPACITY = 5#Max capacity of the chat rooms


#Functions

#Broadcast: Sends a message to all the clients currently connected to the server rn 
def broadcast(message):
    for targetClient in clients:
        targetClient.send(message)

