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
            config = ET.SubElement(root, "config")
            tSize = ET.SubElement(config, "tSize")
            rSize = ET.SubElement(config, "rSize")
            tSize.text = "1.3" # <-- hier die Stepsize eintragen (1 = 1mm)
            rSize.text = "45" # <-- hier die Winkelgröße eintragen (1 = 1°)

            seq = ET.SubElement(root, "seq")
            seqList = []

            if len(string) > 0:
                for s in range(1, len(string)+1):
                    seqList.append(ET.SubElement(seq, "s" + "{:02d}".format(s)))
                    seqList[s-1].text = string[s-1]
            cwd = os.getcwd
            cwd = cwd() + "\\XMLParser\\XMLFiles\\"
            if not os.path.exists(cwd):
                os.makedirs(cwd)
            tree.write(cwd + "message.xml", encoding="utf-8", xml_declaration=True)


