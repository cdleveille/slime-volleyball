## Chris Leveille
## April 2019

import pygame
import math
from pygame import gfxdraw

class Player():

	# Create a new player
	def __init__(self, name, radius, speed, jump, color, inputs):
		self.x = 0
		self.y = 0
		self.xv = 0
		self.yv = 0
		self.color = color
		self.name = name
		self.radius = radius
		self.speed = speed
		self.jump = jump
		self.inputs = inputs
		self.jumpEnabled = True
		self.pupilOffsetRatio = self.radius / 14

	# Update movement properties based on the keys currently being pressed
	def getInput(self, keys):
		jump = self.inputs[0]
		left = self.inputs[1]
		right = self.inputs[2]

		if keys[left] and keys[right]:
			self.xv = 0
		elif keys[left]:
			self.xv = -self.speed
		elif keys[right]:
			self.xv = self.speed
		else:
			self.xv = 0
		if (self.jumpEnabled == True):
			if keys[jump]:
				self.yv = -self.jump
				self.jumpEnabled = False

	def getPupilOffset(self, ball, pupilX):
		(pupilShiftX, pupilShiftY) = (0, 0)
		XDiff = -(ball.x - (self.x + pupilX))
		YDiff = -(ball.y - (self.y - self.radius / 2))
		if XDiff > 0:
			if YDiff > 0:
				Angle = math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif XDiff < 0:
			if YDiff > 0:
				Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif XDiff == 0:
			if YDiff > 0:
				Angle = -90
			else:
				Angle = 90
			pupilShiftX = self.pupilOffsetRatio * math.cos(math.radians(Angle))
			pupilShiftY = self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif YDiff == 0:
			if XDiff < 0:
				Angle = 0
			else:
				Angle = 180
			pupilShiftX = self.pupilOffsetRatio * math.cos(math.radians(Angle))
			pupilShiftY = self.pupilOffsetRatio * math.sin(math.radians(Angle))
		return (pupilShiftX, pupilShiftY)

	# Update position properties based on a given gravity value
	def updatePosition(self, gravity):
		self.yv += gravity
		self.x += self.xv
		self.y += self.yv

	def draw(self, gameWin, backgroundColor, ball):
		self.drawAACircle(gameWin, int(self.x), int(self.y), int(self.radius), self.color)

		if (ball.y + ball.radius < pygame.display.get_surface().get_height()):
			eyeRadius = self.radius / 5
		else:
			eyeRadius = self.radius / 3.8

		if self.x < pygame.display.get_surface().get_width() / 2:
			(pupilOffsetX, pupilOffsetY) = self.getPupilOffset(ball, self.radius * 0.4)
		else:
			(pupilOffsetX, pupilOffsetY) = self.getPupilOffset(ball, -self.radius * 0.4)

		if (self.x < pygame.display.get_surface().get_width() / 2):
			self.drawAACircle(gameWin, int(self.x + self.radius * 0.4), int(self.y - self.radius / 2), int(eyeRadius), pygame.color.Color("lightgray"))
			self.drawAACircle(gameWin, int(self.x + self.radius * 0.4 + pupilOffsetX), int(self.y - self.radius / 2 + pupilOffsetY), int(self.radius / 8), pygame.color.Color("black"))
		else:
			self.drawAACircle(gameWin, int(self.x - self.radius * 0.4), int(self.y - self.radius / 2), int(eyeRadius), pygame.color.Color("lightgray"))
			self.drawAACircle(gameWin, int(self.x - self.radius * 0.4 + pupilOffsetX), int(self.y - self.radius / 2 + pupilOffsetY), int(self.radius / 8), pygame.color.Color("black"))

		pygame.draw.rect(gameWin, backgroundColor, (self.x - self.radius, self.y, self.radius * 2 + 1, self.radius + 1))

	# Draw a circle with smooth edges using anti-aliasing
	def drawAACircle(self, gameWin, x, y, r, color):
		pygame.gfxdraw.aacircle(gameWin, int(x), int(y), int(r), color)
		pygame.gfxdraw.filled_circle(gameWin, int(x), int(y), int(r), color)