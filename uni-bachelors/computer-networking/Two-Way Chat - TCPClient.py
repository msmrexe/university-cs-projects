from socket import *


def binlen(bstring):

    integer = len(bstring)
    return f'{integer:064b}'


def sendfile(socket, filename):

    with open(filename, 'rb') as file:
        filedata = file.read()

    fileformat = filename.split('.')[-1]
    message = f'Attachment: {fileformat}>>'.encode() + filedata
    paddedmessage = binlen(message).encode() + message
    socket.sendall(paddedmessage)


def sendtext(socket, message):

    message = message.encode()
    message = binlen(message).encode() + message
    socket.sendall(message)


def recvall(socket, size):
    
    recvchunks = []
    bufsize = 1048576
    remaining = size
    
    while remaining > 0:
        received = socket.recv(min(remaining, bufsize))
        
        if not received:
            raise Exception('Unexpected EOF')
        
        recvchunks.append(received)
        remaining -= len(received)

    return b''.join(recvchunks)


def recvfile(filename, filedata):

    with open(filename, 'wb') as file:
        file.write(filedata)



if __name__ == "__main__":

    serverName = input('Enter Server IP: ')
    serverPort = 12000

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print('Connection successful. You can begin chatting below.')

    message = None
    received = None
    filesreceived = 0

    while received != b'OVER AND OUT.':

        message = input('From You: ')
        sendingfile = False
        
        try:
            if message[:12] == 'Attachment: ':
                sendingfile = True
                sendfile(clientSocket, message[12:])
        except:
            pass

        if not sendingfile:
            sendtext(clientSocket, message)

        recvsize = int(clientSocket.recv(64).decode(), 2)
        received = recvall(clientSocket, recvsize)
        recvingfile = False

        try:
            if received[:12] == b'Attachment: ':
                recvingfile = True
                filesreceived += 1
                
                char, indx = received[12:14], 12
                while char != b'>>':
                    indx += 1
                    char = received[indx:indx+2]
                fileformat, filedata = received[12:indx], received[indx+2:]
                
                filename = f'received{filesreceived}.{fileformat.decode()}'
                recvfile(filename, filedata)
                print('From Server:', filename)
        except:
            pass

        if not recvingfile:
            print('From Server:', received.decode())
        
    clientSocket.close()
