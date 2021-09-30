from socket import *

ip_address = gethostbyname(gethostname())   # hostname
serverPort = 6788                           # port number
serverAddress = (ip_address, serverPort)    # server address

serverSock = socket(AF_INET, SOCK_STREAM)   # create a TCP/IP socket
serverSock.bind(serverAddress)              # bind socket to port
serverSock.listen(1)                        # server listens for connections

# Prints out a link
print("http://" + ip_address + ":" + str(serverPort) + "/HelloWorld.html")

while True:
    # server waits to accept for an incoming connection request
    # eventually connects with a client [socket]
    print("The server is waiting for a connection...")
    clientSock, clientAddress = serverSock.accept()
    # print("A connection from: " + str(clientAddress))

    # receive message from client socket
    message = clientSock.recv(1024).decode()
    # print("\nHTTP message:\n" + message)

    # ---------- process starts here ----------
    try:# try seeing if file exists
        # parse through message to extract filename
        filename = message.split()[1]

        # if file is found -> read file
        fileRead = open(filename[1:])
        content = fileRead.read()
        # print("File opened: " + filename[1:])

        # form a response message starting with a header
        # then write content of the file into the response message
        responseMessage = "HTTP/1.1 200 OK \r\n Content-Type: text/html;\r\n\r\n"
        responseMessage += content

        # send response message to client, print success message, close objects
        clientSock.send(responseMessage.encode())
        print("200 OK")
        fileRead.close()

    except IOError: # catch if file doesn't exist
        # send error message to client and print error message
        responseMessage = "HTTP/1.1 404 NOT FOUND \r\n Content-Type: text/html;\r\n\r\n"
        clientSock.send(responseMessage.encode())
        print("404 NOT FOUND")

    # ---------- process ends here ----------
    clientSock.close()  # server closes connection with client [socket]
    break               # breaks off the loop

serverSock.close()  # close server socket
