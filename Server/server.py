
# Kommunikation über TCP/IP
# Serverprogramm auf einem Rechner ausführen und Client verwenden um Befehle an den Server zu senden und die Ausgabe zu empfangen
# Servercode und Clientcode müssen von der Befehlszeile ausgeführt werden

import socket
import subprocess

# IP-Adresse & Port für Server
Host = '123.0.0.1'  # Hostname eingeben
Port = 12345        # Portname eingeben

# Führt Befehl auf Server aus und gibt Ergebnis zurück
def run_command(command):
    result = subprocess.run(command, shell = True, capture_output = True, text = True)
    return result.stdout

# Socket initialisieren
# Auf mögliche Verbindungen warten
server_socket = socket.socket(socket.AF_INET, socket.SOCK.STREAM)
server_socket.bind((Host, Port))
server_socket.listen(1)

print(f'Server is running and is waiting for connections {Host}:{Port}...')


while True:
    # Verbindung akzeptieren
    # Client-Socket und Adresse speichern
    client_socket, address = server_socket.accept() 
    print('New connection is ready:', address)

    # Clientbefehl empfangen
    command = client_socket.recv(1024).decode()
    print('Receive command:', command)

    # Befehl ausführen
    output = run_command(command)

    # Ausgabe an Client senden
    client_socket.sendall(output.encode())

    # Verbindung zum Server schließen
    client_socket.close()