## Chris Leveille
## April 2019

import pygame

class Ball():

	# Create a new ball
	def __init__(self, radius, color):
		self.x = 0
		self.y = 0
		self.xv = 0
		self.yv = 0
		self.color = color
		self.radius = radius

	# Update position properties based on a given gravity value
	def updatePosition(self, gravity):
		self.yv += gravity

		if self.yv > 15:
			self.yv = 15
		if self.xv > 15:
			self.xv = 15

		self.x += self.xv
		self.y += self.yv

	# Draw the ball
	def draw(self, gameWin):
		self.drawAACircle(gameWin, int(self.x), int(self.y), int(self.radius), self.color)

		# If the ball is off-screen, draw a dot indicating its horizontal location
		if self.y - self.radius < -450:
			#self.drawAACircle(gameWin, int(self.x), 10, 4, self.color)
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 4, pygame.color.Color("black"))
		elif self.y - self.radius < -350:
			#self.drawAACircle(gameWin, int(self.x), 10, 5, self.color)
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 5, pygame.color.Color("black"))
		elif self.y - self.radius < -250:
			#self.drawAACircle(gameWin, int(self.x), 10, 6, self.color)
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 6, pygame.color.Color("black"))
		elif self.y - self.radius < -150:
			#self.drawAACircle(gameWin, int(self.x), 10, 7, self.color)
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 7, pygame.color.Color("black"))
		elif self.y - self.radius < -50:
			#self.drawAACircle(gameWin, int(self.x), 10, 8, self.color)
			pygame.gfxdraw.aacircle(gameWin, int(self.x), 10, 8, pygame.color.Color("black"))

	# Draw a circle with smooth edges using anti-aliasing
	def drawAACircle(self, gameWin, x, y, r, color):
		pygame.gfxdraw.filled_circle(gameWin, int(x), int(y), int(r), color)
		pygame.gfxdraw.aacircle(gameWin, int(x), int(y), int(r), pygame.color.Color("black"))