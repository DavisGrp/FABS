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
CamCalibrateWindowpath = os.path.abspath("UI_Files/CamCalibrateWindow.ui")
form_class = uic.loadUiType(str(CamCalibrateWindowpath))[0]


class MyCamCalibrateClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnlightspectrum.clicked.connect(self.btnlightspectrum_clicked)
        self.btnsamplespectrum.clicked.connect(self.btnsamplespectrum_clicked)
        self.btnShowVideo.clicked.connect(self.btnShowVideo_clicked)
        self.btntest.clicked.connect(self.btntest_clicked)
        self.btndeclive.clicked.connect(self.btndeclive_clicked)
        self.btnrotlive.clicked.connect(self.btnrotlive_clicked)
        self.btncroplive.clicked.connect(self.btncroplive_clicked)
        self.btnaddgraph.clicked.connect(self.btnaddgraph_clicked)
        self.btnspecviewer.clicked.connect(self.btntest_clicked)
        self.btncalcabs.clicked.connect(self.btncalcabs_clicked)
        self.bonus_button.clicked.connect(self.bonus_button_clicked)
        
        self.factor.hide()
        self.factor_2.hide()
        self.factor_3.hide()
        self.label_30.hide()
        self.label_33.hide()
        self.noframes.hide()
        self.blurcheck.hide()
        self.radioButton.hide()
        self.backgroundcheck.hide()
        self.backgroundcheck_2.hide()
        self.peakcheck.hide()
        self.lsignal.hide()
        self.rsignal.hide()
        self.label.hide()
        self.label_2.hide()
        self.average_box.hide()
        self.label_3.hide()
    
    def bonus_button_clicked(self):
        if self.factor.isHidden():
            self.factor.show()
            self.factor_2.show()
            self.factor_3.show()
            self.label_30.show()
            self.label_33.show()
            self.noframes.show()
            self.blurcheck.show()
            self.radioButton.show()
            self.backgroundcheck.show()
            self.backgroundcheck_2.show()
            self.peakcheck.show()
            self.lsignal.show()
            self.rsignal.show()
            self.label.show()
            self.label_2.show()
            self.average_box.show()
            self.label_3.show()
        else:
            self.factor.hide()
            self.factor_2.hide()
            self.factor_3.hide()
            self.label_30.hide()
            self.label_33.hide()
            self.noframes.hide()
            self.blurcheck.hide()
            self.radioButton.hide()
            self.backgroundcheck.hide()
            self.backgroundcheck_2.hide()
            self.peakcheck.hide()
            self.lsignal.hide()
            self.rsignal.hide()
            self.label.hide()
            self.label_2.hide()
            self.average_box.hide()
            self.label_3.hide()

    def btnlightspectrum_clicked(self):
        # first collect and stack frames
        # next decolorize
        # then rotate
        # then crop
        # then calibrate
        n = self.noframes.value()
        if self.camera_change.currentIndex() == 0:
            self.Responses.append('no camera chosen')
            return 'no camera chosen'
        else:
            camnumber = self.camera_change.currentIndex() - 1
            capture = cv2.VideoCapture(camnumber)
            userbrt = self.brightnessspin.value()
            usercont = self.contrastspin.value()
            usergain = self.gainspin.value()
            userexp = self.exposurespin.value()
            capture.set(cv.CV_CAP_PROP_BRIGHTNESS, userbrt)
            capture.set(cv.CV_CAP_PROP_CONTRAST, usercont)
            capture.set(cv.CV_CAP_PROP_GAIN, usergain)
            time.sleep(2)
            capture.set(cv.CV_CAP_PROP_EXPOSURE, userexp)
            time.sleep(1)
            cap = cv.CaptureFromCAM(int(camnumber))
            i = 0
            while i < int(n):
                img = cv.QueryFrame(cap)
                QtGui.qApp.processEvents()
                i = int(i) + 1
                self.btnlightspectrum.setText('capturing ' + str(int(100*i/n)) +  ' %')
                if not i == 1:
                    cv.SaveImage('lightimg' + str(i) + '.jpg', img)
                q = i
            else:
                print 'stacking frames'
                
            i = 1
            i1 = 'lightimg'+ str(int(i+1)) + '.jpg'
            while i < int(n-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                self.btnlightspectrum.setText('stacking ' + str(int(100*i/n)) +  ' %')
                alpha = 1/(1+i)
                i2 = 'lightimg'+ str(int(i+1)) + '.jpg'
                im1 = Image.open(i1)
                im2 = Image.open(i2)
                i3 = Image.blend(im1, im2, alpha)
                i1 = i3
                im1.save('lightintermediate.jpg')
                i1 = 'lightintermediate.jpg'
            else:
                print 'stacked'
            self.btnlightspectrum.setText('A bit more to go')
            i = 1
            while i <= (q-1):
                i = int(i)+1
                os.remove('lightimg' + str(i) + '.jpg')
            else:
                print 'frames deleted'
            lighttitle = str(self.absnameedit.text() + 'light')
            im=Image.open(i1) #turns it into a colorless image
            factor = float(self.factor.value())
            factor_2 = float(self.factor_2.value())
            factor_3 = float(self.factor_3.value())
            im.convert("L", (factor,factor_2,factor_3,0)).save("decolorized_" + str(lighttitle) + '.jpg', 'JPEG')
            im = Image.open("decolorized_" + str(lighttitle) + '.jpg')
            g = str(im.getextrema())
            print g
            chop = g.index(',')
            max = g[(int(chop)+2):(len(g)-1)]
            if int(max) == 255:
                d = cv2.imread("decolorized_" + str(lighttitle) + '.jpg')
                satpix = str(list(d)).count('255')
                print str(satpix) + ' number of sat pixels'
                w, h = im.size
                tpix = int(w)*int(h)
                print str(tpix) + ' total pixels'
                percsat = float(satpix)/float(tpix)
                self.Responses.append(str(percsat) + '% of pixels are saturated')
            self.Responses.append("saved as decolorized_" + str(lighttitle) + '.jpg, max pixel value out of 255 is ' + str(max) + '. If this is close to 255, the image may be saturated.')
            
            ry = self.rylivespin.value() # set the endpoints of the spectrum
            rx = self.rxlivespin.value()
            ly = self.lylivespin.value()
            lx = self.lxlivespin.value()
            height = ry-ly
            length = rx-lx
        
            mim = Image.open("decolorized_" + lighttitle + '.jpg')
        
#this does the rotation

            if height >= 0:
                if length >= 0:
                    theta = math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample = Image.BICUBIC).save("rotated_" + lighttitle + '.jpg')
                elif length <0:
                    length = -length
                    theta = 180-math.degrees(math.atan(float(height)/(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + lighttitle + '.jpg')
            elif height <0:
                height = -height
                if length >=0:
                    theta = 360-math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + lighttitle + '.jpg')
                elif length <0:
                    theta = 180+math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + lighttitle + '.jpg')
            else:
                self.Responses.append('something is wrong')
                quit()
        
            self.Responses.append('rotated spectrum saved as rotated_' + lighttitle)

            left = self.leftlivespin.value()
            right = self.rightlivespin.value()
            ceiling = self.ceilinglivespin.value()
            floor = self.floorlivespin.value()
            box = (left, ceiling, right, floor)

            cim = Image.open("rotated_" + lighttitle + '.jpg')
            """blur2 = cim.filter(PIL.ImageFilter.BLUR)  This section smoothes out the absorbance
            blur2.save('blurred2' + lighttitle + '.jpg')
            redun2 = Image.open('blurred2' + lighttitle + '.jpg')"""
            cim.crop(box).save('cropped' + lighttitle + '.jpg')
            webbrowser.open("cropped" + lighttitle + '.jpg')
            self.Responses.append('you should be able to see the spectrum clearly in this image')
            
# cropping is finished, begins binning by measuring dimensions of cropped file
            bim = Image.open("cropped" + lighttitle + '.jpg')
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
                rim = Image.open("cropped" + lighttitle + '.jpg')
                rim.crop(box).save("cropped_row" + str(int(i)) + lighttitle + '.jpg')
            else:
                self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row

            newlight = lighttitle + 'txt'
            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                i = int(i) + 1
                tim = Image.open("cropped_row" + str(int(i)) + lighttitle + '.jpg')
                retrieve = list(tim.getdata())
                write = open(newlight + str(int(i)) + '.txt', 'w')
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
                os.remove('cropped_row' + str(i) + lighttitle + '.jpg')
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

                cim = Image.open("rotated_" + str(lighttitle) + '.jpg')
                cim.crop(boxb).save('croppedb' + lighttitle + '.jpg')

                bim = Image.open("croppedb" + str(lighttitle) + '.jpg')
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
                    rim = Image.open("croppedb" + str(lighttitle) + '.jpg')
                    rim.crop(box).save("cropped_rowb" + str(int(i)) + str(lighttitle) + '.jpg')
                else:
                    self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row
        
                newlightb = str(lighttitle) + 'txtb'
                i = 0
                while i <= int(totalheight)-1:
                    i = int(i) + 1
                    tim = Image.open("cropped_rowb" + str(int(i)) + str(lighttitle) + '.jpg')
                    retrieve = list(tim.getdata())
                    write = open(newlightb + str(int(i)) + '.txt', 'w')
                    json.dump(retrieve, write)
                    write.close()
                    q = i
                else:
                    self.Responses.append('intensity data recorded')


                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('cropped_rowb' + str(i) + str(lighttitle) + '.jpg')
                else:
                    self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

                originalreadb = open(newlightb + '1.txt', 'r')
                originaltranscriptb = json.load(originalreadb)
                i = 0
                while i <= int(totalheight)-2:
                    i = int(i)+1
                    read = open(newlightb + str((int(i)+1)) + '.txt', 'r')
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
                    os.remove(newlightb + str(i) + '.txt')
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
            originalreadl = open(newlight + '1.txt', 'r')
            originaltranscriptl = json.load(originalreadl)
            i = 0
            while i <= int(totalheight)-2:
                QtGui.qApp.processEvents()
                i = int(i)+1
                readl = open(newlight + str((int(i)+1)) + '.txt', 'r')
                transcriptl = json.load(readl)
                originaltranscriptl = map(sum,zip(originaltranscriptl, transcriptl))
                readl.close()
            else:
                print 'rows added up'
            if self.backgroundcheck_2.isChecked():
                originaltranscriptl = map(sum,zip(originaltranscriptl,B))
            write = open('lightlist' + lighttitle + '.txt', 'w') # saves final list for light
            json.dump(originaltranscriptl, write)
            write.close()
# deletes the .txt files the intensity data was stored in
            i = 0
            originalreadl.close()
            while i <= (p-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove(newlight + str(i) + '.txt')
            else:
                print 'row intensity data  for light graph removed'
            self.btnlightspectrum.setText('Take light spectrum')
                
                
                
                
                
                
                
                
                
                
    def btnsamplespectrum_clicked(self):
        n = self.noframes.value()
        if self.camera_change.currentIndex() == 0:
            self.Responses.append('no camera chosen')
            return 'no camera chosen'
        else:
            camnumber = self.camera_change.currentIndex() - 1
            capture = cv2.VideoCapture(camnumber)
            userbrt = self.brightnessspin.value()
            usercont = self.contrastspin.value()
            usergain = self.gainspin.value()
            userexp = self.exposurespin.value()
            capture.set(cv.CV_CAP_PROP_BRIGHTNESS, userbrt)
            capture.set(cv.CV_CAP_PROP_CONTRAST, usercont)
            capture.set(cv.CV_CAP_PROP_GAIN, usergain)
            time.sleep(2)
            capture.set(cv.CV_CAP_PROP_EXPOSURE, userexp)
            time.sleep(1)
            cap = cv.CaptureFromCAM(int(camnumber))
            i = 0
            while i < int(n):
                img = cv.QueryFrame(cap)
                QtGui.qApp.processEvents()
                i = int(i) + 1
                self.btnsamplespectrum.setText('capturing ' + str(int(100*i/n)) +  ' %')
                if not i==1:
                    cv.SaveImage('sampleimg' + str(i) + '.jpg', img)
                q = i
            else:
                print 'stacking frames'
                
            i = 1
            i1 = 'sampleimg'+ str(int(i+1)) + '.jpg'
            while i < int(n-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                self.btnsamplespectrum.setText('stacking ' + str(int(100*i/n)) +  ' %')
                alpha = 1/(1+i)
                i2 = 'sampleimg'+ str(int(i+1)) + '.jpg'
                im1 = Image.open(i1)
                im2 = Image.open(i2)
                i3 = Image.blend(im1, im2, alpha)
                i1 = i3
                im1.save('sampleintermediate.jpg')
                i1 = 'sampleintermediate.jpg'
            else:
                print 'stacked'
            self.btnsamplespectrum.setText('A bit more to go')
            i = 1
            while i <= (q-1):
                i = int(i)+1
                os.remove('sampleimg' + str(i) + '.jpg')
            else:
                print 'frames deleted'
            sampletitle = str(self.absnameedit.text()+ 'sample')
            im=Image.open(i1) #turns it into a colorless image
            factor = float(self.factor.value())
            factor_2 = float(self.factor_2.value())
            factor_3 = float(self.factor_3.value())
            im.convert("L", (factor,factor_2,factor_3,0)).save("decolorized_" + str(sampletitle) + '.jpg', 'JPEG')
            im = Image.open("decolorized_" + str(sampletitle) + '.jpg')
            g = str(im.getextrema())
            print g
            chop = g.index(',')
            max = g[(int(chop)+2):(len(g)-1)]
            if int(max) == 255:
                d = cv2.imread("decolorized_" + str(sampletitle) + '.jpg')
                satpix = str(list(d)).count('255')
                print str(satpix) + ' number of sat pixels'
                w, h = im.size
                tpix = int(w)*int(h)
                print str(tpix) + ' total pixels'
                percsat = float(satpix)/float(tpix)
                self.Responses.append(str(percsat) + '% of pixels are saturated')
            self.Responses.append("saved as decolorized_" + str(sampletitle) + '.jpg, max pixel value out of 255 is ' + str(max) + '. If this is close to 255, the image may be saturated.')
            
            ry = self.rylivespin.value() # set the endpoints of the spectrum
            rx = self.rxlivespin.value()
            ly = self.lylivespin.value()
            lx = self.lxlivespin.value()
            height = ry-ly
            length = rx-lx
        
            mim = Image.open("decolorized_" + sampletitle + '.jpg')
        
#this does the rotation

            if height >= 0:
                if length >= 0:
                    theta = math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample = Image.BICUBIC).save("rotated_" + sampletitle + '.jpg')
                elif length <0:
                    length = -length
                    theta = 180-math.degrees(math.atan(float(height)/(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + sampletitle + '.jpg')
            elif height <0:
                height = -height
                if length >=0:
                    theta = 360-math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + sampletitle + '.jpg')
                elif length <0:
                    theta = 180+math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + sampletitle + '.jpg')
            else:
                self.Responses.append('something is wrong')
                quit()
        
            self.Responses.append('rotated spectrum saved as rotated_' + sampletitle)

            left = self.leftlivespin.value()
            right = self.rightlivespin.value()
            ceiling = self.ceilinglivespin.value()
            floor = self.floorlivespin.value()
            box = (left, ceiling, right, floor)

            cim = Image.open("rotated_" + sampletitle + '.jpg')
            """blur2 = cim.filter(PIL.ImageFilter.BLUR)
            blur2.save('blurred2' + sampletitle + '.jpg')
            redun2 = Image.open('blurred2' + sampletitle + '.jpg') Not necessary for the absorbance spectrum""" 
            cim.crop(box).save('cropped' + sampletitle + '.jpg')
            webbrowser.open("cropped" + sampletitle + '.jpg')
            self.Responses.append('you should be able to see the spectrum clearly in this image')
            
# cropping is finished, begins binning by measuring dimensions of cropped file
            bim = Image.open("cropped" + sampletitle + '.jpg')
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
                rim = Image.open("cropped" + sampletitle + '.jpg')
                rim.crop(box).save("cropped_row" + str(int(i)) + sampletitle + '.jpg')
            else:
                self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row

            newsample = sampletitle + 'txt'
            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                i = int(i) + 1
                tim = Image.open("cropped_row" + str(int(i)) + sampletitle + '.jpg')
                retrieve = list(tim.getdata())
                write = open(newsample + str(int(i)) + '.txt', 'w')
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
                os.remove('cropped_row' + str(i) + sampletitle + '.jpg')
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

                cim = Image.open("rotated_" + str(sampletitle) + '.jpg')
                cim.crop(boxb).save('croppedb' + sampletitle + '.jpg')

                bim = Image.open("croppedb" + str(sampletitle) + '.jpg')
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
                    rim = Image.open("croppedb" + str(sampletitle) + '.jpg')
                    rim.crop(box).save("cropped_rowb" + str(int(i)) + str(sampletitle) + '.jpg')
                else:
                    self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row
        
                newsampleb = str(sampletitle) + 'txtb'
                i = 0
                while i <= int(totalheight)-1:
                    i = int(i) + 1
                    tim = Image.open("cropped_rowb" + str(int(i)) + str(sampletitle) + '.jpg')
                    retrieve = list(tim.getdata())
                    write = open(newsampleb + str(int(i)) + '.txt', 'w')
                    json.dump(retrieve, write)
                    write.close()
                    q = i
                else:
                    self.Responses.append('intensity data recorded')


                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('cropped_rowb' + str(i) + str(sampletitle) + '.jpg')
                else:
                    self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

                originalreadb = open(newsampleb + '1.txt', 'r')
                originaltranscriptb = json.load(originalreadb)
                i = 0
                while i <= int(totalheight)-2:
                    i = int(i)+1
                    read = open(newsampleb + str((int(i)+1)) + '.txt', 'r')
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
                    os.remove(newsampleb + str(i) + '.txt')
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

            originalreads = open(newsample + '1.txt', 'r')
            originaltranscripts = json.load(originalreads)
            i = 0
            while i <= int(totalheight)-2:
                QtGui.qApp.processEvents()
                i = int(i)+1
                reads = open(newsample + str((int(i)+1)) + '.txt', 'r')
                transcripts = json.load(reads)
                originaltranscripts = map(sum,zip(originaltranscripts, transcripts))
                reads.close()
            else:
                print 'rows added up'
                
            if self.backgroundcheck_2.isChecked():
                originaltranscripts = map(sum,zip(originaltranscripts,B))
            else:
                print 'not subtracting sample background'
            write = open('samplelist' + sampletitle + '.txt', 'w') # saves final list for sample
            json.dump(originaltranscripts, write)
            write.close()
# deletes the .txt files the intensity data was stored in
            i = 0
            originalreads.close()
            while i <= (p-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove(newsample + str(i) + '.txt')
            else:
                print 'row intensity data  for light graph removed'
            self.btnsamplespectrum.setText('Take sample spectrum')
            self.Responses.append('To make peak corrections: Enter the lowest and highest wavelengths at which your light source has a good output')
            
    def btncalcabs_clicked(self):
        livetitle = self.livename.text()
        plt.close('all')
        sampletitle = str(self.absnameedit.text()+ 'sample')
        lighttitle = str(self.absnameedit.text() + 'light')
        name = str(self.absnameedit.text())
        readsamp = open('samplelist' + sampletitle + '.txt', 'r')
        transcriptsamp = json.load(readsamp)
        S = list()
        for item in transcriptsamp: # the sample needs to be negative, not the blank
            if math.copysign(1,item) == -1:
                S.append(0)
            elif item == 0:
                S.append(0)
            else:
                S.append(-(math.log10(item))) # requires negative values since we need a subtraction below (log subtraction = division)
        readlight = open('lightlist' + lighttitle + '.txt', 'r')
        transcriptlight = json.load(readlight)
        L = list() # moves log of positive values to new list
        for item in transcriptlight:
            if math.copysign(1,item) == -1: # if values are negative, it appends 0 instead of taking the log
                L.append(0)
            elif item == 0: # if they're 0 it does the same so math.log10 can deal with everything
                L.append(0)
            else:
                L.append(math.log10(item)) # takes log if the values are positive
        y = map(sum,zip(S, L)) # performs the subtraction equivalent to: LOG(I0/I) = LOG(I0) - LOG(I) - gives abs values

# this part turns X from pixels into nanometers
        bim = Image.open("cropped" + sampletitle + '.jpg')
        startarea = str(bim).index('size=')+5
        tail = str(bim)[startarea:]
        endoftail = tail.index('at')
        important = tail[:(endoftail-1)]
        endoflength = important.index('x')
        totallength = important[:endoflength]
        lp = self.lplivespin.value()
        lc = self.lclivespin.value()
        rp = self.rplivespin.value()
        rc = self.rclivespin.value()
        dp = rp-lp
        dc = rc-lc
        step = float(dc)/float(dp)
        xl = float(lc) - float(step)*float(lp)
        xr = float (rc) + float(step)*(float(totallength)-float(rp))
        x = np.arange(xl, xr, float(step)) # left bound, right bound, step size
        xlist = []
        for item in x:
            xlist.append(item)
        x = list() # makes x into a list
        for item in xlist:
            x.append(item)
        print str(len(x)) + ' entries for X'
        print str(len(y)) + ' entries for Y'
        while len(x) != len(y): # makes sure x and y are the same length
            if len(x) > len(y):
                x.pop()
                print str(len(x)) + ' entries for X'
                print str(len(y)) + ' entries for Y'
            elif len(y) > len(x):
                y.pop()
                print str(len(x)) + ' entries for X'
                print str(len(y)) + ' entries for Y'
            else:
                print 'x and y are the same size'
        if not self.peakcheck.isChecked():
            if self.average_check.isChecked():
                yaverager = y[:]
                q = self.average_box.value()
                yavg = np.convolve(yaverager, np.ones(int(q))/float(q), 'valid')
                difference = abs((len(yavg)-len(x))/2)
                print str(difference) + 'no peak correction, yes average, size of difference'
                ylist = []
                for item in yavg: # turn yavg into a list
                    ylist.append(item)
                yavg = list()
                for item in ylist:
                    yavg.append(item)
                n = 0
                while n<difference:
                    n = n+1
                    x.pop(0)
                    x.pop()
                print str(len(yavg))
                while len(x) != len(yavg):
                    if len(x) > len(yavg):
                        x.pop()
                        print str(len(x)) + ' entries for X'
                        print str(len(yavg)) + ' entries for Y'
                    elif len(yavg) > len(x):
                        yavg.pop()
                        print str(len(x)) + ' entries for X'
                        print str(len(yavg)) + ' entries for Y'
                    else:
                        print 'x and y are the same size'
        
                plt.close()
                plt.plot(x, yavg)
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('Absorption', color='k')
                plt.suptitle('Absoprtion Graph (adjusted)')
                plt.savefig(name + 'adjgraph.png', frameon=True)
                webbrowser.open(name + 'adjgraph.png')
            else: #not averaging, no peak corrections
                plt.plot(x, y)
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('Absorption', color='k')
                plt.suptitle('Absorption Graph')
                plt.savefig(name + 'graph.png', frameon=True)
                webbrowser.open(name + 'graph.png')
                if self.datacheck_2.isChecked():
                    np.savetxt(name + '_abs_data_unadjusted.csv', (x, y), delimiter = ',')
                    self.Responses.append('CSV saved as '+ str(name) + '_abs_data_unadjusted.csv')
        if self.peakcheck.isChecked(): # set bounds for x from user input, stop graphing outside of boundaries
            yclone = y[:]
            x2 = x[:]
            xclone = []
            for item in x2:
                xclone.append(item) # turns xclone into a list from an array
            xclone2 = xclone[:]
            xclone3 = xclone[:]
            ynew = list() 
            lengthofy = len(y)
            n = 0
            lsignal = self.lsignal.value()
            rsignal = self.rsignal.value()
            n = 0
            lowindex = int(0)
            highindex = int(1)
            for item in xclone:
                n = n+1
                if item < lsignal:
                    lowindex = n
                elif item > rsignal:
                    highindex = n
                    break
            print 'lower index = ' + str(int(lowindex))
            print 'upper index = ' + str(int(highindex))
            n = 0
            for item in xclone3:
                n = n+1
                if n < lowindex:
                    xclone2.pop(0)
                elif n > highindex:
                    xclone2.pop()
            n = 0
            for item in y:
                n = n+1
                if n < lowindex:
                    yclone.pop(0)
                elif n > highindex:
                    yclone.pop()
            while len(xclone2) != len(yclone):
                if len(xclone2) > len(yclone):
                    xclone2.pop()
                    print str(len(xclone2)) + ' entries for X'
                    print str(len(yclone)) + ' entries for Y'
                elif len(yclone) > len(xclone2):
                    yclone.pop()
                    print str(len(xclone2)) + ' entries for X'
                    print str(len(yclone)) + ' entries for Y'
                else:
                    print 'x and y are the same size'
            
            # Finished with adjustments, x and y are bounded by user input
            
            str(yclone) + 'corrected y final'
            plt.close('all')
            
            if self.average_check.isChecked(): # both averaging and peak corrections
                yaverager = yclone[:]
                q = self.average_box.value()
                yavg = np.convolve(yaverager, np.ones(int(q))/float(q), 'valid')
                difference = (len(xclone2)-len(yavg))/2
                print str(difference) + '= averaging and peak corrections, length of difference between x and y'
                ylist = []
                for item in yavg:
                    ylist.append(item)
                yavg = ylist # ensures yavg is a list
                n = 0
                while n < difference: # eliminates terms from beginning and end of x to make it the same length as y
                    n = n+1
                    xclone2.pop(0)
                    xclone2.pop()
                print str(len(yavg)) + '= length of yavg, avg and peak corrections'
                print str(len(xclone2)) + '= length of xclone2, avg and peak corrections'
                n = 0
                while len(xclone2) != len(yavg): # makes sure x and y are the same length
                    if len(xclone2) > len(yavg):
                        xclone2.pop()
                        print str(len(xclone2)) + ' entries for X'
                        print str(len(yavg)) + ' entries for Y'
                    elif len(yavg) > len(xclone2):
                        yavg.pop()
                        print str(len(xclone2)) + ' entries for X'
                        print str(len(yavg)) + ' entries for Y'
                    else:
                        print 'x and y are the same size'
                print str(len(yavg)) + ' corrected y final'
                print str(len(xclone2)) + ' length x'
                plt.plot(xclone2,yavg)
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('adjusted Absorption', color='k')
                plt.suptitle('Adjusted Absorption Graph')
                plt.savefig(name + 'adjustedgraph.png', frameon=True)
                webbrowser.open(name + 'adjustedgraph.png')
                if self.datacheck_2.isChecked():
                    np.savetxt(name + '_abs_data_averaged.csv', (xclone2, yavg), delimiter = ',')
                    self.Responses.append('CSV saved as '+ str(name) + '_abs_data_averaged.csv')
                    
            else:
                print str(len(yclone)) + ' corrected y final'
                print str(len(xclone2)) + ' len x'
                plt.plot(xclone2,yclone)
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('adjusted Absorption', color='k')
                plt.suptitle('Adjusted Absorption Graph')
                plt.savefig(name + 'adjustedgraph.png', frameon=True)
                webbrowser.open(name + 'adjustedgraph.png')
                if self.datacheck_2.isChecked():
                    np.savetxt(name + '_abs_data_adjusted.csv', (xclone2, yclone), delimiter = ',')
                    self.Responses.append('CSV saved as '+ str(name) + '_abs_data_adjusted.csv')

    
    def btnShowVideo_clicked(self):
        if self.camera_change.currentIndex() == 0:
            self.Responses.append('no camera chosen')
            return 'no camera chosen'
        else:
            camnumber = self.camera_change.currentIndex() - 1
            capture = cv2.VideoCapture(camnumber)
            brightness = capture.get(cv.CV_CAP_PROP_BRIGHTNESS)
            contrast = capture.get(cv.CV_CAP_PROP_CONTRAST)
            gain = capture.get(cv.CV_CAP_PROP_GAIN)
            exposure = capture.get(cv.CV_CAP_PROP_EXPOSURE)
            self.brightnessspin.setValue(brightness)
            self.contrastspin.setValue(contrast)
            self.gainspin.setValue(gain)
            self.exposurespin.setValue(exposure)
            cv.NamedWindow('camera ' + str(camnumber))
            cap = cv.CaptureFromCAM(int(camnumber))
            while self.camera_change.currentIndex >0:
                img = cv.QueryFrame(cap)
                cv.ShowImage('camera ' + str(camnumber), img)
                if cv.WaitKey(10) == 27:
                    break
                if self.camera_change.currentIndex == 0:
                    break
            else:
                print 'no more video wanted'
            cv.DestroyWindow('camera ' + str(camnumber))
            capture.release()
            
    def btntest_clicked(self):
        if self.camera_change.currentIndex() == 0:
            self.Responses.append('no camera chosen')
            return 'no camera chosen'
        else:
            self.Responses.append('Adjusting settings - this will take a few seconds.')
            self.Responses.append('Use the spacebar to adjust settings while the video is playing, or esc to stop the stream')
            camnumber = self.camera_change.currentIndex() - 1
            capture = cv2.VideoCapture(camnumber)
            userbrt = self.brightnessspin.value()
            usercont = self.contrastspin.value()
            usergain = self.gainspin.value()
            userexp = self.exposurespin.value()
            capture.set(cv.CV_CAP_PROP_BRIGHTNESS, userbrt)
            capture.set(cv.CV_CAP_PROP_CONTRAST, usercont)
            capture.set(cv.CV_CAP_PROP_GAIN, usergain)
            time.sleep(3)
            capture.set(cv.CV_CAP_PROP_EXPOSURE, userexp)
            cv.NamedWindow('camera ' + str(camnumber))
            cap = cv.CaptureFromCAM(int(camnumber))
            while self.camera_change.currentIndex >0:
                img = cv.QueryFrame(cap)
                cv.ShowImage('camera ' + str(camnumber), img)
                if cv.WaitKey(10) == 27:
                    break
                if self.camera_change.currentIndex == 0:
                    break
                if cv.WaitKey(10) == 32:
                    userbrt = self.brightnessspin.value()
                    usercont = self.contrastspin.value()
                    usergain = self.gainspin.value()
                    userexp = self.exposurespin.value()
                    capture.set(cv.CV_CAP_PROP_BRIGHTNESS, userbrt)
                    capture.set(cv.CV_CAP_PROP_CONTRAST, usercont)
                    capture.set(cv.CV_CAP_PROP_GAIN, usergain)
                    capture.set(cv.CV_CAP_PROP_EXPOSURE, userexp)
                    time.sleep(3)
            else:
                print 'no more video wanted'
            cv.DestroyWindow('camera ' + str(camnumber))
            capture.release()
            
    def btndeclive_clicked(self):
        if self.camera_change.currentIndex() == 0:
            self.Responses.append('no camera chosen')
            return 'no camera chosen'
        else:
            self.Responses.append('This will capture and stack some frames.  Type in the X and Y coordinates of both ends of the spectrum in the appropriate boxes to rotate the image after it appears')
            camnumber = self.camera_change.currentIndex() - 1
            capture = cv2.VideoCapture(camnumber)
            userbrt = self.brightnessspin.value()
            usercont = self.contrastspin.value()
            usergain = self.gainspin.value()
            userexp = self.exposurespin.value()
            capture.set(cv.CV_CAP_PROP_BRIGHTNESS, userbrt)
            capture.set(cv.CV_CAP_PROP_CONTRAST, usercont)
            capture.set(cv.CV_CAP_PROP_GAIN, usergain)
            time.sleep(2)
            capture.set(cv.CV_CAP_PROP_EXPOSURE, userexp)
            time.sleep(1)
            cap = cv.CaptureFromCAM(int(camnumber))
            
            """Should also work:
            cap = cv.CaptureFromCAM(int(camnumber))
            frame = cv.RetrieveFrame(cap)
            img = cv.CloneImage(frame)
            cv.SaveImage('liveimg' + str(i) + '.jpg', img)"""
            
            i = 0
            while i < 10:
                img = cv.QueryFrame(cap)
                QtGui.qApp.processEvents()
                i = int(i) + 1
                if not i ==1:
                    cv.SaveImage('liveimg' + str(i) + '.jpg', img)
                q = i
            else:
                print 'stacking frames'
                
            
                
            i = 1
            i1 = 'liveimg'+ str(int(i+1)) + '.jpg'
            while i < 9:
                QtGui.qApp.processEvents()
                i = int(i)+1
                alpha = 1/(1+i)
                i2 = 'liveimg'+ str(int(i+1)) + '.jpg'
                im1 = Image.open(i1)
                im2 = Image.open(i2)
                i3 = Image.blend(im1, im2, alpha)
                i1 = i3
                im1.save('liveintermediate.jpg')
                i1 = 'liveintermediate.jpg'
            else:
                print 'stacked'
                
            i = 1
            while i <= (q-1):
                i = int(i)+1
                os.remove('liveimg' + str(i) + '.jpg')
            else:
                print 'frames deleted'
            livetitle = self.livename.text()
            im=Image.open(i1) #turns the reference into a colorless image
            factor = float(self.factor.value())
            factor_2 = float(self.factor_2.value())
            factor_3 = float(self.factor_3.value())
            im.convert("L", (factor,factor_2,factor_3,0)).save("decolorized_" + str(livetitle) + '.jpg', 'JPEG')
            im = Image.open("decolorized_" + str(livetitle) + '.jpg')
            g = str(im.getextrema())
            print g
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
            self.Responses.append("saved as decolorized_" + str(livetitle) + '.jpg, max value out of 255 is ' + str(max))
            webbrowser.open("decolorized_" + str(livetitle) + '.jpg')
            
    def btnrotlive_clicked(self):
        livetitle = self.livename.text()
        ry = self.rylivespin.value() # set the endpoints of the spectrum
        rx = self.rxlivespin.value()
        ly = self.lylivespin.value()
        lx = self.lxlivespin.value()
        height = ry-ly
        length = rx-lx
        
        mim = Image.open("decolorized_" + str(livetitle) + '.jpg')
        
#this does the actual rotation

        if height >= 0:
            if length >= 0:
                theta = math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + str(livetitle) + '.jpg')
            elif length <0:
                length = -length
                theta = 180-math.degrees(math.atan(float(height)/(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + str(livetitle) + '.jpg')
        elif height <0:
            height = -height
            if length >=0:
                theta = 360-math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + str(livetitle) + '.jpg')
            elif length <0:
                theta = 180+math.degrees(math.atan(float(height)/float(length)))
                mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + str(livetitle) + '.jpg')
        else:
            self.Responses.append('something is wrong')
            quit()
        
        self.Responses.append('rotated spectrum saved as rotated_' + livetitle)

#this section displays the spectrum to ensure it is flat

        webbrowser.open("rotated_" + str(livetitle) + '.jpg')
        self.Responses.append('If this is flat, move on - otherwise, try again with different coordinates')
        self.Responses.append('enter the values of the rightmost, leftmost, highest and lowest pixels where appropriate')

# this part does the cropping and binning

    def btncroplive_clicked(self):
        livetitle = self.livename.text()

        left = self.leftlivespin.value()
        right = self.rightlivespin.value()
        ceiling = self.ceilinglivespin.value()
        floor = self.floorlivespin.value()
        box = (left, ceiling, right, floor)

        cim = Image.open("rotated_" + str(livetitle) + '.jpg')
        cim.crop(box).save("cropped" + str(livetitle) + '.jpg')
        self.Responses.append('image has been cropped, proceeding to binning')

# cropping is finished, begins binning by measuring dimensions of cropped file
        bim = Image.open("cropped" + str(livetitle) + '.jpg')
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
            rim = Image.open("cropped" + str(livetitle) + '.jpg')
            rim.crop(box).save("cropped_row" + str(int(i)) + str(livetitle) + '.jpg')
        else:
            self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row

        newlive = str(livetitle) + 'txt'
        i = 0
        while i <= int(totalheight)-1:
            i = int(i) + 1
            tim = Image.open("cropped_row" + str(int(i)) + str(livetitle) + '.jpg')
            retrieve = list(tim.getdata())
            write = open(newlive + str(int(i)) + '.txt', 'w')
            json.dump(retrieve, write)
            write.close()
            q = i
        else:
            self.Responses.append('intensity data recorded')


        i = 0
        while i <= (q-1):
            i = int(i)+1
            os.remove('cropped_row' + str(i) + str(livetitle) + '.jpg')
        else:
            self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

        originalread = open(newlive + '1.txt', 'r')
        originaltranscript = json.load(originalread)
        i = 0
        while i <= int(totalheight)-2:
            i = int(i)+1
            read = open(newlive + str((int(i)+1)) + '.txt', 'r')
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
            os.remove(newlive + str(i) + '.txt')
        else:
            print 'row intensity data  for reference removed'

# shows plot for reference spectrum
        plt.close('all')
        plt.figure(3)
        plt.plot(originaltranscript)
        plt.minorticks_on()
        plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
        plt.xlabel('Pixel number', color= 'k')
        plt.ylabel('Intensity (arb units)', color='k')
        plt.suptitle('Calibration Graph')
        plt.savefig(str(livetitle) + 'graph.png', frameon=True)
        webbrowser.open(str(livetitle) + 'graph.png')
        self.Responses.append('for calibration: enter the pixel and corresponding wavelength for two points on this graph.  Then move on to the fluorescence or absorption sections further to the right.')
        
    def btnaddgraph_clicked(self):
        # first collect and stack frames
        # next decolorize
        # then rotate
        # then crop
        # then calibrate
        n = self.noframes.value()
        if self.camera_change.currentIndex() == 0:
            self.Responses.append('no camera chosen')
            return 'no camera chosen'
        else:
            camnumber = self.camera_change.currentIndex() - 1
            capture = cv2.VideoCapture(camnumber)
            userbrt = self.brightnessspin.value()
            usercont = self.contrastspin.value()
            usergain = self.gainspin.value()
            userexp = self.exposurespin.value()
            capture.set(cv.CV_CAP_PROP_BRIGHTNESS, userbrt)
            capture.set(cv.CV_CAP_PROP_CONTRAST, usercont)
            capture.set(cv.CV_CAP_PROP_GAIN, usergain)
            time.sleep(2)
            capture.set(cv.CV_CAP_PROP_EXPOSURE, userexp)
            time.sleep(1)
            cap = cv.CaptureFromCAM(int(camnumber))
            i = 0
            while i < int(n):
                img = cv.QueryFrame(cap)
                QtGui.qApp.processEvents()
                i = int(i) + 1
                self.btnaddgraph.setText('capturing ' + str(int(100*i/n)) +  ' %')
                if not i == 1:
                    cv.SaveImage('graphimg' + str(i) + '.jpg', img)
                q = i
            else:
                print 'stacking frames'
                
            i = 1
            i1 = 'graphimg'+ str(int(i+1)) + '.jpg'
            while i < int(n-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                self.btnaddgraph.setText('stacking ' + str(int(100*i/n)) +  ' %')
                alpha = 1/(1+i)
                i2 = 'graphimg'+ str(int(i+1)) + '.jpg'
                im1 = Image.open(i1)
                im2 = Image.open(i2)
                i3 = Image.blend(im1, im2, alpha)
                i1 = i3
                im1.save('aliveintermediate.jpg')
                i1 = 'aliveintermediate.jpg'
            else:
                print 'stacked'
            self.btnaddgraph.setText('A bit more to go')
            i = 1
            while i <= (q-1):
                i = int(i)+1
                os.remove('graphimg' + str(i) + '.jpg')
            else:
                print 'frames deleted'
            livetitle = str(self.graphnameedit.text())
            im=Image.open(i1) #turns it into a colorless image
            factor = float(self.factor.value())
            factor_2 = float(self.factor_2.value())
            factor_3 = float(self.factor_3.value())
            im.convert("L", (factor,factor_2,factor_3,0)).save("decolorized_" + str(livetitle) + '.jpg', 'JPEG')
            im = Image.open("decolorized_" + str(livetitle) + '.jpg')
            g = str(im.getextrema())
            print g
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
            self.Responses.append("saved as decolorized_" + str(livetitle) + '.jpg, max pixel value out of 255 is ' + str(max) + '. If this is close to 255, the image may be saturated.')
            
            ry = self.rylivespin.value() # set the endpoints of the spectrum
            rx = self.rxlivespin.value()
            ly = self.lylivespin.value()
            lx = self.lxlivespin.value()
            height = ry-ly
            length = rx-lx
        
            mim = Image.open("decolorized_" + livetitle + '.jpg')
        
#this does the rotation

            if height >= 0:
                if length >= 0:
                    theta = math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample = Image.BICUBIC).save("rotated_" + livetitle + '.jpg')
                elif length <0:
                    length = -length
                    theta = 180-math.degrees(math.atan(float(height)/(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + livetitle + '.jpg')
            elif height <0:
                height = -height
                if length >=0:
                    theta = 360-math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + livetitle + '.jpg')
                elif length <0:
                    theta = 180+math.degrees(math.atan(float(height)/float(length)))
                    mim.rotate(theta, resample=Image.BICUBIC).save("rotated_" + livetitle + '.jpg')
            else:
                self.Responses.append('something is wrong')
                quit()
        
            self.Responses.append('rotated spectrum saved as rotated_' + livetitle)
#
#
# gets the background spectrum set up
            if self.backgroundcheck.isChecked():
                leftb = self.leftlivespin.value()
                rightb = self.rightlivespin.value()
                ceilingb = self.ceilinglivespin.value() - 20
                floorb = self.ceilinglivespin.value() - 10
                boxb = (leftb, ceilingb, rightb, floorb)

                cim = Image.open("rotated_" + str(livetitle) + '.jpg')
                cim.crop(boxb).save("croppedb" + str(livetitle) + '.jpg')

                bim = Image.open("croppedb" + str(livetitle) + '.jpg')
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
                    rim = Image.open("croppedb" + str(livetitle) + '.jpg')
                    rim.crop(box).save("cropped_rowb" + str(int(i)) + str(livetitle) + '.jpg')
                else:
                    self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row
        
                newlive = str(livetitle) + 'txtb'
                i = 0
                while i <= int(totalheight)-1:
                    i = int(i) + 1
                    tim = Image.open("cropped_rowb" + str(int(i)) + str(livetitle) + '.jpg')
                    retrieve = list(tim.getdata())
                    write = open(newlive + str(int(i)) + '.txt', 'w')
                    json.dump(retrieve, write)
                    write.close()
                    q = i
                else:
                    self.Responses.append('intensity data recorded')


                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('cropped_rowb' + str(i) + str(livetitle) + '.jpg')
                else:
                    self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

                originalreadb = open(newlive + '1.txt', 'r')
                originaltranscriptb = json.load(originalreadb)
                i = 0
                while i <= int(totalheight)-2:
                    i = int(i)+1
                    read = open(newlive + str((int(i)+1)) + '.txt', 'r')
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
                    os.remove(newlive + str(i) + '.txt')
                else:
                    print 'row intensity data  for reference removed'
                B = list()
                for item in originaltranscriptb:
                    B.append(-int(item))
            else:
                print 'skipping background subtraction'
#
#
# finishes with the background and moves onto the actual spectrum
            
            left = self.leftlivespin.value()
            right = self.rightlivespin.value()
            ceiling = self.ceilinglivespin.value()
            floor = self.floorlivespin.value()
            box = (left, ceiling, right, floor)

            cim = Image.open("rotated_" + livetitle + '.jpg')
            if self.blurcheck.isChecked():
                from PIL import ImageFilter
                blur2 = cim.filter(PIL.ImageFilter.BLUR)
                blur2.save('blurred2' + livetitle + '.jpg')
                redun2 = Image.open('blurred2' + livetitle + '.jpg')
                redun2.crop(box).save('cropped' + livetitle + '.jpg')
                print 'image blurred'
            else:
                cim.crop(box).save("cropped" + livetitle + '.jpg')
                print 'no blur'
            webbrowser.open("cropped" + livetitle + '.jpg')
            self.Responses.append('you should be able to see the spectrum clearly in this image')
            
# cropping is finished, begins binning by measuring dimensions of cropped file
            bim = Image.open("cropped" + livetitle + '.jpg')
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
                rim = Image.open("cropped" + livetitle + '.jpg')
                rim.crop(box).save("cropped_row" + str(int(i)) + livetitle + '.jpg')
            else:
                self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row

            newlive = livetitle + 'txt'
            i = 0
            while i <= int(totalheight)-1:
                QtGui.qApp.processEvents()
                i = int(i) + 1
                tim = Image.open("cropped_row" + str(int(i)) + livetitle + '.jpg')
                retrieve = list(tim.getdata())
                write = open(newlive + str(int(i)) + '.txt', 'w')
                json.dump(retrieve, write)
                write.close()
                q = i
            else:
                self.Responses.append('intensity data recorded')


            i = 0
            while i <= (q-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove('cropped_row' + str(i) + livetitle + '.jpg')
            else:
                self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows

            originalread = open(newlive + '1.txt', 'r')
            originaltranscript = json.load(originalread)
            i = 0
            while i <= int(totalheight)-2:
                QtGui.qApp.processEvents()
                i = int(i)+1
                read = open(newlive + str((int(i)+1)) + '.txt', 'r')
                transcript = json.load(read)
                try:
                    originaltranscript = map(sum,zip(originaltranscript, transcript))
                except TypeError:
                    self.Responses.append('Blur failed.  Starting over without blurring.')
                    print 'type error'
                    cv.WaitKey(10) == 32
                    cim = Image.open("rotated_" + livetitle + '.jpg')
                    left = self.leftlivespin.value()
                    right = self.rightlivespin.value()
                    ceiling = self.ceilinglivespin.value()
                    floor = self.floorlivespin.value()
                    box = (left, ceiling, right, floor)
                    cim.crop(box).save("cropped" + livetitle + '.jpg')
                    print 'no blur'
                    self.Responses.append('image has been cropped, proceeding to binning')

# cropping is finished, begins binning by measuring dimensions of cropped file ** repeated for type error
                    bim = Image.open("cropped" + livetitle + '.jpg')
                    startarea = str(bim).index('size=')+5
                    tail = str(bim)[startarea:]
                    endoftail = tail.index('at')
                    important = tail[:(endoftail-1)]
                    endoflength = important.index('x')
                    totallength = important[:endoflength]
                    totalheight = important[(endoflength+1):]
                    left = 0
                    right = int(totallength)

# splits the image into rows and saves them ** repeated for type error

                    i = 0
                    while i <= int(totalheight)-1:
                        QtGui.qApp.processEvents()
                        floor = 1 + int(i)
                        ceiling = int(floor) - 1
                        i = int(i)+1
                        box = (left, ceiling, int(right), floor)
                        rim = Image.open("cropped" + livetitle + '.jpg')
                        rim.crop(box).save("cropped_row" + str(int(i)) + livetitle + '.jpg')
                    else:
                        self.Responses.append('image has been split into rows')
            

# grabs intensity data from image and saves it to a new .txt for each row ** repeated for type error

                    newlive = livetitle + 'txt'
                    i = 0
                    while i <= int(totalheight)-1:
                        QtGui.qApp.processEvents()
                        i = int(i) + 1
                        tim = Image.open("cropped_row" + str(int(i)) + livetitle + '.jpg')
                        retrieve = list(tim.getdata())
                        write = open(newlive + str(int(i)) + '.txt', 'w')
                        json.dump(retrieve, write)
                        write.close()
                        q = i
                    else:
                        self.Responses.append('intensity data recorded')
    

                    i = 0
                    while i <= (q-1):
                        QtGui.qApp.processEvents()
                        i = int(i)+1
                        os.remove('cropped_row' + str(i) + livetitle + '.jpg')
                    else:
                        self.Responses.append('cropped row images removed')
    
# adds up intensity data for all rows ** repeated for type error

                    originalread = open(newlive + '1.txt', 'r')
                    originaltranscript = json.load(originalread)
                    i = 0
                read.close()
                
            else:
                print "rows have been summed"

# deletes the .txt files the intensity data was stored in for the reference ** type error stuff is finished
            if self.backgroundcheck.isChecked():
                originaltranscript = map(sum,zip(B,originaltranscript))
            else:
                print 'not subtracting background'
            i = 0
            originalread.close()
            while i <= (q-1):
                QtGui.qApp.processEvents()
                i = int(i)+1
                os.remove(newlive + str(i) + '.txt')
            else:
                print 'row intensity data  for live graph removed'
            
            plt.close('all')
            lp = self.lplivespin.value()
            lc = self.lclivespin.value()
            rp = self.rplivespin.value()
            rc = self.rclivespin.value()
            dp = rp-lp
            dc = rc-lc
            step = float(dc)/float(dp)
                
            y = originaltranscript
            xl = float(lc) - float(step)*float(lp)
            xr = float (rc) + float(step)*(float(totallength)-float(rp))
            x = np.arange(xl, xr, float(step))
            xclone = []
            for item in x:
                xclone.append(item)
            print str(len(xclone)) + ' entries for X'
            print str(len(y)) + ' entries for Y'
            while len(xclone) != len(y):
                if len(xclone) > len(y):
                    xclone.pop()
                    print str(len(xclone)) + ' entries for X'
                    print str(len(y)) + ' entries for Y'
                elif len(y) > len(xclone):
                    y.pop()
                    print str(len(xclone)) + ' entries for X'
                    print str(len(y)) + ' entries for Y'
                else:
                    print 'x and y are the same size'
            self.btnaddgraph.setText('Add live graph')

            plt.figure(4)
            try:
                plt.plot(xclone, y)
            except ValueError:
                self.Responses.append('cannot make plot.  Make minor adjustments to the calibration section and hit the space bar to try again')
                print 'value error'
                cv.WaitKey(0) == 32
            else:
                print 'no errors'
                if self.datacheck.isChecked():
                    np.savetxt(livetitle + 'data.csv', (xclone, y), delimiter = ',')
                    self.Responses.append('you can open ' + livetitle + 'data.csv in excel.  To make the formatting nicer, select all cells with entries, copy, and paste them using the transpose function.  Then under cell styles change number format to comma')
        
                plt.minorticks_on()
                plt.grid(which='both', axis='x', color = 'r', linestyle =':', linewidth=(.5))
                plt.xlabel('Wavelength /nm', color= 'k')
                plt.ylabel('Intensity (arb units)', color='k')
                plt.suptitle('Live Intensity Graph')
                plt.savefig(livetitle + 'graph.png', frameon=True)
                webbrowser.open(livetitle + 'graph.png')