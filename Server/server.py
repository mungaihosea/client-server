import socket
import tqdm
import os
import json
from datetime import datetime
# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 13000

# create the server socket
s = socket.socket()

# bind the socket to our local address
s.bind((SERVER_HOST, SERVER_PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
s.listen(5)


# accept connection if there is any
client_socket, address = s.accept()


text = "Welcome to our system. \nEnter your username: " 
client_socket.sendall(text.encode()) #send welcome message to client

username = client_socket.recv(1024).decode() #receive username from client
#terminate the connection if the username is incorrect
if username != 'user1':
    errmsg = 'Incorrect Username, connection Terminated'
    client_socket.sendall(errmsg.encode())
    client_socket.close()
    s.close()
else:
    #display menu if the username is correct
    while True:
        menu = "\n\nPlease select the operation:\n1) View uploaded files' information\n2) Upload a file \n3) Terminate the connection\nChoice: "
        client_socket.sendall(menu.encode())
        #receive menu choice from client
        choice = client_socket.recv(1024).decode()

        if int(choice) == 1:
            #read Database.json file
            database_data = None
            with open('Database.json') as database:
                try:
                    database_data = json.load(database)
                    database.close()
                except json.decoder.JSONDecodeError:
                    pass

            if database_data is not None:
                client_socket.sendall(json.dumps(database_data).encode())        

        elif int(choice) == 2:
            #promt for file name or path
            promt = "Please provide the filename: "
            client_socket.sendall(promt.encode())
            #reteive file metadata
            file_info = client_socket.recv(1024).decode()
            file_size = file_info.split("\n")[1]
            file_path = file_info.split("\n")[0]
            file_name = os.path.basename(file_path)
            #send filesize confirmation
            receving_file = open(file_name, "wb")
            client_socket.sendall(f"OK {file_size}".encode())

            #receive the file
            rcv_data = client_socket.recv(1024)
            total = len(rcv_data)
            while rcv_data:
                if int(total) == int(file_size):
                    break
                receving_file.write(rcv_data)
                rcv_data = client_socket.recv(1024)
                total += len(rcv_data)
            receving_file.close()
            data = None
            #update the Database.json file
            with open('Database.json') as database:
                try:
                    data = json.load(database)
                    database.close()
                except json.decoder.JSONDecodeError:
                    pass
            with open('Database.json', 'w') as database:
                if data is not None:
                    data[file_name] = {"size": file_size, "time": str(datetime.now())}
                    json.dump(data, database)
                    database.close()
                else:
                    data = {file_name: {"size": file_size, "time": str(datetime.now())}}
                    json.dump(data, database)
                    database.close()
                    
        #terminate the program if the choice is 3
        elif int(choice) == 3:
            client_socket.send("connection terminated".encode())
            client_socket.close
            s.close()
            break
