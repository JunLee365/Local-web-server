from socket import *

ip_address = '10.1.141.151'
serverPort = 6788
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((ip_address, serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()

    sentence = connectionSocket.recv(1024).decode()

    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
