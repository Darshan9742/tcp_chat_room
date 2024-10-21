import socket
import threading

#server_address
host = '127.0.0.1'
port = 55553

#creating_driver
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#created lists to store clients and their nicknames
clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(2048)     #try to recieve a messsage from client
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(2048).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        broadcast(f'{nickname} joined the chat!!'.encode('ascii'))
        client.send('Connect to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening.........")
receive()
