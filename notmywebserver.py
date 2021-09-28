# import socket module
from socket import *

import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM)

# http://10.1.141.151:6788/HelloWorld.html
# Prepare a sever socket
ip_address = '10.1.141.151'
port_number = 6788
serverSocket.bind((ip_address, port_number))
serverSocket.listen(1)
print('Ready to serve...')

while True:
    # Establish the connection
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
        f.close()

        # Send one HTTP header line into socket
        connectionSocket.send('\n\nHTTP/1.1 200 OK \r\n Content-Type: text/html;\r\n\r\n'.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            # print(outputdata[i])
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
        break

    except IOError:
        # Send response message for file not found
        print("404 not found")

        # error_file = codecs.open("notFound_404.html", "r", "utf-8")
        connectionSocket.send("\n404 Not Found".encode())

        # Close client socket
        connectionSocket.close()
        break
serverSocket.close()

# Terminate the program after sending the corresponding data
sys.exit()
