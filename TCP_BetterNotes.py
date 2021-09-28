'''
socket [using]
os [should use]
sys [should use]

other custom libraries
requests
http.server
SimpleHTTPServer
socketserver
urllib
'''

from socket import *

ip_address = '10.1.141.151' # hostname
serverPort = 6788           # port number
serverSock = socket(AF_INET, SOCK_STREAM)   # Create a TCP/IP socket

serverAddress = (ip_address, serverPort)    # bind socket to port
serverSock.bind(serverAddress)

serverSock.listen(1)  # server listens for connections

while True:
    print('The server is waiting for a connection')

    # server waits to accept for an incoming request
    clientSock, clientAddress = serverSock.accept()
    print("A connection from: " + str(clientAddress))

    # ---------- process starts here ----------
    # read bytes from client socket and modifies content
    sentence = clientSock.recv(1024).decode()

    # sends modified bytes back to client socket
    capitalizedSentence = sentence.upper()
    clientSock.send(capitalizedSentence.encode())

    # ---------- process ends here ----------
    clientSock.close()  # server closes connection to this client
    break               # breaks off the loop

# server's part is done
serverSock.close()

