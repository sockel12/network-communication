import socket

s = socket.socket()
host = 'localhost'
port = 8000
s.connect((host, port))
print (s.recv(1024))
s.close()