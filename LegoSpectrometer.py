""""Copyright 2014 by the Cornell University and the Cornell Research Foundation, Inc. All Rights Reserved.
This file is part of FABS.

FABS is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
as published by the Free Software Foundation, either version 3 of the License, or(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>."""

import sys
from PyQt4 import QtCore, QtGui, uic
import cv2
import cv2.cv as cv
import numpy as np
import time
import PIL
from PIL import Image
from PIL import ImageFilter
import os
import webbrowser
import json
import matplotlib.pyplot as plt
import math
import glob


optionswindowpath = os.path.abspath("UI_Files/initialwindow.ui")
form_class = uic.loadUiType(str(optionswindowpath))[0]
import AbsImage
import CamCalibrate
import FluorImage
import Videowindow

# 

class OptionsWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.BtnCamCalibrate.clicked.connect(self.BtnCamCalibrate_clicked) # for all webcam measurements
        self.BtnVideo.clicked.connect(self.BtnVideoProcessor_clicked) # for turning existing spectrum videos into images
        self.BtnFluorImage.clicked.connect(self.BtnFluorImage_clicked) # turns absorbance spectrum images into graphs
        self.BtnAbsImage.clicked.connect(self.handAbsImage) # turns fluorescence spectrum images into graphs
        self.Cleanupbtn.clicked.connect(self.Cleanupbtn_clicked)
                                         
    def Cleanupbtn_clicked(self): # list all PNG and JPEG files in the directory, then delete them.
        pngdir = str(os.getcwd()) + '\\*.png' 
        pnglist = glob.glob(str(pngdir))
        for item in pnglist:
            os.remove(str(item))
            
        jpgdir = str(os.getcwd()) + '\\*.jpg'
        jpglist = glob.glob(str(jpgdir))
        for item in jpglist:
            os.remove(str(item))
    
    def BtnCamCalibrate_clicked(self):
        myCamCalibrateWindow = CamCalibrate.MyCamCalibrateClass(myOptionsWindow)
        myCamCalibrateWindow.show()
        
    def BtnVideoProcessor_clicked(self):
        myVideoWindow = Videowindow.MyVideoClass(myOptionsWindow)
        myVideoWindow.show()
    
    def BtnFluorImage_clicked(self):
        myFluorImageWindow = FluorImage.MyFluorImageClass(myOptionsWindow)
        myFluorImageWindow.show()
        
    def handAbsImage(self):
        myAbsImageWindow = AbsImage.MyAbsImageClass(myOptionsWindow)
        myAbsImageWindow.show()
app = QtGui.QApplication(sys.argv)
myOptionsWindow = OptionsWindowClass(None)
myOptionsWindow.show()
app.exec_()