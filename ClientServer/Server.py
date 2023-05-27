import socket
import os

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to a specific address and port
server_address = ('localhost', 8888)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print('Server is listening on {}:{}'.format(*server_address))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print('Client connected from {}:{}'.format(*client_address))

# Read the XML file from the server's filesystem
with open(os.path.abspath('XMLFiles/message.xml'), 'rb') as file:
    xml_data = file.read()

# Send the XML data to the client
client_socket.sendall(xml_data)

# Close the sockets
client_socket.close()
server_socket.close()
