## Chris Leveille
## April 2019

import pygame
import math
import random
from pygame import gfxdraw
from Player import Player
from Ball import Ball

class Game:

	## Create new game
	def __init__(self, winWidth, winHeight, backgroundColor, backgroundImage, frameTimeMS, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
					playerToBallMomentumTransfer, playerToBallHorizontalBoost, insultsEnabled, netHeight, netWidth, netColor, team1, team2, ball):
		
		self.winWidth = winWidth
		self.winHeight = winHeight
		self.backgroundColor = backgroundColor
		self.backgroundImage = backgroundImage
		self.frameTimeMS = frameTimeMS
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

	## Start the game
	def startGame(self):
		
		pygame.display.set_caption("Slime Volleyball")
		self.gameWin = pygame.display.set_mode((self.winWidth, self.winHeight))
		self.team1Score = 0
		self.team2Score = 0
		self.scoreFont = scoreFont = pygame.font.Font(None, 48)
		self.messageFont = pygame.font.Font(None, 42)
		self.subMessageFont = pygame.font.Font(None, 24)
		self.messageColor = pygame.color.Color("black")
		self.message = "Game On!"
		self.insultsUsedAlready = []
		self.subMessage = "May the slimiest Slime win."
		self.frameCount = 0

		if bool(random.getrandbits(1)) == True:
			self.teamToServe = self.team1
		else:
			self.teamToServe = self.team2

		self.resetPositions()
		self.gameLoop()

	## Main game logic flow executed each frame
	def gameLoop(self):
		
		gameOn = True
		messageTimeoutFrameCount = (1000 / self.frameTimeMS) * 3

		while (gameOn == True):

			# Quit game if window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOn = False

			# Hide the game messages after 3 sec
			if self.frameCount > messageTimeoutFrameCount:
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

	## Reset each game object to its starting position
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

	## Check for input from each player
	def getInputFromPlayers(self):
		
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.resetPositions()
		for player in self.team1 + self.team2:
			player.handleInput(keys)

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

	## Detect and process various collision events
	def handleCollisions(self):

		# Ball contacts player
		for player in self.team1 + self.team2:
			if self.ballContactsCircle(player.x, player.y, player.radius) == True:
				if abs(self.ball.yv) < 3:
					self.ball.x, self.ball.y = self.getBallContactsCirclePosition(player.x, player.y, player.radius)
				(self.ball.xv, self.ball.yv) = self.getBallContactsCircleVelocity(player.x, player.y, player.xv, player.yv, self.bounceCoefficientPlayer, self.playerToBallHorizontalBoost)
				break

		# Ball contacts floor
		if self.ball.y > self.winHeight - self.ball.radius:
			self.ball.y = self.winHeight - self.ball.radius
			self.ball.yv = -self.ball.yv * self.bounceCoefficient
			# Team 1 scores a point
			if self.ball.x > self.winWidth / 2:
				self.teamToServe = self.team1
				self.team1Score += 1
				self.message = self.getTeamScoreMessage(self.team1)
				if (self.insultsEnabled == True):
					self.subMessage = self.getInsultMessage(self.team2)
			# Team 2 scores a point
			else:
				self.teamToServe = self.team2
				self.team2Score += 1
				self.message = self.getTeamScoreMessage(self.team2)
				if (self.insultsEnabled == True):
					self.subMessage = self.getInsultMessage(self.team1)

			# Pause briefly before starting a new rally
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

		# Ball contacts net
		if self.ballContactsCircle(self.winWidth /2, self.winHeight - self.netHeight + (self.netWidth / 2), self.netWidth / 2) == True:
				(self.ball.xv, self.ball.yv) = self.getBallContactsCircleVelocity(self.winWidth / 2, self.winHeight - self.netHeight + (self.netWidth / 2), 0, 0, self.bounceCoefficientNet, 1)
		elif self.ball.y > self.winHeight - self.netHeight + self.netWidth:
			if abs((self.winWidth / 2) - (self.ball.x + self.ball.radius)) <= self.netWidth / 2:
				self.ball.x = (self.winWidth / 2) - (self.netWidth / 2) - self.ball.radius
				self.ball.xv = -self.ball.xv * self.bounceCoefficientNet
			elif abs((self.ball.x - self.ball.radius) - (self.winWidth / 2)) <= self.netWidth / 2:
				self.ball.x = (self.winWidth / 2) + (self.netWidth / 2) + self.ball.radius
				self.ball.xv = -self.ball.xv * self.bounceCoefficientNet

	## Draw the current state of the game
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
		pygame.gfxdraw.aacircle(self.gameWin, int(self.winWidth / 2), int(self.winHeight - self.netHeight + (self.netWidth / 2)), int(self.netWidth / 2), self.netColor)
		pygame.gfxdraw.filled_circle(self.gameWin, int(self.winWidth / 2), int(self.winHeight - self.netHeight + (self.netWidth / 2)), int(self.netWidth / 2), self.netColor)

		# Draw players
		for player in self.team1 + self.team2:
			player.draw(self.gameWin, self.backgroundColor, self.ball)

		# Draw ball
		self.ball.draw(self.gameWin)

		# Refresh scene
		pygame.display.update()

		# Process event queue
		pygame.event.pump()

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
			if yDiff > 0:
				angle = math.degrees(math.atan(yDiff / xDiff))
				xSpeed = -ballSpeed * math.cos(math.radians(angle))
				ySpeed = -ballSpeed * math.sin(math.radians(angle))
			elif yDiff < 0:
				angle = math.degrees(math.atan(yDiff / xDiff))
				xSpeed = -ballSpeed * math.cos(math.radians(angle))
				ySpeed = -ballSpeed * math.sin(math.radians(angle))
		elif xDiff < 0:
			if yDiff > 0:
				angle = 180 + math.degrees(math.atan(yDiff / xDiff))
				xSpeed = -ballSpeed * math.cos(math.radians(angle))
				ySpeed = -ballSpeed * math.sin(math.radians(angle))
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

	## Return the message to display when a point is scored
	def getTeamScoreMessage(self, team):

		if len(team) == 1:
			return team[0].name + " Scores!"
		else:
			return "Team Scores!"

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

## Configure and start a new game
def main():
	pygame.init()
	winWidth = 1000
	winHeight = 500
	backgroundColor = pygame.color.Color("lightblue")
	backgroundImage = None
	frameTimeMS = 7 # number of milliseconds in one frame
	gravity = 0.1 # change in speed per frame
	bounceCoefficient = 0.98
	bounceCoefficientPlayer = 0.98
	bounceCoefficientNet = 0.75
	playerToBallMomentumTransfer = 0.12 # percentage of a player's velocity that gets transferred to the ball on contact
	playerToBallHorizontalBoost = 1.03
	netHeight = 100
	netWidth = 20
	netColor = pygame.color.Color("black")
	insultsEnabled = False
	fourPlayer = False

	playerSpeed = 5 # maximum change in position (# pixels) per frame
	playerAccel = 5 # change in velocity per frame
	playerJump = 5 # immediate upward velocity (pixels per frame) on jump
	playerRadius = 48
	ballRadius = 25
	ballColor = pygame.color.Color("darkgreen")

	if playerRadius == ballRadius * 2:
		playerRadius += 1

	p1 = Player("Blue", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("darkblue"), [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s], "[W, A, D]")
	p2 = Player("Red", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("darkred"), [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN], "[UP, LEFT, RIGHT]")
	p3 = Player("Purple", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("purple"), [pygame.K_t, pygame.K_f, pygame.K_h, pygame.K_g], "[T, F, H]")
	p4 = Player("Orange", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("orange"), [pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k], "[I, J, L]")

	# 1v1
	team1 = [p1] # controls: [W, A, D]
	team2 = [p2] # controls: [UP, LEFT, RIGHT]

	# 2v2
	if fourPlayer == True:
		team1.append(p3) # controls: [T, F, H]
		team2.append(p4) # controls: [I, J, L]

	ball = Ball(ballRadius, ballColor)

	game = Game(winWidth, winHeight, backgroundColor, backgroundImage, frameTimeMS, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
				playerToBallMomentumTransfer, playerToBallHorizontalBoost, insultsEnabled, netHeight, netWidth, netColor, team1, team2, ball)

	game.startGame()

if __name__ == "__main__":
	main()