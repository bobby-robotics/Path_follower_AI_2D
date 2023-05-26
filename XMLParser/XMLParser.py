import os
import xml.etree.ElementTree as ET
from datetime import datetime

import StringCompressionAndSplitting
from StringCompressionAndSplitting import StringCompressionAndSplitting

teststring = "rrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrr"
class XMLParser:

    @staticmethod
    def parseToXML(string):
        root = ET.Element("msg")
        tree = ET.ElementTree(root)

        target = ET.SubElement(root, "target")
        target.text = "target"

        seq = ET.SubElement(root, "seq")
        seqList = []

        for s in range(1, len(string)+1):
            seqList.append(ET.SubElement(seq, "s" + "{:02d}".format(s)))
            seqList[s-1].text = string[s-1]


        xml_message = ET.tostring(root, encoding="utf-8", method="xml")

        cwd = os.getcwd
        cwd = cwd() + "\\XMLFiles\\"
        print(cwd)
        #tree.write(cwd + "message.xml", encoding="utf-8", xml_declaration=True)
        tree.write(cwd + "message" + datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ".xml", encoding="utf-8", xml_declaration=True)


compressedTest = StringCompressionAndSplitting.CompressString(teststring)
print(compressedTest)

splittedTest = StringCompressionAndSplitting.splitString(compressedTest)
print(splittedTest)

XMLParser.parseToXML(splittedTest)

