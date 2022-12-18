import socket
import re
import threading
import time
import proxy


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 8080))
server.listen(5)
print("[+] Listening on localhost:8080")

id = 0
while True:
    id += 1
    try:
        client_socket, addr = server.accept()
        proxy.Proxy(client_socket, addr, id).start()
        time.sleep(0.1)       
        
    except KeyboardInterrupt:
        print("\n[+] Shutting down...")
        server.close()
        exit(0)
    except Exception as e:
        print("[+]", e)
