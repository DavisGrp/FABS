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
import FluorImage
Videowindowpath = os.path.abspath("UI_Files/VideoProcessing.ui")
form_class = uic.loadUiType(str(Videowindowpath))[0]


class MyVideoClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnrefvid.clicked.connect(self.btnrefvid_clicked) #  process your spectra
        self.btnspecvid.clicked.connect(self.btnspecvid_clicked)
        self.btnlightvid.clicked.connect(self.btnlightvid_clicked)
        
    def btnrefvid_clicked(self):
        refgrabcancelled = False
        refgrabcut = False
        refgrabsave = False
        refgrabstop = False
        refstackcancelled = False
        refstackcut = False
        refstacksave = False
        refstackstop = False
        refvid = str(self.Refvidedit.text())
        cap = cv2.VideoCapture(str(refvid))
        currentframe = 0
        i = 0
        numframes = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
        while(cap.isOpened()):
            while currentframe <= numframes and refgrabcancelled == False:
                QtGui.qApp.processEvents()
                self.btnrefvid.setText(str(int(100*i/numframes)) +  ' % done')
                currentframe = int(currentframe) + 1
                i = int(i)+1
                Ocap = cv2.cv.CaptureFromFile(str(refvid))
                refstill = cv2.cv.QueryFrame(Ocap)
                cv2.cv.SaveImage('refstill'+ str(i) + '.jpg', refstill)
                q = i
                if self.stopper.currentIndex() == 1:
                    refgrabcancelled = True
                    refgrabcut = True
                    self.stopper.setCurrentIndex(0)
                    break
                if self.stopper.currentIndex() == 2:
                    refgrabcancelled = True
                    refgrabstop = True
                    self.stopper.setCurrentIndex(0)
                    break
                if self.stopper.currentIndex() == 3:
                    refgrabcancelled = True
                    refgrabsave = True
                    self.stopper.setCurrentIndex(0)
                    break
            else:
                break
        else:
            print 'done'
        self.btnrefvid.setText('Process reference')
        if refgrabcancelled:
            self.Responses.append('Frame capture stopped')
        else:
            self.Responses.append('reference video has been decomposed into frames')
        if refgrabstop:
            self.Responses.append('deleting frames') # should NOT stack frames - just delete them
            i = 0
            while i <= (q-1):
                i = int(i)+1
                os.remove('refstill' + str(i) + '.jpg')
            else:
                self.Responses.append('done')
                return 'deleted'
        elif refgrabcut:
            self.Responses.append('stacking frames') # should stack frames
            numframes = q - 1
        elif refgrabsave:
            self.Responses.append('frames saved') # should not delete or stack frames
            return 'saved'
        else:
            self.Responses.append('stacking frames')
        cap.release()
    
# stacks images for the reference and cutoff reference
        i = 0
        i1 = 'refstill'+ str(int(i+1)) + '.jpg'
        while i <= (numframes - 1) and refstackcancelled == False:
            QtGui.qApp.processEvents()
            self.btnrefvid.setText(str(int(100*i/numframes)) +  ' % done')
            i = int(i)+1
            alpha = 1/(1+i)
            i2 = 'refstill'+ str(int(i+1)) + '.jpg'
            im1 = Image.open(i1)
            im2 = Image.open(i2)
            i3 = Image.blend(im1, im2, alpha)
            i1 = i3
            im1.save('intermediate.jpg')
            i1 = 'intermediate.jpg'
            l = i # gives the number of the last frame the loop makes it through as l
# this is the escape part 
            if self.stopper.currentIndex() == 1:
                refstackcancelled = True
                refstackcut = True
                self.stopper.setCurrentIndex(0)
                break
            if self.stopper.currentIndex() == 2:
                refstackcancelled = True
                refstackstop = True
                self.stopper.setCurrentIndex(0)
                break
            if self.stopper.currentIndex() == 3:
                refstackcancelled = True
                refstacksave = True
                self.stopper.setCurrentIndex(0)
                break
        else:
            print 'frames stacked'
        self.btnrefvid.setText('Process reference')
        refname = str(self.Refnameedit.text())
        if refstackcancelled:
            self.Responses.append('Frame stacking stopped')
        else:
            self.Responses.append('reference frames have been stacked')
        if refstackcut: # same as refstacksave - just saves whatever has already been stacked
            self.Responses.append('desired reference frames have been stacked')
        if refstacksave: 
            self.Responses.append('desired reference frames have been stacked')
        if refstackstop:
            self.Responses.append('all images deleted')
            i = 0
            os.remove(i1)
            while i <= (q-1):
                i = int(i)+1
                os.remove('refstill' + str(i) + '.jpg')
            else:
                return 'deleted'
        im1 = Image.open(i1)
        im1.save(str(refname) + '.jpg')
        
# deletes all frames for ref
        i = 0
        while i <= (q-1):
            i = int(i)+1
            os.remove('refstill' + str(i) + '.jpg')
        else:
            self.Responses.append('reference frames removed, and spectrum saved as ' + str(refname) + '.jpg')
        self.Responses.append('ENTER VIDEO OF SPECTRUM AND CLICK BUTTON TO PROCEED')
        
    def btnlightvid_clicked(self):
            lightgrabcancelled = False
            lightgrabcut = False
            lightgrabsave = False
            lightgrabstop = False
            lightstackcancelled = False
            lightstackcut = False
            lightstacksave = False
            lightstackstop = False
            lightvid = str(self.Lightvidedit.text())
            cap = cv2.VideoCapture(str(refvid))
            currentframe = 0
            i = 0
            numframes = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            while(cap.isOpened()):
                while currentframe <= numframes and lightgrabcancelled == False:
                    QtGui.qApp.processEvents()
                    self.btnlightvid.setText(str(int(100*i/numframes)) +  ' % done')
                    currentframe = int(currentframe) + 1
                    i = int(i)+1
                    Ocap = cv2.cv.CaptureFromFile(str(refvid))
                    lightstill = cv2.cv.QueryFrame(Ocap)
                    cv2.cv.SaveImage('refstill'+ str(i) + '.jpg', lightstill)
                    q = i
                    if self.stopper.currentIndex() == 1:
                        lightgrabcancelled = True
                        lightgrabcut = True
                        self.stopper.setCurrentIndex(0)
                        break
                    if self.stopper.currentIndex() == 2:
                        lightgrabcancelled = True
                        lightgrabstop = True
                        self.stopper.setCurrentIndex(0)
                        break
                    if self.stopper.currentIndex() == 3:
                        lightgrabcancelled = True
                        lightgrabsave = True
                        self.stopper.setCurrentIndex(0)
                        break
                else:
                    break
            else:
                print 'done'
            self.btnlightvid.setText('Process light spectrum')
            if lightgrabcancelled:
                self.Responses.append('Frame capture stopped')
            else:
                self.Responses.append('light spectrum has been decomposed into frames')
            if lightgrabstop:
                self.Responses.append('deleting frames') # should NOT stack frames - just delete them
                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('refstill' + str(i) + '.jpg')
                else:
                    self.Responses.append('done')
                    return 'deleted'
            elif lightgrabcut:
                self.Responses.append('stacking frames') # should stack frames
                numframes = q - 1
            elif lightgrabsave:
                self.Responses.append('frames saved') # should not delete or stack frames
                return 'saved'
            else:
                self.Responses.append('stacking frames')
            cap.release()
        
# stacks images for the light spectrum, plus the cutoff part
            i = 0
            i1 = 'refstill'+ str(int(i+1)) + '.jpg'
            while i <= (numframes - 1) and lightstackcancelled == False:
                QtGui.qApp.processEvents()
                self.btnlightvid.setText(str(int(100*i/numframes)) +  ' % done')
                i = int(i)+1
                alpha = 1/(1+i)
                i2 = 'refstill'+ str(int(i+1)) + '.jpg'
                im1 = Image.open(i1)
                im2 = Image.open(i2)
                i3 = Image.blend(im1, im2, alpha)
                i1 = i3
                im1.save('intermediate.jpg')
                i1 = 'intermediate.jpg'
                l = i # gives the number of the last frame the loop makes it through as l
    # this is the escape part 
                if self.stopper.currentIndex() == 1:
                    lightstackcancelled = True
                    lightstackcut = True
                    self.stopper.setCurrentIndex(0)
                    break
                if self.stopper.currentIndex() == 2:
                    lightstackcancelled = True
                    lightstackstop = True
                    self.stopper.setCurrentIndex(0)
                    break
                if self.stopper.currentIndex() == 3:
                    lightstackcancelled = True
                    lightstacksave = True
                    self.stopper.setCurrentIndex(0)
                    break
            else:
                print 'frames stacked'
            self.btnlightvid.setText('Process light spectrum')
            lightname = str(self.Lightnameedit.text())
            if lightstackcancelled:
                self.Responses.append('Frame stacking stopped')
            else:
                self.Responses.append('light frames have been stacked')
            if lightstackcut: # same as lightstacksave - just saves whatever has already been stacked
                self.Responses.append('desired light frames have been stacked')
            if lightstacksave: 
                self.Responses.append('desired light frames have been stacked')
            if lightstackstop:
                self.Responses.append('all images deleted')
                i = 0
                os.remove(i1)
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('refstill' + str(i) + '.jpg')
                else:
                    return 'deleted'
            im1 = Image.open(i1)
            im1.save(str(refname) + '.jpg')
        
# deletes all frames for light
            i = 0
            while i <= (q-1):
                i = int(i)+1
                os.remove('refstill' + str(i) + '.jpg')
            else:
                self.Responses.append('light frames removed, and spectrum saved as ' + str(refname) + '.jpg')
# breaks sample video into frames

    def btnspecvid_clicked(self):
            sgrabcancelled = False
            sgrabcut = False
            sgrabsave = False
            sgrabstop = False
            sstackcancelled = False
            sstackcut = False
            sstacksave = False
            sstackstop = False
            sampvid = str(self.SpecvidEdit.text())
            cap = cv2.VideoCapture(str(sampvid))
            currentframe = 0
            i = 0
            numframes = cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            while(cap.isOpened()):
                while currentframe <= numframes and sgrabcancelled == False:
                    QtGui.qApp.processEvents()
                    self.btnspecvid.setText(str(int(100*i/numframes)) +  ' % done')
                    currentframe = int(currentframe) + 1
                    i = int(i)+1
                    Ocap = cv2.cv.CaptureFromFile(str(sampvid))
                    sampstill = cv2.cv.QueryFrame(Ocap)
                    cv2.cv.SaveImage('sampstill'+ str(i) + '.jpg', sampstill)
                    q = i
                    if self.stopper.currentIndex() == 1:
                        sgrabcancelled = True
                        sgrabcut = True
                        self.stopper.setCurrentIndex(0)
                        break
                    if self.stopper.currentIndex() == 2:
                        sgrabcancelled = True
                        sgrabstop = True
                        self.stopper.setCurrentIndex(0)
                        break
                    if self.stopper.currentIndex() == 3:
                        sgrabcancelled = True
                        sgrabsave = True
                        self.stopper.setCurrentIndex(0)
                        break
                else:
                    break
            else:
                print 'done'
            self.btnspecvid.setText('Process Spectrum')
            if sgrabcancelled:
                self.Responses.append('Frame capture stopped')
            else:
                self.Responses.append('sample video has been decomposed into frames')
            if sgrabstop:
                self.Responses.append('deleting frames') # should NOT stack frames - just delete them
                i = 0
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('sampstill' + str(i) + '.jpg')
                else:
                    self.Responses.append('done')
                    return 'deleted'
            elif sgrabcut:
                self.Responses.append('stacking frames') # should stack frames
                numframes = q - 1
            elif sgrabsave:
                self.Responses.append('frames saved') # should not delete or stack frames
                return 'saved'
            else:
                self.Responses.append('stacking frames')
            self.stopper.setCurrentIndex(0)
            cap.release()

# stacks frames for the sample
        
            i = 0
            i1 = 'sampstill'+ str(int(i+1)) + '.jpg'
            while i <= (numframes - 1) and sstackcancelled == False:
                QtGui.qApp.processEvents()
                self.btnspecvid.setText(str(int(100*i/numframes)) +  ' % done')
                i = int(i)+1
                alpha = 1/(1+i)
                i2 = 'sampstill'+ str(int(i+1)) + '.jpg'
                im1 = Image.open(i1)
                im2 = Image.open(i2)
                i3 = Image.blend(im1, im2, alpha)
                i1 = i3
                im1.save('sintermediate.jpg')
                i1 = 'sintermediate.jpg'
                l = i # gives the number of the last frame the loop makes it through as l
    # this is the escape part 
                if self.stopper.currentIndex() == 1:
                    sstackcancelled = True
                    sstackcut = True
                    self.stopper.setCurrentIndex(0)
                    break
                if self.stopper.currentIndex() == 2:
                    sstackcancelled = True
                    sstackstop = True
                    self.stopper.setCurrentIndex(0)
                    break
                if self.stopper.currentIndex() == 3:
                    sstackcancelled = True
                    sstacksave = True
                    self.stopper.setCurrentIndex(0)
                    break
            else:
                print 'done'
            self.btnspecvid.setText('Process Spectrum')
            spectrumname = str(self.Specnameedit.text())
            if sstackcancelled:
                self.Responses.append('Frame stacking stopped')
            else:
                self.Responses.append('sample frames have been stacked')
            if sstackcut: # same as sstacksave - just saves whatever has already been stacked
                self.Responses.append('desired sample frames have been stacked')
            if sstacksave: 
                self.Responses.append('desired sample frames have been stacked')
            if sstackstop:
                self.Responses.append('all images deleted')
                i = 0
                os.remove(i1)
                while i <= (q-1):
                    i = int(i)+1
                    os.remove('sampstill' + str(i) + '.jpg')
                else:
                    return 'deleted'
            im1 = Image.open(i1)
            im1.save(str(spectrumname) + '.jpg')
        
# deletes all frames for sample
        
            i = 0
            while i <= (q-1):
                i = int(i)+1
                os.remove('sampstill' + str(i) + '.jpg')
            else:
                self.Responses.append('sample frames removed, and spectrum saved as ' + str(spectrumname) + '.jpg')
            self.Responses.append('MOVE ON TO NEXT SECTION')