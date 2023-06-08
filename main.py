
from DataGenerator.fake_path_from_image import fake_path_from_image
from Bildverarbeitung.Calibration.four_points_method import four_points_method
from Bildverarbeitung.Final.take_pic import take_pic
import os
import cv2
import numpy as np
from math import sin,cos, pi,sqrt

from XMLParser.StringCompressionAndSplitting import StringCompressionAndSplitting
from XMLParser.XMLParser import XMLParser
from enum_motion import Motions
from cv2 import WINDOW_NORMAL
from Q_learning.training import training
import time
import HotWireServer.Server as server
import xml.etree.ElementTree as ET


def main():

    #teststring = "rrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrrrrrrdrdrddrcrdrcdrcrrrrwrrwurrwrurrrrruuuuwrrrururruuuuuwwuuuuulullluuuucuuuwuwrururrrrr"

    server.ai()
    server.server()


if __name__ == '__main__':
    main()


