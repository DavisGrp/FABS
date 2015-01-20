FABS
Version 1.0
Updated 1/20
------------------------------
FABS is free software designed to help run the absorption and fluorescence spectrometers, designed by the Davis group at Cornell. 
The author can be contacted via email at nal58@cornell.edu.
-----------------------------
Copyright 2015 Cornell University and the Cornell University Research Foundation, Inc.  All rights reserved.
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or(at your option) any later version.  This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for 
more details.  You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.
-----------------------------
Installation and Use
An installer for FABS is available on SourceForge.net/projects/fabs.  FABS runs on Windows 7, and the source code (written in Python 2.7) is distributed along with 
the program.  To run the software, open the shortcut in the FABS-1.0 folder or run the executable file in the FABS folder as an administrator.  
FABS is capable of taking fluorescence or absorption spectra from live webcam video, saved videos on your computer, or saved images.  Simply follow the 
on-screen instructions during each step.  FABS will work best if Microsoft Paint is your default image viewing program. Some troubleshooting advice follows.

In general, be sure not to move the spectrometer between runs.  This will throw off your calibration.  If you hit the ‘Cleanup’ button on the main window, 
all your images and graphs will be deleted from the FABS folder.  Due to the nature of absorbance spectra, the graph you end up with may be spiky 
in areas with low signal levels.  

USING LIVE VIDEO
If the camera is not giving useful video, adjust the parameters (brightness, contrast, gain, exposure) and test the video to apply them to the camera.  
You may need click test twice.
If your spectrum is too dark, you won’t get any useful data.  To solve this problem, make the exposure more negative and increase the gain.
If the spectrum does not look continuous (it looks like blobs of uniform red, green and blue), you may not get useful data.  This is indicative of 
problems with the camera parameters.
Poor signal to noise ratios can be improved by increasing the number of frames averaged.

USING SAVED VIDEOS
FlAbS may not be able to handle all video formats.  If you are having problems, try converting your videos to .mp4 or .mpeg files.
Long videos will take a long time to process, since FlAbS combines every single frame into a single image.  You can cut off the processing and only use a 
section of the video using the drop down menu above the instructions box.
Fluorescence spectra require only two videos; one of a highly structured spectrum (the calibration spectrum), and one of the 
fluorescent solution as it is fluorescing (the sample spectrum).  For absorbance measurements, the sample spectrum will be of the cuvette with 
some absorbing dye in it, and you will also need a spectrum of the cuvette filled with solvent.

USING IMAGES
Be aware that spectra from single images will have poor signal to noise ratios compared to those in videos.
Do not include the extensions when you are typing in the image names.
