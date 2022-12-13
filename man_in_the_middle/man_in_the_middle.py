import socket

client_socket = socket.socket()
server_socket = socket.socket()

host = 'localhost'
port = 8000

server_socket.bind((host, port))
server_socket.listen(1)

client_socket.connect((host, 8080))

try:
    while True:
        client, addr = server_socket.accept()
        data = client.recv(1024)
        while data:
            print(data  )
            client_socket.send(data)
            data = client.recv(1024)
        client.close()


except KeyboardInterrupt:
    print ('Shutting down server')
    server_socket.close()
    client_socket.close()
except Exception as e:
    print ('Error:', e)
    server_socket.close()
    client_socket.close()