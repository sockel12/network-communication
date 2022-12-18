import socket
import re
import threading

protPattern = r"^([A-z]+)"
hostPattern = r"Host: ([A-Za-z0-9\-\.]+)"
portPattern = r"[A-Za-z0-9\-\.\/]+:([0-9]*)"

class Proxy(threading.Thread):
    target_socket = None

    def __init__(self, client_socket: socket.socket, addr: tuple, id: int):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr
        self.id = id
        self.running = True

        self.client_socket.setblocking(0)
        self.client_socket.settimeout(0.1)
         
        try:
            data = client_socket.recv(4096)
        except Exception as e:
            print("[PROXY] Error: " + str(e))
            self.running = False
            return
        
        # Get target and port
        try:
            self.target_prot = re.search(protPattern, data.decode("utf-8")).group(1)
        except:
            print("prot")
        try:
            self.target_hostname = re.search(hostPattern, data.decode("utf-8")).group(1)
        except:
            print("host")
        try:
            self.target_port = int(re.search(portPattern, data.decode("utf-8")).group(1))
        except:
            print("port")
            self.target_port = 80
        print("[PROXY] Target: " + self.target_hostname + ":" + str(self.target_port) + " (" + self.target_prot + ") TID: " + str(id))
        print("[CLIENT] Got data from Target: " + data.decode("utf-8"))

        if self.target_hostname != "benjaminappel.tech":
            self.running = False
            return

        try:
            self.target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.target_socket.connect((socket.gethostbyname(self.target_hostname), self.target_port))
            self.target_socket.setblocking(0)
            self.target_socket.settimeout(0.1)
            with open(str(self.id) + "_log.txt", "ab") as f:
                f.write(b"[CLIENT] Got data from Client: " + data + b"\n")
                f.flush()
                if self.target_prot == "CONNECT":
                    print("[PROXY] Sending CONNECT resonse to client...")
                    client_socket.send("HTTP/1.1 200 Connection established\r\n\r\n".encode("utf-8"))
                else:
                    print("[PROXY] Got request, no connect, forwarding to target...")
                    self.target_socket.send(data)
                    sever_data = self.target_socket.recv(4096)
                    client_socket.send(sever_data)
        except Exception as e:
            print("[PROXY] Error: " + str(e))
            print("[PROXY] Data received: " + data.decode("utf-8"))
            self.running = False


    def run(self):
        if not self.running:
            return

        client_buffer = []
        target_buffer = []

        with open(str(self.id) + "_log.txt", "ab") as f:
            while self.running:
                try:
                    while True:
                        try:

                            data = self.client_socket.recv(4096)
                        except socket.timeout:
                            break
                        if data:
                            client_buffer.append(data)
                            f.write(b"[CLIENT] Got data from Client: " + data + b"\n")
                        else:
                            break
                        f.flush()
                    
                    for data in client_buffer:
                        self.target_socket.send(data)
                    client_buffer = []

                    while True:
                        try:
                            data = self.target_socket.recv(4096)
                        except socket.timeout:
                            break
                        if data:
                            target_buffer.append(data)
                            f.write(b"[SERVER] Got data from Target: " + data + b"\n")
                        else:
                            break
                        f.flush()

                    for data in target_buffer:
                        self.client_socket.send(data)
                    target_buffer = []

                    
                except ConnectionResetError:
                    print("[PROXY] Connection reset by peer... TID: " + str(self.id))
                    break
                except Exception as e:
                    print("[PROXY] Error: " + str(e))
                    break

                

            print("[PROXY] Closing connection... TID: " + str(self.id))
            self.client_socket.close()
            if self.target_socket:
                self.target_socket.close()


