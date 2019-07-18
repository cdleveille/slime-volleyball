## Chris & Michael Leveille
## June 2019

import math

class AI():

	def __init__(self):
		a = 0

	## Predict the horizontal position of the ball when it contacts the floor
	def predictBallLandingPosition(self, game):

		r = game.ball.radius
		x = game.ball.x
		y = game.ball.y
		xv = game.ball.xv
		yv = game.ball.yv
		g = game.gravity
		gameWidth = game.winWidth
		gameHeight = game.winHeight

		# frames: number of frames elapsed during ball's flight
		frames1 = (-yv + (yv**2 - 2 * g * (y - gameHeight + r))**0.5) / g
		frames2 = (-yv - (yv**2 - 2 * g * (y - gameHeight + r))**0.5) / g
		frames = max(frames1, frames2)

		# d: total horizontal distance traveled by ball during flight (pixels), disregarding walls
		d = xv * frames

		# x_intercept: final x-position of ball when it lands, disregarding walls
		x_intercept = x + d

		# ball will not hit a wall
		if x_intercept + r < gameWidth and x_intercept - r > 0:
			x_final = x_intercept
		# ball will hit at least one wall
		else:
			if xv > 0:
				x_final = gameWidth - (x_intercept - gameWidth) - 2 * r
			else:
				x_final = 2 * r - x_intercept

		return int(x_final)