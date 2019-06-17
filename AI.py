## Chris Leveille
## April 2019

import math

class AI():

	def __init__(self):
		a = 1

	## Predict the horizontal position of the ball when it contacts the floor
	def predictBallLandingPosition(self, game):

		ball = game.ball
		r = game.ball.radius
		x = game.ball.x
		y = game.ball.y
		xv = game.ball.xv
		yv = game.ball.yv
		g = game.gravity
		bounce = game.bounceCoefficient
		gameWidth = game.winWidth

		

		return 0