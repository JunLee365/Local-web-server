from socket import *

ip_address = '10.1.141.151' # hostname
serverPort = 6788           # port number
serverSock = socket(AF_INET, SOCK_STREAM)   # create a TCP/IP socket

serverAddress = (ip_address, serverPort)    # bind socket to port
serverSock.bind(serverAddress)
serverSock.listen(1)                        # server listens for connections

# used to print link
    # print("http://" + ip_address + ":" + str(serverPort) + "/HelloWorld.html")

while True:
    # server waits to accept for an incoming connection request
    # eventually connects with a client [socket]
    print("The server is waiting for a connection...")
    clientSock, clientAddress = serverSock.accept()
        # print("A connection from: " + str(clientAddress))

    # ---------- process starts here ----------
    try:    # try seeing if file exists
        # receive message from client socket
        message = clientSock.recv(1024).decode()
            # print("\nHTTP message:\n" + message)

        # parse through the message
        # if file is found -> read file
        filename = message.split()[1]
        f = open(filename[1:])
        content = f.read()
        f.close()
            # print("File opened: " + filename[1:])

        # form a response message starting with a header
        responseMessage = "HTTP/1.1 200 OK \r\n Content-Type: text/html;\r\n\r\n"

        # write content of the file into the response message
        for i in range(0, len(content)):
            responseMessage += content[i]

        # send response message to client and print success message
        clientSock.send(responseMessage.encode())
        print("200 OK")

    except IOError: # catch if file doesn't exist
        # send error message to client and print error message
        responseMessage = "HTTP/1.1 404 NOT FOUND \r\n Content-Type: text/html;\r\n\r\n"
        clientSock.send(responseMessage.encode())
        print("404 NOT FOUND")

    # ---------- process ends here ----------
    clientSock.close()  # server closes connection with client [socket]
    break               # breaks off the loop

serverSock.close()  # close server socket
