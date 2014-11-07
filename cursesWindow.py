#  encoding=latin-1
import random

class Eye:
	current = [0 for x in xrange(8)]
	pupilX = 4
	pupilY = 4

	def __init__(self):
		self.update()

	def setPupil(self, x,y):
		self.pupilX = max(0, min(7, x))
		self.pupilY = max(0, min(7, y))
		self.update()
	
	def movePupil(self, x,y):
		self.pupilX = (self.pupilX + x + 8) % 8
		self.pupilY = (self.pupilY + y + 8) % 8
		self.update()

	def update(self):
		global openEye, pupilByX
		self.current = list(openEye)
		if self.pupilY == 0:
			self.current[0] = self.current[0] & pupilByX[self.pupilX]
			self.current[7] = self.current[7] & pupilByX[self.pupilX]
		else:
			self.current[self.pupilY-1] = self.current[self.pupilY-1] & pupilByX[self.pupilX]
			self.current[self.pupilY] = self.current[self.pupilY] & pupilByX[self.pupilX]


openEye = [
0b00111100,
0b01111110,
0b11111111,
0b11111111,
0b11111111,
0b11111111,
0b01111110,
0b00111100,
]
pupilByX = [
0b01111110,
0b00111111,
0b10011111,
0b11001111,
0b11100111,
0b11110011,
0b11111001,
0b11111100,
]

leftEye = Eye()
rightEye = Eye()

window = 0
centerX = 0
centerY = 0

def curses(win):
	from curses import use_default_colors, napms, curs_set

	use_default_colors()
	win.border()
	curs_set(0)

	global window, centerX, centerY
	
	row, col = win.getmaxyx()
	centerX = int(col / 2)
	centerY = int(row / 2)
	window = win
	while True:
		drawEyes()

		leftEye.movePupil(1,0)#random.randint(-1,1),random.randint(-1,1))
		rightEye.movePupil(0,1)#random.randint(-1,1),random.randint(-1,1))

		napms(500)

def drawEyes():
	global window, centerX, centerY, leftEye, rightEye
	for x in range(8):
		for y in range(8):
			#left eye
			val = (leftEye.current[y] & 1 << 7-x) != 0
			window.addstr(centerY+y-4, centerX+x-10, '8' if val else ' ')
			#right eye
			val = (rightEye.current[y] & 1 << 7-x) != 0
			window.addstr(centerY+y-4, centerX+x+2, '8' if val else ' ')
	window.refresh()



if __name__ == "__main__":
	from curses import wrapper
	wrapper(curses)