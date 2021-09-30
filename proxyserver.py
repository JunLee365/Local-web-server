from socket import *

ip_address = 'localhost'                # hostname
proxyPort = 8080                        # port number
proxyAddress = (ip_address, proxyPort)  # server address

# Create a proxy socket, bind it to a port and start listening
proxySock = socket(AF_INET, SOCK_STREAM)    # create a TCP/IP socket
proxySock.bind(proxyAddress)                # bind proxy to port
proxySock.listen(1)                         # proxy listens for connections

while True:
    # server waits to accept a connection
    print('Ready to serve...')
    clientSock, clientAddr = proxySock.accept()
    print('Received a connection from:', clientAddr)

    # receive message from client socket
    message = clientSock.recv(100000000).decode()
    # print("HTTP message:\n" + message)

    # parse through message to extract filename
    filename = message.split()[1].partition("/")[2]
    filetouse = message.split()[1]

    try:
        # if requested file is found in cache -> read file
        cacheRead = open(filetouse[1:], "r")
        content = cacheRead.read()
        # print("filename: " + filename)
        # print("filetouse: " + filetouse)

        # form a response message starting with a header
        # then write content of the file into the response message
        responseMessage = "HTTP/1.1 200 OK \r\n Content-Type: text/html;\r\n\r\n"
        responseMessage += content

        # Proxy sends message to client [in this case: browser]
        # print success message, closes objects
        clientSock.send(responseMessage.encode())
        print("200 OK")
        print('Read ' + filename + ' from cache\n')
        clientSock.close()
        cacheRead.close()

    # EXCEPTION: if requested file is not found in cache
    except IOError:
        # Create a socket in proxy
        proxyClientSock = socket(AF_INET, SOCK_STREAM)

        # Parse through the previously received message
        hostname = message.split()[1].partition("/")[2].partition("/")[0]
        destination = message.split()[1].partition("/")[2].partition("/")[2]
        # print("hostname: " + hostname)
        # print("destination: " + destination)

        try:
            # Proxy makes connection to a server [this time as a client]
            proxyClientSock.connect((hostname, 80))
            print('Socket connected to port 80 of the host')

            # generate request message [to server] starting with header
            sendMessage = message.split()[0] + ' /' + destination + ' ' + message.split()[2] + '\r\n'
            sendMessage += message.split('\n')[1].split()[0] + ' ' + hostname + '\r\n'
            # print("HTTP message:\n" + serverMessage)

            for i in message.split('\r\n')[2:]:
                sendMessage += i + '\r\n'

            # proxy [as client] sends 'serverMessage' to server
            # receives a message from server
            proxyClientSock.send(sendMessage.encode())
            rq = proxyClientSock.recv(100000000)

            # file is saved into cache for future use
            saveFile = open("./" + filename, "wb")
            saveFile.write(rq)
            saveFile.close()

            # Proxy sends content back to the (actual) client
            # [to the browser]. Prints message, closes objects
            print('Read is complete. File is saved\n')
            clientSock.send(rq)
            clientSock.close()

        # If there is an error in the process, abruptly stop connection
        except IOError:
            print("Error\n")
            clientSock.close()
