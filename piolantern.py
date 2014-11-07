#  encoding=latin-1
import random
import cv2
import os
import io
import picamera
import time
import numpy
import threading
from eye import Eye

import MAX7219array as m7219
from MAX7219fonts import CP437_FONT, SINCLAIRS_FONT, LCD_FONT, TINY_FONT
from MAX7219array import DIR_L, DIR_R, DIR_U, DIR_D
from MAX7219array import DIR_LU, DIR_RU, DIR_LD, DIR_RD
from MAX7219array import DISSOLVE, GFX_ON, GFX_OFF, GFX_INVERT

# Initialise the LED array
m7219.init()
#m7219.brightness(0)


leftEye = Eye()
rightEye = Eye()

window = 0
centerX = 0
centerY = 0

cameraWidth = 160# * 2
cameraHeight = 120# * 2


def processImage(t0, t1, t2):
	d1 = cv2.absdiff(t1, t0)
	d2 = cv2.absdiff(t2, t0)
	image = cv2.bitwise_and(d1, d2)
	image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	image = cv2.blur(image, (5,5))
	value, image = cv2.threshold(image, 25, 255, cv2.THRESH_BINARY)
	
	#element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
	#image = cv2.erode(image, element)

	image = cv2.blur(image, (5,5))
	#image = cv2.normalize(image, 0., 1.)
	
	#mean, stddev = cv2.meanStdDev(image)
	#if stddev[0] > 40:
	#	return image

	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)
	
	global cameraWidth, cameraHeight, x11
	xDiv = (cameraWidth+1) / 7.
	yDiv = (cameraHeight+1) / 7.
	if maxVal > 100:
		if x11:
			image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
			cv2.rectangle(image, (maxLoc[0]-10,maxLoc[1]-10), (maxLoc[0]+20,maxLoc[1]+20), (0,0,255), 1)
		#print xLoc, yLoc
		global leftEye, rightEye
		leftEye.setPupilSmoothed(maxLoc[0] / xDiv, maxLoc[1] / yDiv)
		rightEye.setPupilSmoothed(maxLoc[0] / xDiv, maxLoc[1] / yDiv)

	return image

camera = 0
x11 = False

def getcvImage():
	global camera
	stream = io.BytesIO()
	camera.capture(stream, format='jpeg', use_video_port=True)
	data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
	image = cv2.imdecode(data, 1)
	#image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	return image


def main(win):
	from curses import use_default_colors, napms, curs_set

	print "Starting up"

	use_default_colors()
	win.border()
	curs_set(0)

	global window, centerX, centerY, cameraWidth, cameraHeight, camera, x11
	
	row, col = win.getmaxyx()
	centerX = int(col / 2)
	centerY = int(row / 2)
	window = win
	windowName = "Test"
	
	try:
		os.environ['DISPLAY']
		x11 = True
	except:
		print "No display mode"
	
	if x11:
		cv2.namedWindow(windowName)
		cv2.moveWindow(windowName, 100, 100)
	
	with picamera.PiCamera() as camera:
		camera.resolution = (cameraWidth, cameraHeight)
		camera.led = x11
		camera.hflip = True
		camera.exposure_mode = "night"
		
		current = getcvImage()
		prev1 = getcvImage()
		prev2 = getcvImage()
		
		try:
			while cv2.waitKey(10) == -1:
				image = processImage(current, prev1, prev2)
				if x11:
					cv2.imshow(windowName, image)
				
				prev2 = prev1
				prev1 = current
				current = getcvImage()
	
				drawEyes()
		except Exception:
			pass

	if x11:
		cv2.destroyWindow(windowName)
	
	print "Done"

def drawEyes():
	global window, centerX, centerY, leftEye, rightEye, x11
	if x11:
		for x in range(8):
			for y in range(8):
				#left eye
				val = (leftEye.current[y] & 1 << 7-x) != 0
				window.addstr(centerY+y-4, centerX+x-10, '8' if val else ' ')
				#right eye
				val = (rightEye.current[y] & 1 << 7-x) != 0
				window.addstr(centerY+y-4, centerX+x+2, '8' if val else ' ')
		window.refresh()

	leftEye.update()
	rightEye.update()

	for y in range(8):
		m7219.send_matrix_reg_byte(0, y+1, leftEye.current[y])
		m7219.send_matrix_reg_byte(1, y+1, rightEye.current[y])



if __name__ == "__main__":
	from curses import wrapper
	wrapper(main)
