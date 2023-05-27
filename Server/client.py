
# Kommunikation über TCP/IP
# Serverprogramm auf einem Rechner ausführen und Client verwenden um Befehle an den Server zu senden und die Ausgabe zu empfangen
# Servercode und Clientcode müssen von der Befehlszeile ausgeführt werden

import socket

# IP-Adresse und Port für Server
Host = '127.0.0.1'  # IP-Adresse von Server eingeben
Port = 12345        # Portname eingeben

# Befehl der auf dem Server ausgeführt werden soll
command = input('Type in command:')

# Socket initialisieren
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Verbindung zum Server herstellen
client_socket.connect((Host, Port))

# Befehl an Server senden
client_socket.sendall(command.encode())

# Antwort vom Server empfangen und ausgeben
response = client_socket.recv(1024).decode()
print('Answer from server:', response)

# Verbindung zum Server schließen
client_socket.close()
