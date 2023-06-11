# echo-client.py

import socket
import time

command = '<xml version="1.0" encoding="UTF-8"><header/><body><code><body/>'

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1415  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b"HotWireStarted")
while True:
    data = s.recv(1024)
    data = str(data, "utf-8")
    print(f"Received {data}")
    if data.find("Record") > 0:
        time.sleep(1)
        s.sendall(b"OnRecord")
    elif data.find("Wait") > 0:
        time.sleep(2)
        s.sendall(b"OnRecord")
    elif data.find("Start") > 0:
        time.sleep(5)
        s.sendall(b"Finished")
    

