from socket import *
import threading


def binlen(bstring):

    integer = len(bstring)
    return f'{integer:064b}'


def receive():

    received = None
    filesreceived = 0

    while True:

        try:
            padding = clientSocket.recv(64)
            recvsize = int(padding.decode(), 2)
            received = recvall(clientSocket, recvsize)
            recvingfile = False

            i = 0
            recvUsername = ''
            while received[i:i+2] != b'//':
                recvUsername += received[i:i+2].decode()[0]
                i += 1
            receivedMsg = received[i+2:]

            try:
                if receivedMsg[:8] == b'ATCHMNT:':
                    recvingfile = True
                    filesreceived += 1
                    
                    char, indx = receivedMsg[8:10], 8
                    while char != b'>>':
                        indx += 1
                        char = receivedMsg[indx:indx+2]
                    fileformat, filedata = receivedMsg[8:indx], receivedMsg[indx+2:]
                    
                    filename = f'received{filesreceived}.{fileformat.decode()}'
                    recvfile(filename, filedata)
                    print(f'\n{recvUsername}: ', filename, '\n')
            except:
                pass
    
            if not recvingfile:
                print(f'\n{recvUsername}: ', receivedMsg.decode(), '\n')

        except:
            clientSocket.close()
            break


def sendtext(socket, username, message):

    message = f'{username}//{message}'.encode()
    message = binlen(message).encode() + message
    socket.sendall(message)


def sendfile(socket, username, filepath):

    with open(filepath, 'rb') as file:
        filedata = file.read()

    filename = filepath.split('/')[-1]
    fileformat = filename.split('.')[-1]
    message = f'{username}//ATCHMNT:{fileformat}>>'.encode() + filedata
    paddedmessage = binlen(message).encode() + message
    socket.sendall(paddedmessage)


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

    print(clientSocket.recv(1024).decode())
    username = input('Enter your username: ')
    clientSocket.send(f'USERNAME: {username}'.encode())
    print('You can begin chatting below.\n')

    receive_thread = threading.Thread(target = receive)
    receive_thread.start()

    message = None
    while message != '/oao':

        message = input('')
        sendingfile = False
        
        try:
            if message[:8] == 'ATCHMNT:':
                sendingfile = True
                sendfile(clientSocket, username, message[8:])
        except:
            pass

        if not sendingfile:
            sendtext(clientSocket, username, message)
        
    clientSocket.close()
