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
AbsImagepath = os.path.abspath("UI_Files/AbsImagewindow.ui")
form_class = uic.loadUiType(str(AbsImagepath))[0]

        
class MyAbsImageClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btndecrAbs.clicked.connect(self.btndec_clicked)
        self.btnrotAbs.clicked.connect(self.btnrot_clicked)
        self.btncropAbs.clicked.connect(self.btncrop_clicked)
        self.btncalcabs.clicked.connect(self.btncalcabs_clicked)
        
    def btndec_clicked(self):
        referencename = str(self.Refnameedit2.text())
        spectrumname = str(self.Specnameedit2.text())
        lightname = str(self.lightname.text())
        im=Image.open(referencename + '.jpg') #turns the reference into a colorless image
        im.convert("L").save("decolorized_"+ referencename + '.jpg')
        im = Image.open("decolorized_" + referencename + '.jpg')
        g = str(im.getextrema())
        chop = g.index(',')
        max = g[(int(chop)+2):(len(g)-1)]
        if int(max) == 255:
            d = cv2.imread("decolorized_" + str(referencename) + '.jpg')
            satpix = str(list(d)).count('255')
            print str(satpix) + ' number of sat pixels'
            w, h = im.size
            tpix = int(w)*int(h)
            print str(tpix) + ' total pixels'
            percsat = float(satpix)/float(tpix)
            self.Responses.append(str(percsat) + '% of pixels are saturated')
        self.Responses.append("decolorized reference saved as decolorized_" + referencename + '.jpg, max pixel value out of 255 is ' + str(255))
        
        sim=Image.open(lightname + '.jpg') # turns the light spectrum into a colorless image
        im.convert("L").save("decolorized_" + lightname + '.jpg')
        im = Image.open("decolorized_" + lightname + '.jpg')
        g = str(im.getextrema())
        chop = g.index(',')
        max = g[(int(chop)+2):(len(g)-1)]
        if int(max) == 255:
            d = cv2.imread("decolorized_" + str(lightname) + '.jpg')
            satpix = str(list(d)).count('255')
            w, h = im.size
            tpix = w*h
            percsat = float(satpix)/float(tpix)
            self.Responses.append(str(percsat) + '% of pixels are saturated')
        self.Responses.append("decolorized reference saved as decolorized_" + lightname + '.jpg, max pixel value out of 255 is ' + str(255))
        
        
        sim=Image.open(spectrumname + '.jpg') # turns the sample into a colorless image
        im.convert("L").save("decolorized_" + spectrumname + '.jpg')
        im = Image.open("decolorized_" + spectrumname + '.jpg')
        g = str(im.getextrema())
        chop = g.index(',')
        max = g[(int(chop)+2):(len(g)-1)]
        if int(max) == 255:
            d = cv2.imread("decolorized_" + str(spectrumname) + '.jpg')
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
        referencename = str(self.Refnameedit2.text())
        spectrumname = str(self.Specnameedit2.text())
        lightname = str(self.lightname.text())
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
        mim = Image.open("decolorized_" + spectrumname + '.jpg')
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
        
        mim = Image.open("decolorized_" + lightname + '.jpg') # rotates the light image
        if height >= 0:
            if length >= 0:
                theta = math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +lightname + '.jpg')
            elif length <0:
                length = -length
                theta = 180-math.degrees(math.atan(float(height)/(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +lightname + '.jpg')
        elif height <0:
            height = -height
            if length >=0:
                theta = 360-math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +lightname + '.jpg')
            elif length <0:
                theta = 180+math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" +lightname + '.jpg')
        else:
            self.Responses.append('something is wrong')
        
        self.Responses.append('rotated sample spectrum saved as rotated_' + spectrumname)
        self.Responses.append('rotated reference spectrum saved as rotated_' + referencename)
        self.Responses.append('rotated light spectrum saved as rotated_' + lightname)

#this section displays the spectra to make sure they are flat

        webbrowser.open("rotated_" + referencename + '.jpg')
        webbrowser.open("rotated_" + spectrumname + '.jpg')
        webbrowser.open("rotated_" + lightname + '.jpg')
        self.Responses.append('If these are both flat, move on - otherwise, try again with different coordinates')
        self.Responses.append('enter the values of the rightmost, leftmost, highest and lowest pixels where appropriate')

# this part does the cropping and binning

    def btncrop_clicked(self):
        referencename = str(self.Refnameedit2.text())
        spectrumname = str(self.Specnameedit2.text())
        lightname = str(self.lightname.text())

        left = self.leftspin.value()
        right = self.rightspin.value()
        ceiling = self.ceilingspin.value()
        floor = self.floorspin.value()
        box = (left, ceiling, right, floor)

        cim = Image.open("rotated_" + referencename + '.jpg')
        cim.crop(box).save("cropped" + referencename + '.jpg')
        cim = Image.open("rotated_" + spectrumname + '.jpg')
        cim.crop(box).save("cropped" + spectrumname + '.jpg')
        cim = Image.open("rotated_" + lightname + '.jpg')
        cim.crop(box).save("cropped" + lightname + '.jpg')
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


    def btncalcabs_clicked(self):
            referencename = str(self.Refnameedit2.text())
            spectrumname = str(self.Specnameedit2.text())
            lightname = str(self.lightname.text())
            bim = Image.open("cropped" + spectrumname + '.jpg')
            startarea = str(bim).index('size=')+5
            tail = str(bim)[startarea:]
            endoftail = tail.index('at')
            important = tail[:(endoftail-1)]
            endoflength = important.index('x')
            totallength = important[:endoflength]
            totalheight = important[(endoflength+1):]
            left = 0
            right = int(totallength)

# splits the image into rows and saves them

            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                floor = 1 + int(i)
                ceiling = int(floor) - 1
                i = int(i)+1
                box = (left, ceiling, int(right), floor)
                rim = Image.open("cropped" + spectrumname + '.jpg')
                rim.crop(box).save("cropped_row" + str(int(i)) + spectrumname + '.jpg')
            else:
                self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row

            newspectrumname = spectrumname + 'txt'
            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                i = int(i) + 1
                tim = Image.open("cropped_row" + str(int(i)) + spectrumname + '.jpg')
                retrieve = list(tim.getdata())
                write = open(newspectrumname + str(int(i)) + '.txt', 'w')
                json.dump(retrieve, write)
                write.close()
                q = i
                p = i
            else:
                self.Responses.append('intensity data recorded')

            i = 0
            while i <= (q-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove('cropped_row' + str(i) + spectrumname + '.jpg')
            else:
                self.Responses.append('cropped row images removed')
#
#
# gets the background spectrum set up
            if self.backgroundcheck_2.isChecked():
                leftb = self.leftlivespin.value()
                rightb = self.rightlivespin.value()
                ceilingb = self.ceilinglivespin.value() - 20
                floorb = self.ceilinglivespin.value() - 10
                boxb = (leftb, ceilingb, rightb, floorb)

                cim = Image.open("rotated_" + str(spectrumname) + '.jpg')
                blur2 = cim.filter(PIL.ImageFilter.BLUR)
                blur2.save('blurred2b' + spectrumname + '.jpg')
                redun2 = Image.open('blurred2b' + spectrumname + '.jpg')
                redun2.crop(boxb).save('croppedb' + spectrumname + '.jpg')

                bim = Image.open("croppedb" + str(spectrumname) + '.jpg')
                startarea = str(bim).index('size=')+5
                tail = str(bim)[startarea:]
                endoftail = tail.index('at')
                important = tail[:(endoftail-1)]
                endoflength = important.index('x')
                totallength = important[:endoflength]
                totalheight = important[(endoflength+1):]
                left = 0
                right = int(totallength)

# splits the image into rows and saves them

                i = 0
                while i <= int(totalheight)-1:
                    floor = 1 + int(i)
                    ceiling = int(floor) - 1
                    i = int(i)+1
                    box = (left, ceiling, int(right), floor)
                    rim = Image.open("croppedb" + str(spectrumname) + '.jpg')
                    rim.crop(box).save("cropped_rowb" + str(int(i)) + str(spectrumname) + '.jpg')
                else:
                    self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row
        
                newspectrumnameb = str(spectrumname) + 'txtb'
                i = 0
                while i <= int(totalheight)-1:
                    i = int(i) + 1
                    tim = Image.open("cropped_rowb" + str(int(i)) + str(spectrumname) + '.jpg')
                    retrieve = list(tim.getdata())
                    write = open(newspectrumnameb + str(int(i)) + '.txt', 'w')
                    json.dump(retrieve, write)
                    write.close()
                    q = i
                else:
                    self.Responses.append('intensity data recorded')


                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('cropped_rowb' + str(i) + str(spectrumname) + '.jpg')
                else:
                    self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

                originalreadb = open(newspectrumnameb + '1.txt', 'r')
                originaltranscriptb = json.load(originalreadb)
                i = 0
                while i <= int(totalheight)-2:
                    i = int(i)+1
                    read = open(newspectrumnameb + str((int(i)+1)) + '.txt', 'r')
                    transcriptb = json.load(read)
                    originaltranscriptb = map(sum,zip(originaltranscriptb, transcriptb)) # this gives a list of the background
                    read.close()
                else:
                    print "rows have been summed"

# deletes the .txt files the intensity data was stored in for the reference
                i = 0
                originalreadb.close()
                while i <= (q-1):
                    i = int(i)+1
                    os.remove(newspectrumnameb + str(i) + '.txt')
                else:
                    print 'row intensity data  for reference removed'
                B = list()
                for item in originaltranscriptb:
                    B.append(-int(item))
            else:
                print 'skipping background subtraction'
#
#
# adds up intensity data for all rows

            originalreads = open(newspectrumname + '1.txt', 'r')
            originaltranscripts = json.load(originalreads)
            i = 0
            while i <= int(totalheight)-2:
                QtGui.qApp.processEvents()
                i = int(i)+1
                reads = open(newspectrumname + str((int(i)+1)) + '.txt', 'r')
                transcripts = json.load(reads)
                originaltranscripts = map(sum,zip(originaltranscripts, transcripts))
                reads.close()
            else:
                print 'rows added up'
                
            if self.backgroundcheck_2.isChecked():
                originaltranscripts = map(sum,zip(originaltranscripts,B))
            else:
                print 'not subtracting sample background'
            write = open('samplelist' + spectrumname + '.txt', 'w') # saves final list for sample
            json.dump(originaltranscripts, write)
            write.close()
# deletes the .txt files the intensity data was stored in
            i = 0
            originalreads.close()
            while i <= (p-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove(newspectrumname + str(i) + '.txt')
            else:
                print 'row intensity data  for light graph removed'
#
#
#
#
#Does the same thing for the light spectrum - 
            bim = Image.open("cropped" + lightname + '.jpg')
            startarea = str(bim).index('size=')+5
            tail = str(bim)[startarea:]
            endoftail = tail.index('at')
            important = tail[:(endoftail-1)]
            endoflength = important.index('x')
            totallength = important[:endoflength]
            totalheight = important[(endoflength+1):]
            left = 0
            right = int(totallength)

# splits the image into rows and saves them

            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                floor = 1 + int(i)
                ceiling = int(floor) - 1
                i = int(i)+1
                box = (left, ceiling, int(right), floor)
                rim = Image.open("cropped" + lightname + '.jpg')
                rim.crop(box).save("cropped_row" + str(int(i)) + lightname + '.jpg')
            else:
                self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row

            newlightname = lightname + 'txt'
            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                i = int(i) + 1
                tim = Image.open("cropped_row" + str(int(i)) + lightname + '.jpg')
                retrieve = list(tim.getdata())
                write = open(newlightname + str(int(i)) + '.txt', 'w')
                json.dump(retrieve, write)
                write.close()
                q = i
                p = i
            else:
                self.Responses.append('intensity data recorded')

            i = 0
            while i <= (q-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove('cropped_row' + str(i) + lightname + '.jpg')
            else:
                self.Responses.append('cropped row images removed')
#
#
# gets the background spectrum set up
            if self.backgroundcheck_2.isChecked():
                leftb = self.leftlivespin.value()
                rightb = self.rightlivespin.value()
                ceilingb = self.ceilinglivespin.value() - 20
                floorb = self.ceilinglivespin.value() - 10
                boxb = (leftb, ceilingb, rightb, floorb)

                cim = Image.open("rotated_" + str(lightname) + '.jpg')
                blur2 = cim.filter(PIL.ImageFilter.BLUR)
                blur2.save('blurred2b' + lightname + '.jpg')
                redun2 = Image.open('blurred2b' + lightname + '.jpg')
                redun2.crop(boxb).save('croppedb' + lightname + '.jpg')

                bim = Image.open("croppedb" + str(lightname) + '.jpg')
                startarea = str(bim).index('size=')+5
                tail = str(bim)[startarea:]
                endoftail = tail.index('at')
                important = tail[:(endoftail-1)]
                endoflength = important.index('x')
                totallength = important[:endoflength]
                totalheight = important[(endoflength+1):]
                left = 0
                right = int(totallength)

# splits the image into rows and saves them

                i = 0
                while i <= int(totalheight)-1:
                    floor = 1 + int(i)
                    ceiling = int(floor) - 1
                    i = int(i)+1
                    box = (left, ceiling, int(right), floor)
                    rim = Image.open("croppedb" + str(lightname) + '.jpg')
                    rim.crop(box).save("cropped_rowb" + str(int(i)) + str(lightname) + '.jpg')
                else:
                    self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row
        
                newlightnameb = str(lightname) + 'txtb'
                i = 0
                while i <= int(totalheight)-1:
                    i = int(i) + 1
                    tim = Image.open("cropped_rowb" + str(int(i)) + str(lightname) + '.jpg')
                    retrieve = list(tim.getdata())
                    write = open(newlightnameb + str(int(i)) + '.txt', 'w')
                    json.dump(retrieve, write)
                    write.close()
                    q = i
                else:
                    self.Responses.append('intensity data recorded')


                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('cropped_rowb' + str(i) + str(lightname) + '.jpg')
                else:
                    self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

                originalreadb = open(newlightnameb + '1.txt', 'r')
                originaltranscriptb = json.load(originalreadb)
                i = 0
                while i <= int(totalheight)-2:
                    i = int(i)+1
                    read = open(newlightnameb + str((int(i)+1)) + '.txt', 'r')
                    transcriptb = json.load(read)
                    originaltranscriptb = map(sum,zip(originaltranscriptb, transcriptb)) # this gives a list of the background
                    read.close()
                else:
                    print "rows have been summed"

# deletes the .txt files the intensity data was stored in for the reference
                i = 0
                originalreadb.close()
                while i <= (q-1):
                    i = int(i)+1
                    os.remove(newlightnameb + str(i) + '.txt')
                else:
                    print 'row intensity data  for reference removed'
                B = list()
                for item in originaltranscriptb:
                    B.append(-int(item))
            else:
                print 'skipping background subtraction'
#
#
# adds up intensity data for all rows

            originalreads = open(newlightname + '1.txt', 'r')
            originaltranscripts = json.load(originalreads)
            i = 0
            while i <= int(totalheight)-2:
                QtGui.qApp.processEvents()
                i = int(i)+1
                reads = open(newlightname + str((int(i)+1)) + '.txt', 'r')
                transcripts = json.load(reads)
                originaltranscripts = map(sum,zip(originaltranscripts, transcripts))
                reads.close()
            else:
                print 'rows added up'
                
            if self.backgroundcheck_2.isChecked():
                originaltranscripts = map(sum,zip(originaltranscripts,B))
            else:
                print 'not subtracting sample background'
            write = open('lightlist' + lightname + '.txt', 'w') # saves final list for sample
            json.dump(originaltranscripts, write)
            write.close()
# deletes the .txt files the intensity data was stored in
            i = 0
            originalreads.close()
            while i <= (p-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove(newlightname + str(i) + '.txt')
            else:
                print 'row intensity data  for light graph removed'

#end of the light spectrum section

###this part corresponds to the calc abs section of the main module.

            name = str(self.absnameedit2.text())
            readsamp = open('samplelist' + spectrumname + '.txt', 'r')
            transcriptsamp = json.load(readsamp)
            S = list()
            for item in transcriptsamp: # the sample needs to be negative, not the blank
                if math.copysign(1,item) == -1:
                    S.append(0)
                elif item == 0:
                    S.append(0)
                else:
                    S.append(-(math.log10(item))) # requires negative values since we need a subtraction below (log subtraction = division)
            readlight = open('lightlist' + lightname + '.txt', 'r')
            transcriptlight = json.load(readlight)
            L = list() # moves log of positive values to new list
            for item in transcriptlight:
                if math.copysign(1,item) == -1: # if values are negative, it appends 0 instead of taking the log
                    L.append(0)
                elif item == 0: # if they're 0 it does the same so math.log10 can deal with everything
                    L.append(0)
                else:
                    L.append(math.log10(item)) # takes log if the values are neither 0 nor negative
            y = map(sum,zip(S, L)) # performs the subtraction equivalent to: LOG(I0/I) = LOG(I0) - LOG(I) - gives abs values
    
# this part turns X from pixels into nanometers
            
            sampletitle = spectrumname
            bim = Image.open("cropped" + sampletitle + '.jpg')
            startarea = str(bim).index('size=')+5
            tail = str(bim)[startarea:]
            endoftail = tail.index('at')
            important = tail[:(endoftail-1)]
            endoflength = important.index('x')
            totallength = important[:endoflength]
            lp = self.lpspinabs.value()
            lc = self.lcspinabs.value()
            rp = self.rpspinabs.value()
            rc = self.rcspinabs.value()
            dp = rp-lp
            dc = rc-lc
            step = float(dc)/float(dp)
            xl = float(lc) - float(step)*float(lp)
            xr = float (rc) + float(step)*(float(totallength)-float(rp))
            x = np.arange(xl, xr, float(step)) # left bound, right bound, step size
            print str(len(x)) + ' entries for X'
            print str(len(y)) + ' entries for Y'
            while len(x) != len(y): # makes sure x and y are the same length
                if len(x) > len(y):
                    x = np.arange(xl, xr - float(step), float(step))
                    print str(len(x)) + ' entries for X'
                    print str(len(y)) + ' entries for Y'
                elif len(y) > len(x):
                    x = np.arange(xl, xr + float(step), float(step))
                    print str(len(x)) + ' entries for X'
                    print str(len(y)) + ' entries for Y'
                else:
                    print 'x and y are the same size'
            if not self.peakcheck.isChecked():
                plt.plot(x, y)
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('Absorption', color='k')
                plt.suptitle('Absorption Graph')
                plt.savefig(name + 'graph.png', frameon=True)
                webbrowser.open(name + 'graph.png')
                if self.datacheck_2.isChecked():
                    np.savetxt(name + '_absim_data_unadjusted.csv', (x, y), delimiter = ',')
                    self.Responses.append('CSV saved as '+ str(name) + '_absim_data_unadjusted.csv')
            if self.peakcheck.isChecked():
                yclone = y[:]
                yclone2 = y[:]
                ynew = list() # this part finds the acceleration
                lengthofy = len(y)
                n = 0
                while n < (lengthofy-1):
                    try:
                        ynew.append(y.pop(0)-y.pop(0))
                        y.insert(0, yclone.pop(1))
                    except IndexError:
                        break
                ynewclone = ynew[:]
                ynew2 = list()
                lengthofynew = len(ynew)
                n = 0
                while n < lengthofynew:
                    try:
                        ynew2.append(ynew.pop(1)-ynew.pop(0)) # gets change in change of y
                        ynew.insert(0, ynewclone.pop(1))
                    except IndexError:
                        break
                adjustments = list()
                n = 0
                lsignal = self.lsignal.value()
                rsignal = self.rsignal.value()
                lsig = (int(lsignal) - int(xl))/step
                rsig = (int(rsignal)-int(xl))/step
                print str(lsig)
                print str(rsig)
                for item in ynew2:
                    n = n+1
                    if float(item) == float(item):
                        if n < int(lsig):
                            adjustments.append(-10)
                        elif n>int(rsig):
                            adjustments.append(-10)
                        else: adjustments.append(item)
                    else:
                        adjustments.append(item)
                correctedyfirst = map(sum,zip(yclone2, adjustments))
                correctedyfinal = list()
                for item in correctedyfirst:
                    if float(item) < 0:
                        correctedyfinal.append(0)
                    else:
                        correctedyfinal.append(item)
                correctedyfinal.append(0)
                correctedyfinal.append(0)
                str(correctedyfinal) + 'corrected y final'
                plt.close('all')
                print str(len(correctedyfinal)) + ' corrected y final'
                print str(len(x)) + ' len x'
                plt.plot(x,correctedyfinal)
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('adjusted Absorption', color='k')
                plt.suptitle('Adjusted Absorption Graph')
                plt.savefig(name + 'adjustedgraph.png', frameon=True)
                webbrowser.open(name + 'adjustedgraph.png')
                if self.datacheck_2.isChecked():
                    np.savetxt(name + '_absim_data_adjusted.csv', (x, correctedyfinal), delimiter = ',')
                    self.Responses.append('CSV saved as '+ str(name) + '_absim_data_adjusted.csv')
                
