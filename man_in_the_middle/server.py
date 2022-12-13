import socket

s = socket.socket()
s.bind(('localhost', 8080))
s.listen(5)

try: 
    while True:
        c, addr = s.accept()
        print ('Got connection from:', addr)
        c.send(b'Thank you for connecting')
        c.close()
except KeyboardInterrupt:
    print ('Shutting down server')
    s.close()
except Exception as e:
    print ('Error:', e)
    s.close()