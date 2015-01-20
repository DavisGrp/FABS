""""Copyright 2014 by the Cornell University and the Cornell Research Foundation, Inc. All Rights Reserved.
This file is part of LegoSpec.

LegoSpec is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
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
FluorImagepath = os.path.abspath("UI_Files/FluorImageWindow.ui")
form_class = uic.loadUiType(str(FluorImagepath))[0]


class MyFluorImageClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btndecr.clicked.connect(self.btndecr_clicked)
        self.btnrot.clicked.connect(self.btnrot_clicked)
        self.btncrop.clicked.connect(self.btncrop_clicked)
        self.btncal.clicked.connect(self.btncal_clicked)
        
    def btndecr_clicked(self):
        referencename = str(self.Refnameedit.text())
        spectrumname = str(self.Specnameedit.text())
        livetitle = self.fluornameedit.text()
        im=Image.open(referencename + '.jpg') #turns the reference into a colorless image
        factor = float(self.factor.value())
        im.convert("L", (.333*factor,333*factor,.333*factor,0)).save("decolorized_"+ referencename + '.jpg')
        im = Image.open("decolorized_" + referencename + '.jpg')
        g = str(im.getextrema())
        chop = g.index(',')
        max = g[(int(chop)+2):(len(g)-1)]
        if int(max) == 255:
            d = cv2.imread("decolorized_" + str(livetitle) + '.jpg')
            satpix = str(list(d)).count('255')
            print str(satpix) + ' number of sat pixels'
            w, h = im.size
            tpix = int(w)*int(h)
            print str(tpix) + ' total pixels'
            percsat = float(satpix)/float(tpix)
            self.Responses.append(str(percsat) + '% of pixels are saturated')
        self.Responses.append("decolorized reference saved as decolorized_" + referencename + '.jpg, max pixel value out of 255 is ' + str(255))
        
        sim=Image.open(spectrumname + '.jpg') # turns the sample into a colorless image
        im.convert("L", (.333*factor,333*factor,.333*factor)).save("decolorized_" + spectrumname + '.jpg')
        im = Image.open("decolorized_" + spectrumname + '.jpg')
        g = str(im.getextrema())
        chop = g.index(',')
        max = g[(int(chop)+2):(len(g)-1)]
        if int(max) == 255:
            d = cv2.imread("decolorized_" + str(livetitle) + '.jpg')
            satpix = str(list(d)).count('255')
            w, h = im.size
            tpix = w*h
            percsat = float(satpix)/float(tpix)
            self.Responses.append(str(percsat) + '% of pixels are saturated')
        self.Responses.append("decolorized reference saved as decolorized_" + spectrumname + '.jpg, max pixel value out of 255 is ' + str(255))
        
        
        webbrowser.open("decolorized_"+referencename + '.jpg')
        webbrowser.open("decolorized_"+spectrumname + '.jpg')
        self.Responses.append('type in the x and y pixel coordinates of the left and right corners of these spectra in the appropriate boxes')
        self.Responses.append('If the coordinates are not the same for both spectra, start over with spectra that match better')

    def btnrot_clicked(self):
        referencename = str(self.Refnameedit.text())
        spectrumname = str(self.Specnameedit.text())
        ry = self.ryspin.value() # set the endpoints of the spectrum
        rx = self.rxspin.value()
        ly = self.lyspin.value()
        lx = self.lxspin.value()
        height = ry-ly
        length = rx-lx
        mim = Image.open("decolorized_" + referencename + '.jpg')
        
#this does the actual rotation

        if height >= 0:
            if length >= 0:
                theta = math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + referencename + '.jpg')
            elif length <0:
                length = -length
                theta = 180-math.degrees(math.atan(float(height)/(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + referencename + '.jpg')
        elif height <0:
            height = -height
            if length >=0:
                theta = 360-math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + referencename + '.jpg')
            elif length <0:
                theta = 180+math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + referencename + '.jpg')
        else:
            self.Responses.append('something is wrong')
            quit()
        mim = Image.open("decolorized_"+spectrumname + '.jpg')
        if height >= 0:
            if length >= 0:
                theta = math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +spectrumname + '.jpg')
            elif length <0:
                length = -length
                theta = 180-math.degrees(math.atan(float(height)/(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +spectrumname + '.jpg')
        elif height <0:
            height = -height
            if length >=0:
                theta = 360-math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +spectrumname + '.jpg')
            elif length <0:
                theta = 180+math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +spectrumname + '.jpg')
        else:
            self.Responses.append('something is wrong')
        
        self.Responses.append('rotated sample spectrum saved as rotated_" + spectrumname')
        self.Responses.append('rotated reference spectrum saved as rotated_" + referencename')

#this section displays the spectra to make sure they are flat

        webbrowser.open("rotated_" + referencename + '.jpg')
        webbrowser.open("rotated_" + spectrumname + '.jpg')
        self.Responses.append('If these are both flat, move on - otherwise, try again with different coordinates')
        self.Responses.append('enter the values of the rightmost, leftmost, highest and lowest pixels where appropriate')

# this part does the cropping and binning

    def btncrop_clicked(self):
        referencename = str(self.Refnameedit.text())
        spectrumname = str(self.Specnameedit.text())

        left = self.leftspin.value()
        right = self.rightspin.value()
        ceiling = self.ceilingspin.value()
        floor = self.floorspin.value()
        box = (left, ceiling, right, floor)

        cim = Image.open("rotated_" + referencename + '.jpg')
        cim.crop(box).save("cropped" + referencename + '.jpg')
        cim = Image.open("rotated_" + spectrumname + '.jpg')
        cim.crop(box).save("cropped" + spectrumname + '.jpg')
        self.Responses.append('files have been cropped, proceeding to binning')

# cropping is finished, begins binning by measuring dimensions of cropped file
        bim = Image.open("cropped" + referencename + '.jpg')
        startarea = str(bim).index('size=')+5
        tail = str(bim)[startarea:]
        endoftail = tail.index('at')
        important = tail[:(endoftail-1)]
        endoflength = important.index('x')
        totallength = important[:endoflength]
        totalheight = important[(endoflength+1):]
        left = 0
        right = int(totallength)

# splits the reference image into rows and saves them

        i = 0
        while i <= int(totalheight)-1:
            floor = 1 + int(i)
            ceiling = int(floor) - 1
            i = int(i)+1
            box = (left, ceiling, int(right), floor)
            rim = Image.open("cropped" + referencename + '.jpg')
            rim.crop(box).save("cropped_row" + str(int(i)) + referencename + '.jpg')
        else:
            self.Responses.append('image has been split into rows')
            

# grabs intensity data from reference image and saves it to a new .txt for each row

        newref = referencename + 'txt'
        i = 0
        while i <= int(totalheight)-1:
            i = int(i) + 1
            tim = Image.open("cropped_row" + str(int(i)) + referencename + '.jpg')
            retrieve = list(tim.getdata())
            write = open(newref + str(int(i)) + '.txt', 'w')
            json.dump(retrieve, write)
            write.close()
            q = i
        else:
            self.Responses.append('intensity data recorded')


        i = 0
        while i <= (q-1):
            i = int(i)+1
            os.remove('cropped_row' + str(i) + referencename + '.jpg')
        else:
            self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows for the reference


        originalread = open(newref + '1.txt', 'r')
        originaltranscript = json.load(originalread)
        i = 0
        while i <= int(totalheight)-2:
            i = int(i)+1
            read = open(newref + str((int(i)+1)) + '.txt', 'r')
            transcript = json.load(read)
            originaltranscript = map(sum,zip(originaltranscript, transcript))
            read.close()
        else:
            print "rows have been summed"

# deletes the .txt files the intensity data was stored in for the reference
        i = 0
        originalread.close()
        while i <= (q-1):
            i = int(i)+1
            os.remove(newref+ str(i) + '.txt')
        else:
            print 'row intensity data  for reference removed'

# shows plot for reference spectrum
# if you click the graph something bad happens
        plt.figure(1)
        plt.plot(originaltranscript)
        plt.minorticks_on()
        plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
        plt.xlabel('Pixel number', color= 'k')
        plt.ylabel('Intensity (arb units)', color='k')
        plt.suptitle('Calibration Graph')
        plt.savefig(referencename + 'graph.png', frameon=True)
        webbrowser.open(referencename + 'graph.png')
        self.Responses.append('for calibration: enter the pixel and corresponding wavelength for two points on this graph, then move on to the fluorescence or absorption sections further to the right')


    def btncal_clicked(self):
        plt.close(1)
        spectrumname = str(self.Specnameedit.text())
        spectrumname = spectrumname + '.jpg'
        lp = self.lpspin.value()
        lc = self.lcspin.value()
        rp = self.rpspin.value()
        rc = self.rcspin.value()
        dp = rp-lp
        dc = rc-lc
        step = float(dc)/float(dp)

# splits the SPECTRUM into rows and saves them
        bim = Image.open("cropped" + spectrumname)
        startarea = str(bim).index('size=')+5
        tail = str(bim)[startarea:]
        endoftail = tail.index('at')
        important = tail[:(endoftail-1)]
        endoflength = important.index('x')
        totallength = important[:endoflength]
        totalheight = important[(endoflength+1):]
        left = 0
        right = int(totallength)

        i = 0
        while i <= int(totalheight)-1:
            floor = 1 + int(i)
            ceiling = int(floor) - 1
            i = int(i)+1
            box = (left, ceiling, int(right), floor)
            rim = Image.open("cropped" + spectrumname)
            rim.crop(box).save("cropped_row" + str(int(i)) + spectrumname)
        else:
            print 'done'

# grabs intensity data from spectrum image and saves it to a new .txt for each row

        newspec = spectrumname + 'txt'
        i = 0
        while i <= int(totalheight)-1:
            i = int(i) + 1
            tim = Image.open("cropped_row" + str(int(i)) + spectrumname)
            retrieve = list(tim.getdata())
            write = open(newspec + str(int(i)) + '.txt', 'w')
            json.dump(retrieve, write)
            write.close()
            q = i
        else:
            print 'done'

# removes cropped row images
        i = 0
        while i <= (q-1):
            i = int(i)+1
            os.remove('cropped_row' + str(i) + spectrumname)
        else:
            print 'done'

# adds up intensity data for all rows of the spectrum

        originalread = open(newspec + '1.txt', 'r')
        originaltranscript = json.load(originalread)
        i = 0
        while i <= int(totalheight)-2:
            i = int(i)+1
            read = open(newspec + str((int(i)+1)) + '.txt', 'r')
            transcript = json.load(read)
            originaltranscript = map(sum,zip(originaltranscript, transcript))
            read.close()
        else:
            print 'done'

# deletes the .txt files the intensity data was stored in for the sample
        i = 0
        originalread.close()
        while i <= (q-1):
            i = int(i)+1
            os.remove(newspec+ str(i) + '.txt')
        else:
            print 'done'

        livetitle = self.fluornameedit.text()
        y = originaltranscript
        xl = float(lc) - float(step)*float(lp)
        xr = float (rc) + float(step)*(float(totallength)-float(rp))
        x = np.arange(xl, xr, float(step))
        plt.figure(2)
        plt.plot(x, y)
        plt.minorticks_on()
        plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
        plt.xlabel('Wavelength /nm', color= 'k')
        plt.ylabel('Intensity (arb units)', color='k')
        plt.suptitle('Sample Intensity Graph')
        plt.savefig(str(self.Specnameedit.text()) + 'graph.png', frameon=True)
        if self.datacheck_2.isChecked():
                np.savetxt(name + '_fluor_data.csv', (x,y), delimiter = ',')
                self.Responses.append('you can open' + str(livetitle) + '_fluor_data.csv in excel.  To make the formatting nicer, select all cells with entries, copy, and paste them using the transpose function.  Then under cell styles change number format to comma')
        webbrowser.open(str(self.Specnameedit.text()) + 'graph.png')
        