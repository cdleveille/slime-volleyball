## Chris Leveille
## April 2019

import pygame

class Ball():

	## Create a new ball
	def __init__(self, radius, color):
		
		self.x = 0
		self.y = 0
		self.xv = 0
		self.yv = 0
		self.color = color
		self.radius = radius

	## Update position properties given a gravity value
	def updatePosition(self, gravity):
		
		self.yv += gravity
		self.x += self.xv
		self.y += self.yv

	## Draw the ball
	def draw(self, gameWin):
		
		pygame.gfxdraw.filled_circle(gameWin, int(self.x), int(self.y), int(self.radius), self.color)
		pygame.gfxdraw.aacircle(gameWin, int(self.x), int(self.y), int(self.radius), pygame.color.Color("black"))

		# If the ball is off-screen, draw a dot indicating its horizontal location
		if self.y - self.radius < -450:
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 4, pygame.color.Color("black"))
		elif self.y - self.radius < -350:
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 5, pygame.color.Color("black"))
		elif self.y - self.radius < -250:
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 6, pygame.color.Color("black"))
		elif self.y - self.radius < -150:
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 7, pygame.color.Color("black"))
		elif self.y - self.radius < -50:
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 8, pygame.color.Color("black"))