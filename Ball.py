## Chris Leveille
## April 2019

import pygame, pygame.gfxdraw

class Ball():

	## Create new ball
	def __init__(self, radius, color):
		
		self.x = 0
		self.y = 0
		self.xv = 0
		self.yv = 0
		self.maxV = 15
		self.color = color
		self.radius = radius

	## Update the ball's position
	def updatePosition(self, gravity):
		
		self.yv += gravity

		# Enforce the ball's maximum speed
		if abs(self.xv) > self.maxV:
			self.xv = self.maxV * (self.xv / abs(self.xv))
		if abs(self.yv) > self.maxV:
			self.yv = self.maxV * (self.yv / abs(self.yv))

		self.x += self.xv
		self.y += self.yv

	## Draw the ball
	def draw(self, gameWin):
		
		pygame.gfxdraw.filled_circle(gameWin, int(self.x), int(self.y), int(self.radius), self.color)
		pygame.gfxdraw.aacircle(gameWin, int(self.x), int(self.y), int(self.radius), pygame.color.Color("black"))
		self.drawXInd(gameWin)

	# If the ball is off-screen, draw a marker indicating its horizontal location
	def drawXInd (self, gameWin):
		
		if self.y - self.radius < -450:
			radius =  4
		elif self.y - self.radius < -350:
			radius =  5
		elif self.y - self.radius < -250:
			radius =  6
		elif self.y - self.radius < -150:
			radius =  7
		elif self.y - self.radius < -50:
			radius =  8
		else:
			radius = 0

		if radius > 0:
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, radius, pygame.color.Color("black"))
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, radius - 1, pygame.color.Color("black"))