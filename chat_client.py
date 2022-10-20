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

nickname = input("Please enter the nickname you wish to use: ")

#setting up TCp with our server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

introduction  = {
    "type":"welcome",
    "nick-name":nickname
}

# as soon as the server is joined our client send out a new nick name
client.send(json.dumps(introduction).encode())
new = client.recv(1024)
print(json.loads(new).decode('UTF-8'))

""" def write():
    while True:
        try:
            trystuff()
        except Exception as e:
            continue """


""" def read():
    while True:
        try:
            trystuff()
        except Exception as e:
            continue """


""" # Starting Threads For Listening And Writing
read_thread = threading.Thread(target=read)
read_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start() """
