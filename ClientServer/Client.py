import socket

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server's address and port
server_address = ('localhost', 8888)
client_socket.connect(server_address)
print('Connected to {}:{}'.format(*server_address))

# Receive the XML data from the server
xml_data = client_socket.recv(4096)

# Save the received XML data to a file
with open('received_file.xml', 'wb') as file:
    file.write(xml_data)

# Close the socket
client_socket.close()