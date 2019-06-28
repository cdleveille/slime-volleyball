## Chris Leveille
## April 2019

import pygame, pygame.gfxdraw, math, random
from sys import platform
from AI import AI
if platform == "win32":
	from xinput import *

class Game:

	## Create new game
	def __init__(self, scoreLimit, winWidth, winHeight, backgroundColor, backgroundImage, framerate, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
					playerToBallMomentumTransfer, playerToBallHorizontalBoost, insultsEnabled, netHeight, netWidth, netColor, team1, team2, ball):
		
		self.scoreLimit = scoreLimit
		self.winWidth = winWidth
		self.winHeight = winHeight
		self.backgroundColor = backgroundColor
		self.backgroundImage = backgroundImage
		self.framerate = framerate
		self.gravity = gravity
		self.bounceCoefficient = bounceCoefficient
		self.bounceCoefficientPlayer = bounceCoefficientPlayer
		self.bounceCoefficientNet = bounceCoefficientNet
		self.playerToBallMomentumTransfer = playerToBallMomentumTransfer
		self.playerToBallHorizontalBoost = playerToBallHorizontalBoost
		self.insultsEnabled = insultsEnabled
		self.netHeight = netHeight
		self.netWidth = netWidth
		self.netColor = netColor
		self.team1 = team1
		self.team2 = team2
		self.ball = ball
		pygame.display.set_icon(pygame.image.load('assets/slime.ico'))
		pygame.display.set_caption("Slime Volleyball")
		self.gameWin = pygame.display.set_mode((self.winWidth, self.winHeight))

	## Start the game
	def startGame(self, firstRun):

		self.team1Score = 0
		self.team2Score = 0
		self.scoreFont = scoreFont = pygame.font.Font(None, 52)
		self.messageFont = pygame.font.Font(None, 42)
		self.subMessageFont = pygame.font.Font(None, 24)
		self.messageColor = pygame.color.Color("black")
		self.message = "GAME ON"
		self.subMessage = "First to " + str(self.scoreLimit) + " points wins!"
		self.playerMessageFlashRate = self.framerate / 2
		self.playerMessageFlashFrameMarker = 0
		self.drawPlayerMessage = False
		self.playerPowerBarOutlineFlashRate = self.framerate / 4
		self.playerPowerBarOutlineFrameMarker = 0
		self.drawPlayerPowerBarOutline = True
		self.insultsUsedAlready = []
		self.frameCount = 0
		self.gameOver = False
		self.AI = AI()

		if bool(random.getrandbits(1)) == True:
			self.teamToServe = self.team1
		else:
			self.teamToServe = self.team2

		self.resetPositions()
		self.resetPlayerPowers()

		if firstRun == True:
			self.gameLoop()

	## Main game logic executed each frame
	def gameLoop(self):
		
		gameOn = True
		messageTimeoutFrameCount = self.framerate * 4
		clock = pygame.time.Clock()

		while (gameOn == True):

			self.hideMessagesOnTimeout(messageTimeoutFrameCount)

			self.checkForXInputDevices()

			gameOn = self.getInputFromPlayers()

			self.updatePositionOfGameObjects()

			self.keepPlayersInBounds()

			self.handleCollisions()

			self.updatePowerBars()

			self.draw()

			self.frameCount += 1
			clock.tick(self.framerate)
			pygame.event.pump()

	## Reset each game object to its starting position
	def resetPositions(self):
		
		for i, player in enumerate(self.team1):
			self.team1[i].x = ((self.winWidth / 2) / (len(self.team1) + 1)) * (i + 1)
			self.team1[i].y = self.winHeight
			self.team1[i].yv = 0
			self.team1[i].powerX = ((self.winWidth / 2) / (len(self.team1) + 1)) * (i + 1) - (self.team1[i].powerWidth / 2)
			self.team1[i].powerY = 13

		for i, player in enumerate(self.team2):
			self.team2[i].x = (((self.winWidth / 2) / (len(self.team2) + 1)) * (i + 1)) + (self.winWidth / 2)
			self.team2[i].y = self.winHeight
			self.team2[i].yv = 0
			self.team2[i].powerX = (((self.winWidth / 2) / (len(self.team2) + 1)) * (i + 1)) + (self.winWidth / 2) - (self.team2[i].powerWidth / 2)
			self.team2[i].powerY = 13
		index = random.randint(0, len(self.teamToServe) - 1)
		for i, player in enumerate(self.teamToServe):
			if i == index:
				self.ball.x = player.x
		self.ball.y = self.winHeight / 3
		self.ball.xv = 0
		self.ball.yv = 0
		self.pointStartFrameCount = self.frameCount

	# Hide the game messages after they time out
	def hideMessagesOnTimeout(self, messageTimeoutFrameCount):

		players = self.team1 + self.team2
		for i, player in enumerate(players):
			if self.frameCount - players[i].messageStartFrame >= messageTimeoutFrameCount:
				players[i].displayMessage = ""
		if self.frameCount - self.pointStartFrameCount >= messageTimeoutFrameCount and self.gameOver == False:
			self.message = ""
			self.subMessage = ""

	## Check if any new controllers have been connected
	def checkForXInputDevices(self):

		if platform == "win32":
			controllers = XInputJoystick.enumerate_devices()
			if len(controllers) > 0 and len(self.team1) > 0:
				if self.team1[0].xinput is None:
					self.team1[0].setXInput(controllers[0], self.frameCount)
			if len(controllers) > 1 and len(self.team2) > 0:
				if self.team2[0].xinput is None:
					self.team2[0].setXInput(controllers[1], self.frameCount)
			if len(controllers) > 2 and len(self.team1) > 1:
				if self.team1[1].xinput is None:
					self.team1[1].setXInput(controllers[2], self.frameCount)
			if len(controllers) > 3 and len(self.team2) > 1:
				if self.team2[1].xinput is None:
					self.team2[1].setXInput(controllers[3], self.frameCount)

	## Check for input from each player
	def getInputFromPlayers(self):

		keys = pygame.key.get_pressed()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q and keys[pygame.K_LCTRL]:
					return False
				if event.key == pygame.K_r and keys[pygame.K_LCTRL]:
					self.resetPositions()
				if event.key == pygame.K_1:
					self.team1[0].isAI = not self.team1[0].isAI
				if event.key == pygame.K_2:
					self.team2[0].isAI = not self.team2[0].isAI
				if event.key == pygame.K_RETURN and self.gameOver == True:
					self.startGame(False)

		for player in self.team1 + self.team2:
			player.getPlayerAction(keys, self.frameCount, self)

		return True

	## Update the position of the ball and each player
	def updatePositionOfGameObjects(self):
		
		for player in self.team1 + self.team2:
			if player.y < self.winHeight:
				player.updatePosition(self.gravity)
			else:
				player.updatePosition(0)
		self.ball.updatePosition(self.gravity)

	## Enforce the boundaries on each side of the court
	def keepPlayersInBounds(self):
		
		for i, player in enumerate(self.team1):
			if player.x - player.radius < 1:
				self.team1[i].x = player.radius
				self.team1[i].xv = 0
			elif player.x + player.radius > self.winWidth / 2 - self.netWidth / 2 - 1:
				self.team1[i].x = self.winWidth / 2 - self.netWidth / 2 - player.radius - 1
				self.team1[i].xv = 0
			if player.y >= self.winHeight:
				self.team1[i].y = self.winHeight
				self.team1[i].yv = 0
				self.team1[i].jumpEnabled = True

		for i, player in enumerate(self.team2):
			if player.x - player.radius < self.winWidth / 2 + self.netWidth / 2 + 1:
				self.team2[i].x = self.winWidth / 2 + self.netWidth / 2 + player.radius + 1
				self.team2[i].xv = 0
			elif player.x + player.radius > self.winWidth - 1:
				self.team2[i].x = self.winWidth - player.radius - 1
				self.team2[i].xv = 0
			if player.y >= self.winHeight:
				self.team2[i].y = self.winHeight
				self.team2[i].yv = 0
				self.team2[i].jumpEnabled = True

	## Detect and process various collision events
	def handleCollisions(self):

		# Ball contacts player
		for player in self.team1 + self.team2:
			if self.ballContactsCircle(player.x, player.y, player.radius) == True:
				if abs(self.ball.yv - player.yv) < 3:
					self.ball.x, self.ball.y = self.getBallContactsCirclePosition(player.x, player.y, player.radius)
				elif player.xinput is not None:
					player.frameMarker = self.frameCount
					player.xinput.set_vibration(1.0, 1.0)
				(self.ball.xv, self.ball.yv) = self.getBallContactsCircleVelocity(player.x, player.y, player.xv, player.yv, self.bounceCoefficientPlayer, self.playerToBallHorizontalBoost)
			
			# Deactivate XInput controller vibration several frames after the ball contacts a player
			if player.xinput is not None:
				if self.frameCount - player.frameMarker >= self.framerate / 15.0:
					player.xinput.set_vibration(0.0, 0.0)

		# Ball contacts floor
		if self.ball.y > self.winHeight - self.ball.radius:
			self.ball.y = self.winHeight - self.ball.radius
			self.ball.yv = -self.ball.yv * self.bounceCoefficient
			# Team 1 scores a point
			if self.ball.x > self.winWidth / 2:
				self.teamToServe = self.team1
				for i, player in enumerate(self.team1):
					if self.team1[i].powerActive == False:
						self.team1[i].incrementPowerPct(0.15)
				if self.gameOver == False:
					self.team1Score += 1
					if self.team1Score == self.scoreLimit:
						self.message = self.getGameOverMessage(self.team1)
					else:
						self.message = self.getTeamScoreMessage(self.team1)
						if (self.insultsEnabled == True):
							self.subMessage = self.getInsultMessage(self.team2)
						else:
							self.subMessage = ""
			# Team 2 scores a point
			else:
				self.teamToServe = self.team2
				for i, player in enumerate(self.team2):
					if self.team2[i].powerActive == False:
						self.team2[i].incrementPowerPct(0.15)
				if self.gameOver == False:
					self.team2Score += 1
					if self.team2Score == self.scoreLimit:
						self.message = self.getGameOverMessage(self.team2)
					else:
						self.message = self.getTeamScoreMessage(self.team2)
						if (self.insultsEnabled == True):
							self.subMessage = self.getInsultMessage(self.team1)
						else:
							self.subMessage = ""

			# Pause briefly before starting a new point
			self.draw()
			for player in self.team1 + self.team2:
				if player.xinput is not None:
					player.xinput.set_vibration(0.0, 0.0)
			pygame.time.delay(500)
			self.resetPositions()

		# Ball contacts wall
		if self.ball.x - self.ball.radius < 1:
			self.ball.x = self.ball.radius
			self.ball.xv = -self.ball.xv * self.bounceCoefficient
		elif self.ball.x + self.ball.radius > self.winWidth:
			self.ball.x = self.winWidth - self.ball.radius
			self.ball.xv = -self.ball.xv * self.bounceCoefficient

		# Ball contacts net
		if self.ballContactsCircle(self.winWidth / 2, self.winHeight - self.netHeight + (self.netWidth / 2), self.netWidth / 2) == True:
				(self.ball.xv, self.ball.yv) = self.getBallContactsCircleVelocity(self.winWidth / 2, self.winHeight - self.netHeight + (self.netWidth / 2), 0, 0, self.bounceCoefficientNet, 1)
		elif self.ball.y > self.winHeight - self.netHeight + self.netWidth:
			if abs((self.winWidth / 2) - (self.ball.x + self.ball.radius)) <= self.netWidth / 2:
				self.ball.x = (self.winWidth / 2) - (self.netWidth / 2) - self.ball.radius
				self.ball.xv = -self.ball.xv * self.bounceCoefficientNet
			elif abs((self.ball.x - self.ball.radius) - (self.winWidth / 2)) <= self.netWidth / 2:
				self.ball.x = (self.winWidth / 2) + (self.netWidth / 2) + self.ball.radius
				self.ball.xv = -self.ball.xv * self.bounceCoefficientNet

	## Increment each player's power bar in the proper direction
	def updatePowerBars(self):

		players = self.team1 + self.team2
		for i, player in enumerate(players):
			if player.powerActive == False and player.powerPct < 1:
				players[i].incrementPowerPct(0.0003)
			elif player.powerActive == True and player.powerPct > 0:
				players[i].incrementPowerPct(-0.0012)

	## Draw the current state of the game
	def draw(self):

		# Fill window with background color
		self.gameWin.fill(self.backgroundColor)

		# Draw net
		pygame.draw.rect(self.gameWin, self.netColor, (self.winWidth / 2 - (self.netWidth / 2), self.winHeight - self.netHeight + (self.netWidth / 2), self.netWidth + 1, self.netHeight))
		pygame.gfxdraw.aacircle(self.gameWin, int(self.winWidth / 2), int(self.winHeight - self.netHeight + (self.netWidth / 2)), int(self.netWidth / 2), self.netColor)
		pygame.gfxdraw.filled_circle(self.gameWin, int(self.winWidth / 2), int(self.winHeight - self.netHeight + (self.netWidth / 2)), int(self.netWidth / 2), self.netColor)

		# Draw players
		if len(self.team1 + self.team2) > 2 or self.backgroundImage is not None:
			drawPillow = True
		else:
			drawPillow = False

		if self.frameCount - self.playerMessageFlashRate >= self.playerMessageFlashFrameMarker:
			self.drawPlayerMessage = not self.drawPlayerMessage
			self.playerMessageFlashFrameMarker = self.frameCount

		if self.frameCount - self.playerPowerBarOutlineFlashRate >= self.playerPowerBarOutlineFrameMarker:
			self.drawPlayerPowerBarOutline = not self.drawPlayerPowerBarOutline
			self.playerPowerBarOutlineFrameMarker = self.frameCount

		for player in self.team1 + self.team2:
			player.draw(self.gameWin, self.backgroundColor, self.ball, drawPillow, self.drawPlayerMessage, self.drawPlayerPowerBarOutline)

		# Draw messages
		messageLabel = self.messageFont.render(self.message, True, self.messageColor)
		messageLabelRect = messageLabel.get_rect(center = (self.winWidth / 2, 20))
		self.gameWin.blit(messageLabel, messageLabelRect)

		if self.gameOver == False or (self.gameOver == True and self.drawPlayerMessage == True):
			subMessageLabel = self.subMessageFont.render(self.subMessage, True, self.messageColor)
			subMessageLabelRect = subMessageLabel.get_rect(center = (self.winWidth / 2, 50))
			self.gameWin.blit(subMessageLabel, subMessageLabelRect)

		# Draw scores
		team1ScoreLabel = self.scoreFont.render(str(self.team1Score), True, self.messageColor)
		self.gameWin.blit(team1ScoreLabel, (30, 5))
		team2ScoreLabel = self.scoreFont.render(str(self.team2Score), True, self.messageColor)
		self.gameWin.blit(team2ScoreLabel, (self.winWidth - 60, 5))

		# Draw ball
		self.ball.draw(self.gameWin)

		# Refresh scene
		pygame.display.update()

	## Check if the ball is contacting a circle of the given dimensions
	def ballContactsCircle(self, circleX, circleY, circleRadius):

		if math.sqrt( ((self.ball.x - circleX) ** 2) + ((self.ball.y - circleY) ** 2) ) <= (self.ball.radius + circleRadius):
			return True
		return False

	## Calculate the rebound velocity vector of the ball after contacting a circle of the given dimensions
	def getBallContactsCircleVelocity(self, circleX, circleY, circleXV, circleYV, bounceCoefficient, xvBoost):

		ballSpeed = math.sqrt((self.ball.xv ** 2) + (self.ball.yv ** 2))
		xDiff = -(self.ball.x - circleX)
		yDiff = -(self.ball.y - circleY)
		if xDiff > 0:
			angle = math.degrees(math.atan(yDiff / xDiff))
			xSpeed = -ballSpeed * math.cos(math.radians(angle))
			ySpeed = -ballSpeed * math.sin(math.radians(angle))
		elif xDiff < 0:
			if yDiff > 0:
				angle = 180 + math.degrees(math.atan(yDiff / xDiff))
			elif yDiff < 0:
				angle = -180 + math.degrees(math.atan(yDiff / xDiff))
			xSpeed = -ballSpeed * math.cos(math.radians(angle))
			ySpeed = -ballSpeed * math.sin(math.radians(angle))
		elif xDiff == 0:
			if yDiff > 0:
				angle = -90
			else:
				angle = 90
			xSpeed = ballSpeed * math.cos(math.radians(angle))
			ySpeed = ballSpeed * math.sin(math.radians(angle))
		elif yDiff == 0:
			if yDiff < 0:
				angle = 0
			else:
				angle = 180
			xSpeed = ballSpeed * math.cos(math.radians(angle))
			ySpeed = ballSpeed * math.sin(math.radians(angle))
		xv = (xSpeed + (circleXV * self.playerToBallMomentumTransfer)) * bounceCoefficient * xvBoost
		yv = (ySpeed + (circleYV * self.playerToBallMomentumTransfer)) * bounceCoefficient
		return (xv, yv)

	## Calculate the position of the ball around the arc of the circle of the given dimensions it is currently contacting
	def getBallContactsCirclePosition(self, circleX, circleY, circleRadius):

		combinedRadius = self.ball.radius + circleRadius
		xDiff = -(self.ball.x - circleX)
		yDiff = -(self.ball.y - circleY)
		if xDiff > 0:
			if yDiff > 0:
				angle = math.degrees(math.atan(yDiff / xDiff))
				xShift = -combinedRadius * math.cos(math.radians(angle))
				yShift = -combinedRadius * math.sin(math.radians(angle))
			elif yDiff < 0:
				angle = math.degrees(math.atan(yDiff / xDiff))
				xShift = -combinedRadius * math.cos(math.radians(angle))
				yShift = -combinedRadius * math.sin(math.radians(angle))
		elif xDiff < 0:
			if yDiff > 0:
				angle = 180 + math.degrees(math.atan(yDiff / xDiff))
				xShift = -combinedRadius * math.cos(math.radians(angle))
				yShift = -combinedRadius * math.sin(math.radians(angle))
			elif yDiff < 0:
				angle = -180 + math.degrees(math.atan(yDiff / xDiff))
				xShift = -combinedRadius * math.cos(math.radians(angle))
				yShift = -combinedRadius * math.sin(math.radians(angle))
		elif xDiff == 0:
			if yDiff > 0:
				angle = -90
			else:
				angle = 90
			xShift = combinedRadius * math.cos(math.radians(angle))
			yShift = combinedRadius * math.sin(math.radians(angle))
		elif yDiff == 0:
			if yDiff < 0:
				angle = 0
			else:
				angle = 180
			xShift = combinedRadius * math.cos(math.radians(angle))
			yShift = combinedRadius * math.sin(math.radians(angle))
		return (circleX + xShift, circleY + yShift)

	## Get the message to display when a point is scored
	def getTeamScoreMessage(self, team):

		if len(team) == 1:
			return team[0].name + " Scores!"
		else:
			return team[0].name + "/" + team[1].name + " Scores!"

	## The loser of the point must be shamed. This function makes that happen.
	def getInsultMessage(self, losingTeam):

		if len(losingTeam) == 1:
			loser = losingTeam[0].name
			insults =	[	"@ got REKT right there.", "@, turn your f*cking brain on.", "@ brought dishonor to his family.",
							"Hey @, how do you like them apples?", "@, u mad bro?", "@ must be pretty rattled after that.", "@ continues to suck some serious ass.",
							"@, wow, not even close.", "I'm not mad, I'm just disappointed. In @. For that.",
							"@ is currently playing like a little bitch.", "@ is simply an embarassment.", "@ is garbage. Complete and utter garbage",
							"@.isScrub() == True", "@ just managed to look like a complete idiot.", "@ is trash. Plain and simple.",
							"@, please try not to suck so much.", "@ f*cked up and he knows it."
						]

			if len(self.insultsUsedAlready) >= len(insults):
				self.insultsUsedAlready.clear()

			insult = insults[random.randint(0, len(insults) - 1)]
			while (insult in self.insultsUsedAlready):
				insult = insults[random.randint(0, len(insults) - 1)]
			self.insultsUsedAlready.append(insult)
			return insult.replace("@", loser)
		else:
			return ""

	## Declare the winner when the score limit is reached
	def getGameOverMessage(self, winningTeam):

		self.gameOver = True

		self.subMessage = "Press ENTER to start new game"

		if len(winningTeam) == 1:
			return winningTeam[0].name + " Wins!"
		else:
			return winningTeam[0].name + "/" + winningTeam[1].name + " Wins!"

	## Reset player powers for a new game
	def resetPlayerPowers(self):
		players = self.team1 + self.team2
		for i, player in enumerate(players):
			players[i].powerPct = 0.00
			players[i].deactivatePowers()