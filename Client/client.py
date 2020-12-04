import socket
import os
import json


# the ip address or hostname of the server, the receiver
host = input("Enter the server hostname or IP: ")

# the port, let's use 13000
port = 13000
# the name of file we want to send, make sure it exists
filename = ""

# create the client socket
s = socket.socket()

s.connect((host, port))

#get the client username and send to the client
def get_username(server_msg):
    username = input(server_msg)
    s.sendall(username.encode())

connection_is_on = True

#get the menu choice and submit to client
def get_choice(server_msg):
    choice = input(server_msg)
    s.sendall(choice.encode())
 
#collect the the file path or name .. 
def get_filename(server_msg):
    global filename
    filename = os.path.abspath(f"{input(server_msg)}")
    filesize = os.path.getsize(filename)
    s.sendall(f"{filename}\n{filesize}".encode())

#actively listen for server messages
while connection_is_on:
    server_msg = s.recv(1024).decode()
    if server_msg == "Welcome to our system. \nEnter your username: ":
        get_username(server_msg)
    elif server_msg == 'Incorrect Username, connection Terminated':
        s.close()
        connection_is_on = False
        print(server_msg)

    elif server_msg == "\n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \n3) Terminate the connection\nChoice: ":
        get_choice(server_msg)
    elif server_msg == "Please provide the filename: ":
        get_filename(server_msg)
    
    elif server_msg.__contains__('size'):
        server_msg = json.loads(server_msg)
        print(f"file name \t file size \t date uploaded")
        for key in server_msg.keys():
            print(f"{key} \t {server_msg[key]['size']} \t {server_msg[key]['time']}")

    #file upload process
    elif server_msg.__contains__('OK'):
        print(server_msg)
        sending_file = open(filename, 'rb')
        send_data = sending_file.read(1024)
        while send_data:
            s.sendall(send_data)
            send_data = sending_file.read(1024)
        sending_file.close()
        print("Upload process completed")
        
        
    #terminate connection
    elif server_msg == "connection terminated":
        s.close()
        print("Connection terminated")
        connection_is_on = False



