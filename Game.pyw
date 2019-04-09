## Chris Leveille
## April 2019

import pygame
import math
import random
from pygame import gfxdraw
from Player import Player
from Ball import Ball

class Game:

	# Create a new Game
	def __init__(self, winWidth, winHeight, backgroundColor, backgroundImage, frameTimeMS, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
					playerToBallMomentumTransfer, playerToBallHorizontalBoost, netHeight, netWidth, netColor, team1, team2, ball):
		self.winWidth = winWidth
		self.winHeight = winHeight
		self.gameWin = pygame.display.set_mode((winWidth, winHeight))
		self.backgroundColor = backgroundColor
		self.backgroundImage = backgroundImage
		self.frameTimeMS = frameTimeMS
		self.gravity = gravity
		self.bounceCoefficient = bounceCoefficient
		self.bounceCoefficientPlayer = bounceCoefficientPlayer
		self.bounceCoefficientNet = bounceCoefficientNet
		self.playerToBallMomentumTransfer = playerToBallMomentumTransfer
		self.playerToBallHorizontalBoost = playerToBallHorizontalBoost
		self.netHeight = netHeight
		self.netWidth = netWidth
		self.netColor = netColor
		self.team1 = team1
		self.team2 = team2
		self.ball = ball

	def startGame(self):
		self.team1Score = 0
		self.team2Score = 0
		self.scoreFont = scoreFont = pygame.font.Font(None, 48)
		self.messageFont = pygame.font.Font(None, 42)
		self.subMessageFont = pygame.font.Font(None, 24)
		self.messageColor = pygame.color.Color("black")
		self.message = "Game On!"
		self.subMessage = "May the slimiest Slime win."
		self.frameCount = 0

		rng = bool(random.getrandbits(1))
		if rng == True:
			self.teamToServe = self.team1
		else:
			self.teamToServe = self.team2

		self.resetPositions()
		self.gameLoop()

	def gameLoop(self):
		gameOn = True
		messageTimeoutFrameCount = (1000 / self.frameTimeMS) * 3

		while (gameOn == True):

			# Quit game if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOn = False

			# Hide the game messages after 3 sec
			if self.frameCount >= messageTimeoutFrameCount:
				self.message = ""
				self.subMessage = ""
				players = self.team1 + self.team2
				for i, player in enumerate(players):
					players[i].message = ""

			self.getInputFromPlayers()

			self.updatePositionOfGameObjects()

			self.keepPlayersInBounds()

			self.handleCollisions()

			self.draw()

			if self.frameCount < messageTimeoutFrameCount:
				self.frameCount += 1

	# Return each game object to its original position
	def resetPositions(self):
		for i, player in enumerate(self.team1):
			self.team1[i].x = ((self.winWidth / 2) / (len(self.team1) + 1)) * (i + 1)
			self.team1[i].y = self.winHeight

		for i, player in enumerate(self.team2):
			self.team2[i].x = (((self.winWidth / 2) / (len(self.team2) + 1)) * (i + 1)) + (self.winWidth / 2)
			self.team2[i].y = self.winHeight

		index = random.randint(0, len(self.teamToServe) - 1)
		for i, player in enumerate(self.teamToServe):
			if i == index:
				self.ball.x = player.x
		self.ball.y = self.winHeight * (1 / 3)
		self.ball.xv = 0
		self.ball.yv = 0

	def getInputFromPlayers(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.resetPositions()
		for player in self.team1 + self.team2:
			player.handleInput(keys)

	def updatePositionOfGameObjects(self):
		for player in self.team1 + self.team2:
			if player.y < self.winHeight:
				player.updatePosition(self.gravity)
			else:
				player.updatePosition(0)
		self.ball.updatePosition(self.gravity)

	def keepPlayersInBounds(self):
		for i, player in enumerate(self.team1):
			if player.x - player.radius < 1:
				self.team1[i].x = player.radius
			elif player.x + player.radius > self.winWidth / 2 - self.netWidth / 2 - 1:
				self.team1[i].x = self.winWidth / 2 - self.netWidth / 2 - player.radius - 1
			if player.y > self.winHeight:
				self.team1[i].y = self.winHeight
				self.team1[i].jumpEnabled = True

		for i, player in enumerate(self.team2):
			if player.x - player.radius < self.winWidth / 2 + self.netWidth / 2 + 1:
				self.team2[i].x = self.winWidth / 2 + self.netWidth / 2 + player.radius + 1
			elif player.x + player.radius > self.winWidth - 1:
				self.team2[i].x = self.winWidth - player.radius - 1
			if player.y > self.winHeight:
				self.team2[i].y = self.winHeight
				self.team2[i].jumpEnabled = True

	def handleCollisions(self):
		# Ball contacts floor
		if self.ball.y > self.winHeight - self.ball.radius:
			self.ball.y = self.winHeight - self.ball.radius
			self.ball.yv = -self.ball.yv * self.bounceCoefficient
			if self.ball.x > self.winWidth / 2:
				self.teamToServe = self.team1
				self.team1Score += 1
				self.message = self.getTeamScoreMessage(self.team1)
			else:
				self.teamToServe = self.team2
				self.team2Score += 1
				self.message = self.getTeamScoreMessage(self.team2)

			self.draw()
			pygame.time.delay(500)
			self.resetPositions()
			self.frameCount = 0

		# Ball contacts wall
		if self.ball.x - self.ball.radius < 1:
			self.ball.x = self.ball.radius
			self.ball.xv = -self.ball.xv * self.bounceCoefficient
		elif self.ball.x + self.ball.radius > self.winWidth:
			self.ball.x = self.winWidth - self.ball.radius
			self.ball.xv = -self.ball.xv * self.bounceCoefficient

		# Ball contacts Player
		for player in self.team1 + self.team2:
			if ballContactsCircle(self.ball.x, self.ball.y, self.ball.radius, player.x, player.y, player.radius) == True:
				(self.ball.xv, self.ball.yv) = getBallCircleVelocityVector(self.ball.x, self.ball.y, self.ball.xv, self.ball.yv, player.x, 
					player.y, player.xv, player.yv, self.bounceCoefficientPlayer, self.playerToBallMomentumTransfer, self.playerToBallHorizontalBoost)
				break

		# Ball contacts net
		if ballContactsCircle(self.ball.x, self.ball.y, self.ball.radius, self.winWidth /2, self.winHeight - self.netHeight + (self.netWidth / 2), self.netWidth / 2) == True:
				(self.ball.xv, self.ball.yv) = getBallCircleVelocityVector(self.ball.x, self.ball.y, self.ball.xv, self.ball.yv, self.winWidth / 2, 
					self.winHeight - self.netHeight + (self.netWidth / 2), 0, 0, self.bounceCoefficientNet, 0, 1)
		elif self.ball.y > self.winHeight - self.netHeight + self.netWidth:
			if abs((self.winWidth / 2) - (self.ball.x + self.ball.radius)) <= self.netWidth / 2:
				self.ball.x = (self.winWidth / 2) - (self.netWidth / 2) - self.ball.radius
				self.ball.xv = -self.ball.xv * self.bounceCoefficientNet
			elif abs((self.ball.x - self.ball.radius) - (self.winWidth / 2)) <= self.netWidth / 2:
				self.ball.x = (self.winWidth / 2) + (self.netWidth / 2) + self.ball.radius
				self.ball.xv = -self.ball.xv * self.bounceCoefficientNet

	def draw(self):
		# Control framerate
		pygame.time.delay(self.frameTimeMS)

		# Fill window with background color
		self.gameWin.fill(self.backgroundColor)

		# Draw messages
		messageLabel = self.messageFont.render(self.message, True, self.messageColor)
		messageLabelRect = messageLabel.get_rect(center = (self.winWidth / 2, 20))
		self.gameWin.blit(messageLabel, messageLabelRect)
		subMessageLabel = self.subMessageFont.render(self.subMessage, True, self.messageColor)
		subMessageLabelRect = subMessageLabel.get_rect(center = (self.winWidth / 2, 50))
		self.gameWin.blit(subMessageLabel, subMessageLabelRect)

		# Draw scores
		team1ScoreLabel = self.scoreFont.render(str(self.team1Score), True, self.messageColor)
		self.gameWin.blit(team1ScoreLabel, (30, 5))
		team2ScoreLabel = self.scoreFont.render(str(self.team2Score), True, self.messageColor)
		self.gameWin.blit(team2ScoreLabel, (self.winWidth - 60, 5))

		# Draw net
		pygame.draw.rect(self.gameWin, self.netColor, (self.winWidth / 2 - (self.netWidth / 2), self.winHeight - self.netHeight + (self.netWidth / 2), self.netWidth + 1, self.netHeight))
		drawAACircle(self.gameWin, int(self.winWidth / 2), int(self.winHeight - self.netHeight + (self.netWidth / 2)), int(self.netWidth / 2), self.netColor)

		# Draw players
		for player in self.team1 + self.team2:
			player.draw(self.gameWin, self.backgroundColor, self.ball)

		# Draw ball
		self.ball.draw(self.gameWin)

		# Refresh graphics
		pygame.display.update()

	def getTeamScoreMessage(self, team):
		if len(team) == 1:
			return team[0].name + " Scores!"
		else:
			return "Team Scores!"

def ballContactsCircle(x, y, ballRadius, c_x, c_y, circleRadius):
	if math.sqrt( ((x - c_x) ** 2) + ((y - c_y) ** 2) ) <= (ballRadius + circleRadius):
		return True
	return False

def getBallCircleVelocityVector(x, y, x_v, y_v, c_x, c_y, c_xv, c_yv, bounceCoefficient, playerToBallMomentumTransfer, playerToBallHorizontalBoost):
	ballSpeed = math.sqrt((x_v ** 2) + (y_v ** 2))
	XDiff = -(x - c_x)
	YDiff = -(y - c_y)
	if XDiff > 0:
		if YDiff > 0:
			Angle = math.degrees(math.atan(YDiff / XDiff))
			XSpeed = -ballSpeed * math.cos(math.radians(Angle))
			YSpeed = -ballSpeed * math.sin(math.radians(Angle))
		elif YDiff < 0:
			Angle = math.degrees(math.atan(YDiff / XDiff))
			XSpeed = -ballSpeed * math.cos(math.radians(Angle))
			YSpeed = -ballSpeed * math.sin(math.radians(Angle))
	elif XDiff < 0:
		if YDiff > 0:
			Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
			XSpeed = -ballSpeed * math.cos(math.radians(Angle))
			YSpeed = -ballSpeed * math.sin(math.radians(Angle))
		elif YDiff < 0:
			Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
			XSpeed = -ballSpeed * math.cos(math.radians(Angle))
			YSpeed = -ballSpeed * math.sin(math.radians(Angle))
	elif XDiff == 0:
		if YDiff > 0:
			Angle = -90
		else:
			Angle = 90
		XSpeed = ballSpeed * math.cos(math.radians(Angle))
		YSpeed = ballSpeed * math.sin(math.radians(Angle))
	elif YDiff == 0:
		if XDiff < 0:
			Angle = 0
		else:
			Angle = 180
		XSpeed = ballSpeed * math.cos(math.radians(Angle))
		YSpeed = ballSpeed * math.sin(math.radians(Angle))
	x_v = (XSpeed + (c_xv * playerToBallMomentumTransfer)) * bounceCoefficient  * playerToBallHorizontalBoost
	y_v = (YSpeed + (c_yv * playerToBallMomentumTransfer)) * bounceCoefficient
	return (x_v, y_v)

# The loser of the point must be shamed. This function makes that happen.
def getInsultMessage(loser, insultsUsedAlready):
	insults =	[	" got REKT right there.", ", turn your f*cking brain on.", " brought dishonor to his family.",
					", how do you like them apples?", ", u mad bro?", " must be rattled after that.", " continues to suck some serious ass.",
					", wow, not even close.", ", I'm not mad, I'm just disappointed. In you. For that.",
					" is playing like a little bitch.", " is simply an embarassment.", " is garbage. Complete and utter garbage",
					".isScrub() == True", " just managed to look like a complete idiot.", " is trash. Plain and simple.",
					", try not to suck so much all the time", " f*cked up and he knows it."
				]

	if len(insultsUsedAlready) >= len(insults):
		insultsUsedAlready.clear()

	insult = insults[random.randint(0, len(insults) - 1)]
	while (insult in insultsUsedAlready):
		insult = insults[random.randint(0, len(insults) - 1)]
	insultsUsedAlready.append(insult)
	return loser + insult

# Draw a circle with smooth edges using anti-aliasing
def drawAACircle(gameWin, x, y, r, color):
	pygame.gfxdraw.aacircle(gameWin, int(x), int(y), int(r), color)
	pygame.gfxdraw.filled_circle(gameWin, int(x), int(y), int(r), color)

def playGame():
	winWidth = 1000
	winHeight = 500
	backgroundColor = pygame.color.Color("lightblue")
	backgroundImage = None
	frameTimeMS = 7
	gravity = 0.1
	bounceCoefficient = 0.98
	bounceCoefficientPlayer = 0.98
	bounceCoefficientNet = 0.75
	playerToBallMomentumTransfer = 0.12
	playerToBallHorizontalBoost = 1.03
	netHeight = 100
	netWidth = 20
	netColor = pygame.color.Color("black")
	fourPlayer = False

	playerSpeed = 5
	playerJump = 5
	playerRadius = 50
	ballRadius = 25

	if playerRadius == ballRadius * 2:
		playerRadius += 1

	p1 = Player("Blue Slime", playerRadius, playerSpeed, playerJump, pygame.color.Color("darkblue"), [pygame.K_w, pygame.K_a, pygame.K_d], "[W, A, D]")
	p2 = Player("Red Slime", playerRadius, playerSpeed, playerJump, pygame.color.Color("darkred"), [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT], "[UP, LEFT, RIGHT]")
	p3 = Player("Purple Slime", playerRadius, playerSpeed, playerJump, pygame.color.Color("purple"), [pygame.K_t, pygame.K_f, pygame.K_h], "[T, F, H]")
	p4 = Player("Orange Slime", playerRadius, playerSpeed, playerJump, pygame.color.Color("orange"), [pygame.K_i, pygame.K_j, pygame.K_l], "[I, J, L]")

	# 1v1
	team1 = [p1] # controls: [W, A, D]
	team2 = [p2] # controls: [UP, LEFT, RIGHT]

	# 2v2
	if fourPlayer == True:
		team1.append(p3) # controls: [T, F, H]
		team2.append(p4) # controls: [I, J, L]

	ball = Ball(ballRadius, pygame.color.Color("darkgreen"))

	game = Game(winWidth, winHeight, backgroundColor, backgroundImage, frameTimeMS, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
				playerToBallMomentumTransfer, playerToBallHorizontalBoost, netHeight, netWidth, netColor, team1, team2, ball)
	game.startGame()

pygame.init()
playGame()