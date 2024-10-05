from socket import *
import threading

hostname = gethostname()
HOST = gethostbyname(hostname)
PORT = 12000
MAX_CLIENTS = 5

clients = {}

def binlen(bstring):

    integer = len(bstring)
    return f'{integer:064b}'


def broadcast(message, new = False, exceptClient = False):

    for client in clients:
        if new:
            if (not exceptClient) or (exceptClient != client):
                sendtext(client, message)
        else:
            if (not exceptClient) or (exceptClient != client):
                client.sendall(message)


def receive(client):

    receivedMsg = None
    filesreceived = 0

    while receivedMsg != b'/oao':

        try:
            padding = client.recv(64)
            recvsize = int(padding.decode(), 2)
            received = recvall(client, recvsize)
            recvingfile = False

            i = 0
            recvUsername = ''
            while received[i:i+2] != b'//':
                recvUsername += received[i:i+2].decode()[0]
                i += 1
            receivedMsg = received[i+2:]
            received = padding + received

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
                    print(f'{recvUsername}: ', filename)

                    broadcast(received, exceptClient = client)
            except:
                pass

            if not recvingfile:

                if receivedMsg.decode().startswith('/'):
                    command = receivedMsg.decode().strip()

                    if command == '/users':
                        sendtext(client, f'Connected users: {", ".join(list(clients.values()))}\n')

                    elif command == '/oao':
                        break
                    else:
                        sendtext(client, 'Invalid command.')
                else:
                    broadcast(received, exceptClient = client)
            
        except:
            break
    
    username = clients[client]
    del clients[client]
    print(f'{username} left the chat.\n')
    broadcast(f'{username} left the chat.', new = True)
    client.close()


def sendtext(socket, message):

    message = f'Server//{message}'.encode()
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

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', PORT))
    serverSocket.listen(1)
    print(f'Server is ready for connection on {HOST}:{PORT}.')

    message = None
    received = None
    filesreceived = 0

    while len(clients) < MAX_CLIENTS:

        clientSocket, address = serverSocket.accept()
        
        print(f'Connected with {address}.')

        clientSocket.send('Welcome to the chat room!\nPlease send your username.\n'.encode())
        username = None

        while username == None:
            usernameMsg = clientSocket.recv(1024).decode()

            if usernameMsg.startswith('USERNAME'):
                username = usernameMsg[10:]
            else:
                clientSocket.send('Invalid format.'.encode())

        clients[clientSocket] = username
        broadcast(f'{username} joined the chat!', new = True)

        thread = threading.Thread(target=receive, args=(clientSocket,))
        thread.start()
