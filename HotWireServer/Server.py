import socket
from threading import Thread
import time
import xml.etree.ElementTree as ET

from Q_learning.training import training
from XMLParser.StringCompressionAndSplitting import StringCompressionAndSplitting
from XMLParser.XMLParser import XMLParser
from Bildverarbeitung.Final.take_pic import take_pic

# ******************************************************************************
# Settings
# ******************************************************************************
SRV_IP = '0.0.0.0'
SRV_PORT = 1415
BUFF_SIZE = 1024
LBR_IP = "10.84.57.105"

ai_state = 0
ai_sequence = ""
ai_config = ""

camerainput = 1


# ******************************************************************************
# Common methods and functions
# ******************************************************************************
def str_to_bytes(s: str):
    """Convert string into bytes.
    :param s: String to convert.
    :return: Bytes representation of string s.
    """
    return bytes(s, 'utf-8')


def bytes_to_str(b: bytes):
    """Convert bytes into string.
    :param b: Bytes to convert.
    :return: String representation of bytes b.
    """
    return str(b, 'utf-8')

# ******************************************************************************
# TCP-client's thread
# ******************************************************************************
class ClientThread(Thread):
    """TCP-client's thread."""

    def __init__(self, conn, ip, port, buff_size):
        Thread.__init__(self)
        self.conn = conn
        self.ip = ip
        self.port = port
        self.buff_size = buff_size
        print("\nCONNECTED    | Client's IP: {}:{}".format(ip, port))

    def run(self):
        global ai_state
        global ai_sequence
        global ai_config

        print("Server started")

        while True:
            try:
                data = self.conn.recv(self.buff_size)
                if not data:
                    print("LBR_DISCONNECT |")
                    break
                else:
                    print("RCV_FROM_LBR | {}".format(data))
                    data = bytes_to_str(data)
                    to_send = ""

                    xmlWait =       ET.tostring(ET.parse("XMLParser/XMLFiles/messageWait.xml").getroot(), encoding='utf-8').decode('utf-8')
                    xmlRecord =     ET.tostring(ET.parse("XMLParser/XMLFiles/messageGoToRecord.xml").getroot(), encoding='utf-8').decode('utf-8')
                    xmlStart =      ET.tostring(ET.parse("XMLParser/XMLFiles/messageGoToStart.xml").getroot(), encoding='utf-8').decode('utf-8')
                    xmlMessage =    ET.tostring(ET.parse("XMLParser/XMLFiles/message.xml").getroot(), encoding='utf-8').decode('utf-8')
                    xmlEnd =        ET.tostring(ET.parse("XMLParser/XMLFiles/messageGoToEnd.xml").getroot(), encoding='utf-8').decode('utf-8')

                    if data == "HotWireStarted":
                        to_send = xmlRecord
                    elif data == "OnRecord":
                        if ai_state == 0:
                            # AI thread takes photo and calculates movement path
                            ai_state = 1
                            to_send = xmlWait
                        elif ai_state == 1:
                            # AI still calculates the movement path
                            to_send = xmlWait
                        elif ai_state == 2:
                            # AI is ready with the calculation and generates motion string
                            to_send = xmlMessage
                            ai_state = 0
                    elif data == "NoSeq":
                        to_send = xmlStart
                    elif data == "Finished":
                        to_send = xmlEnd
                    else:
                        to_send = ""

                    if to_send != "":
                        self.conn.send(str_to_bytes(to_send))
                        print("SENT_TO_LBR  | {}".format(to_send))
            except IOError as err:
                print("IO error: {0}".format(err))
                break
        print("DISCONNECTED | Client's IP: {}:{}".format(self.ip, self.port))


# ******************************************************************************
# Test AI class and thread
# ******************************************************************************
class AiThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        #self.ai = ai

    def run(self):
        global ai_state
        #global ai_sequence
        #global ai_config
        ai_sequence = ""
        ai_config = ""

        print("AI_THREAD    | AI thread started.")

        while True:
            if ai_state == 1:

                #fotoaufnahme
                img = take_pic().get_pic(camerainput)
                print("AI_THREAD    | Photo taken.")
                #hier q learner starten
                trainer = training(offset = 20, end_x= 530 ,visualise=True,execution=True)
                path = trainer.execute(img)
                #teststring = "rrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrr"
                split = StringCompressionAndSplitting.compressAndSplit(path)
                XMLParser.parseToXML(split)

                print("XML generated, sending to LBR")
                ai_state = 2

                break


# ******************************************************************************
# Multithreaded python server: TCP-server socket program
# ******************************************************************************
def server():
    """Multithreaded python server: TCP-server socket program."""
    clients = []

    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((SRV_IP, SRV_PORT))
        print("### SRV: started **************************************************")
        print("### SRV: waiting for connections from TCP clients on port-no: ", SRV_PORT)
        srv_run = True

    except socket.error as err:
        print("### SRV: some errors while starting:\n", err)
        srv_run = False
        exit(1)

    while srv_run:
        tcp_server.listen(1)
        (conn, (ip, port)) = tcp_server.accept()

        #fortesting:
        #conn, port = "", ""
        #ip = LBR_IP #delete after testing

        if ip == LBR_IP:  # only KUKA LBR4+ allowed
            new_client = ClientThread(conn, ip, port, BUFF_SIZE)
            new_client.start()
            clients.append(new_client)

    for item in clients:
        item.join()


def ai():

    ai_thread = AiThread()
    ai_thread.start()

