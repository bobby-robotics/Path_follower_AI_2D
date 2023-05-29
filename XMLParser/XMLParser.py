import os
import xml.etree.ElementTree as ET
from datetime import datetime


teststring = "rrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrr"
class XMLParser:

    @staticmethod
    def parseToXML(string):
        root = ET.Element("msg")
        tree = ET.ElementTree(root)

        target = ET.SubElement(root, "target")
        target.text = "Start"

        if not string == "":

            seq = ET.SubElement(root, "seq")
            seqList = []

            for s in range(1, len(string)+1):
                seqList.append(ET.SubElement(seq, "s" + "{:02d}".format(s)))
                seqList[s-1].text = string[s-1]




        #check directory

        cwd = os.getcwd

        cwd = cwd() + "\\XMLParser\\XMLFiles\\"
        if not os.path.exists(cwd):
            os.makedirs(cwd)

        tree.write(cwd + "message" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ".xml", encoding="utf-8", xml_declaration=True)

