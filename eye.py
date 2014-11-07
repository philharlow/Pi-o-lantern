#  encoding=latin-1
import random

class Eye:
	current = [0 for x in xrange(8)]
	pupilX = 4
	pupilY = 4
	blinkStep = 0
	blinkWait = random.randint(20,100)

	def __init__(self):
		self.update()
		self.blinkWait = random.randint(20,100)

	def setPupilSmoothed(self, x,y):
		smooth = 4.
		self.pupilX += (x-self.pupilX)/smooth
		self.pupilY += (y-self.pupilY)/smooth
		self.setPupil(self.pupilX, self.pupilY)

	def setPupil(self, x,y):
		self.pupilX = max(0, min(6, x))
		self.pupilY = max(0, min(6, y))
		#self.update()
	
	def movePupil(self, x,y):
		self.pupilX = (self.pupilX + x + 7.) % 7.
		self.pupilY = (self.pupilY + y + 7.) % 7.
		#self.update()

	def update(self):
		self.current = list(self.blankEye[self.blinkStep])
		self.current[int(self.pupilY)] = self.current[int(self.pupilY)] & self.pupilByX[int(self.pupilX)]
		self.current[int(self.pupilY+1)] = self.current[int(self.pupilY+1)] & self.pupilByX[int(self.pupilX)]
		self.blinkWait -= 1
		if self.blinkWait <= 0:
			self.blinkStep += 1
			if self.blinkStep == 8:
				self.blinkWait = random.randint(20,100)
				self.blinkStep = 0

	blankEye = [
	[
	0b00111100,
	0b01111110,
	0b11111111,
	0b11111111,
	0b11111111,
	0b11111111,
	0b01111110,
	0b00111100,
	],
	[
	0b00000000,
	0b01111110,
	0b11111111,
	0b11111111,
	0b11111111,
	0b11111111,
	0b01111110,
	0b00000000,
	],
	[
	0b00000000,
	0b00000000,
	0b11111111,
	0b11111111,
	0b11111111,
	0b11111111,
	0b00000000,
	0b00000000,
	],
	[
	0b00000000,
	0b00000000,
	0b00000000,
	0b11111111,
	0b11111111,
	0b00000000,
	0b00000000,
	0b00000000,
	],
	[
	0b00000000,
	0b00000000,
	0b00000000,
	0b00000000,
	0b00000000,
	0b00000000,
	0b00000000,
	0b00000000,
	],
	[
	0b00000000,
	0b00000000,
	0b00000000,
	0b11111111,
	0b11111111,
	0b00000000,
	0b00000000,
	0b00000000,
	],
	[
	0b00000000,
	0b00000000,
	0b11111111,
	0b11111111,
	0b11111111,
	0b11111111,
	0b00000000,
	0b00000000,
	],
	[
	0b00000000,
	0b01111110,
	0b11111111,
	0b11111111,
	0b11111111,
	0b11111111,
	0b01111110,
	0b00000000,
	],
	]
	
	pupilByX = [
	0b00111111,
	0b10011111,
	0b11001111,
	0b11100111,
	0b11110011,
	0b11111001,
	0b11111100,
]