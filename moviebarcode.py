#!/usr/bin/env python

# Compresses a movie into a single image.
# Author: Sascha Hagedorn
 
import cv, sys, math, os, time

imgWidth = 1280
imgHeight = imgWidth * 10 / 16
barWidth = 1

frame = 0
x = 0

files = sys.argv[1:]

start = time.time()

for f in files:
	capture = cv.CaptureFromFile(f)
	frames = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)
	step = math.floor(frames / imgWidth)
	moviebarcode = cv.CreateImage((imgWidth, imgHeight), 8, 3)
		
	while(x < imgWidth):
		frameImg = cv.QueryFrame(capture)
		
		if frame % step == 0:
			bar = cv.CreateImage( (barWidth, imgHeight), 8, 3 )
			
			cv.Smooth(frameImg, frameImg, cv.CV_GAUSSIAN, 25)
			
			cv.Resize( frameImg, bar )	
			
			cv.SetImageROI( moviebarcode, (x, 0, barWidth, moviebarcode.height) )
			cv.SetImageROI( bar, (0, 0, barWidth, bar.height) )
			
			cv.Add( moviebarcode, bar, moviebarcode, None)
			
			cv.ResetImageROI(moviebarcode)
			cv.ResetImageROI(bar)
			x += 1
		frame += 1
		
	cv.SaveImage(os.path.basename(f) + ".jpg", moviebarcode)	
	print "Moviebarcode done in %.2f minutes" % ((time.time() - start) / 60.0)
