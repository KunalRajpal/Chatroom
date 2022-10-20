#******************************
#
#
#******************************

#Imports
import socket
import threading

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8080

nickname = input("Please enter the nickname you wish to use: ")

#setting up TCp with our server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

