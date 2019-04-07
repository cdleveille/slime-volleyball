import pygame
from pygame import gfxdraw
import math
import random

# Main game function
def playGame():
	## Initialize properties of game objects
	# Game window properties
	winWidth = 1000
	winHeight = 500
	pygame.display.set_caption("Slime Volleyball")
	gameWin = pygame.display.set_mode((winWidth, winHeight))

	#myimage = pygame.image.load("test.png")
	#imagerect = myimage.get_rect()

	# Game speed and physics properties
	frameTimeMS = 7
	gravity = 0.1
	bounceCoefficient = 0.98
	bounceCoefficientNet = 0.75 
	playerToBallMomentumTransfer = 0.12
	playerToBallHorizontalBoost = 1.03

	# Player, ball, and net properties
	p1Name = "Blue"
	p2Name = "Red"
	p1Score = 0
	p2Score = 0
	p1Serve = bool(random.getrandbits(1))
	playerSpeed = 5
	playerJump = 5
	playerRadius = 50
	pupilFactor = playerRadius / 14
	ballRadius = 25
	netWidth = 20
	netHeight = 100

	# Set up game fonts and messages
	scoreFont = pygame.font.Font(None, 48)
	messageFont = pygame.font.Font(None, 42)
	insultMessageFont = pygame.font.Font(None, 24)
	message = "Game On!"
	insultMessage = ""
	insultsUsedAlready = []

	# Set colors of game objects
	backgroundColor = pygame.color.Color("lightblue")
	ballColor = pygame.color.Color("darkgreen")
	netColor = pygame.color.Color("black")
	p1Color = pygame.color.Color("darkblue")
	p2Color = pygame.color.Color("darkred")
	messageColor = pygame.color.Color("black")

	## Game loop
	gameOn = True
	newPoint = True
	while(gameOn):
		# Reset applicable properties at the start of a new point
		if newPoint == True:
			if p1Serve == True:
				x = winWidth / 4
			else:
				x = winWidth * (3 / 4)
			y = winHeight / 2
			x_v = 0
			y_v = 0

			p1_x = winWidth / 4
			p1_y = winHeight
			p1_x_v = 0
			p1_y_v = 0
			p1JumpEnabled = True

			p2_x = winWidth * (3 / 4)
			p2_y = winHeight
			p2_x_v = 0
			p2_y_v = 0
			p2JumpEnabled = True

			frameCount = 0
			newPoint = False

		# Clear messages after 3 seconds
		if (frameCount >= (1000 / frameTimeMS) * 3):
			message = ""
			insultMessage = ""

		# Quit game if window is closed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOn = False

		## Handle player input
		keys = pygame.key.get_pressed()

		# Restart game if 'R' is pressed
		if keys[pygame.K_r]:
			playGame()

		# Player1 input
		if keys[pygame.K_a] and keys[pygame.K_d]:
			p1_x_v = 0
		elif keys[pygame.K_a]:
			p1_x_v = -playerSpeed
		elif keys[pygame.K_d]:
			p1_x_v = playerSpeed
		else:
			p1_x_v = 0
		if (p1JumpEnabled == True):
			if keys[pygame.K_w]:
				p1_y_v = -playerJump
				p1JumpEnabled = False

		# Player2 input
		if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
			p2_x_v = 0
		elif keys[pygame.K_LEFT]:
			p2_x_v = -playerSpeed
		elif keys[pygame.K_RIGHT]:
			p2_x_v = playerSpeed
		else:
			p2_x_v = 0
		if (p2JumpEnabled == True):
			if keys[pygame.K_UP]:
				p2_y_v = -playerJump
				p2JumpEnabled = False

		## Ball collision events

		# Ball contacts floor
		if y >= (winHeight - ballRadius):
			y = winHeight - ballRadius
			y_v = -y_v * bounceCoefficient
			if x > winWidth / 2:
				p1Score += 1
				message = p1Name + " Scores!"
				insultMessage = getInsultMessage(p2Name, insultsUsedAlready)
				p1Serve = True
			else:
				p2Score += 1
				message = p2Name + " Scores!"
				insultMessage = getInsultMessage(p1Name, insultsUsedAlready)
				p1Serve = False
			pygame.time.delay(500)
			newPoint = True

		# Ball contacts wall
		if x - ballRadius < 0:
			x = ballRadius
			x_v = -x_v * bounceCoefficient
		elif x + ballRadius > winWidth:
			x = winWidth - ballRadius
			x_v = -x_v * bounceCoefficient

		# Ball contacts Player1
		if ballContactsCircle(x, y, ballRadius, p1_x, p1_y, playerRadius) == True:
			(x_v, y_v) = getBallCircleVelocityVector(x, y, x_v, y_v, p1_x, p1_y, p1_x_v, p1_y_v, bounceCoefficient, playerToBallMomentumTransfer, playerToBallHorizontalBoost)

		# Ball contacts Player2
		if ballContactsCircle(x, y, ballRadius, p2_x, p2_y, playerRadius) == True:
			(x_v, y_v) = getBallCircleVelocityVector(x, y, x_v, y_v, p2_x, p2_y, p2_x_v, p2_y_v, bounceCoefficient, playerToBallMomentumTransfer, playerToBallHorizontalBoost)

		# Ball contacts top of net
		if ballContactsCircle(x, y, ballRadius, winWidth / 2, winHeight - netHeight + (netWidth / 2), netWidth / 2) == True:
			(x_v, y_v) = getBallCircleVelocityVector(x, y, x_v, y_v, winWidth / 2, winHeight - netHeight + (netWidth / 2), 0, 0, bounceCoefficientNet, 1, 1)

		# Ball contacts side of net
		elif y > winHeight - netHeight + netWidth:
			if abs((winWidth / 2) - (x + ballRadius)) <= netWidth / 2:
				x = (winWidth / 2) - (netWidth / 2) - ballRadius
				x_v = -x_v * bounceCoefficientNet
			elif abs((x - ballRadius) - (winWidth / 2)) <= netWidth / 2:
				x = (winWidth / 2) + (netWidth / 2) + ballRadius
				x_v = -x_v * bounceCoefficientNet

		## Update game objects for next frame

		# Update ball position and vertical speed
		x += x_v
		y += y_v
		y_v += gravity

		# Update Player1 position
		p1_x += p1_x_v
		p1_y += p1_y_v
		if p1_y < winHeight:
			p1_y_v += gravity
		else:
			p1_y = winHeight
			p1JumpEnabled = True
		if p1_x - playerRadius < 0:
			p1_x = playerRadius
		elif p1_x + playerRadius > winWidth / 2 - netWidth / 2:
			p1_x = winWidth / 2 - netWidth / 2 - playerRadius

		# Update Player2 position
		p2_x += p2_x_v
		p2_y += p2_y_v
		if p2_y < winHeight:
			p2_y_v += gravity
		else:
			p2_y = winHeight
			p2JumpEnabled = True
		if p2_x + playerRadius > winWidth:
			p2_x = winWidth - playerRadius
		elif p2_x - playerRadius < winWidth / 2 + netWidth / 2:
			p2_x = winWidth / 2 + netWidth / 2 + playerRadius
		
		# Calculate Player1 pupil shift
		(p1_pupilShiftX, p1_pupilShiftY) = getPlayerPupilShift(x, y, p1_x, p1_y, playerRadius, pupilFactor)

		# Calculate Player2 pupil shift
		(p2_pupilShiftX, p2_pupilShiftY) = getPlayerPupilShift(x, y, p2_x, p2_y, playerRadius, pupilFactor)

		# Control framerate
		pygame.time.delay(frameTimeMS)

		## Draw game objects
		# Draw backgound color
		gameWin.fill(backgroundColor)
		# Draw Player1
		drawAACircle(gameWin, int(p1_x), int(p1_y), playerRadius, p1Color)
		drawAACircle(gameWin, int(p1_x + playerRadius * 0.4), int(p1_y - playerRadius / 2), int(playerRadius / 5), pygame.color.Color("lightgray"))
		drawAACircle(gameWin, int(p1_x + playerRadius * 0.4 + p1_pupilShiftX), int(p1_y - playerRadius / 2 + p1_pupilShiftY), int(playerRadius / 8), pygame.color.Color("black"))
		pygame.draw.rect(gameWin, backgroundColor, (p1_x - playerRadius, p1_y, playerRadius * 2 + 1, playerRadius + 1))
		# Draw Player2
		drawAACircle(gameWin, int(p2_x), int(p2_y), playerRadius, p2Color)
		drawAACircle(gameWin, int(p2_x - playerRadius * 0.4), int(p2_y - playerRadius / 2), int(playerRadius / 5), pygame.color.Color("lightgray"))
		drawAACircle(gameWin, int(p2_x - playerRadius * 0.4 + p2_pupilShiftX), int(p2_y - playerRadius / 2 + p2_pupilShiftY), int(playerRadius / 8), pygame.color.Color("black"))
		pygame.draw.rect(gameWin, backgroundColor, (p2_x - playerRadius, p2_y, playerRadius * 2 + 1, playerRadius + 1))
		# Draw Player1 score
		p1ScoreLabel = scoreFont.render(str(p1Score), True, p1Color)
		gameWin.blit(p1ScoreLabel, (30, 5))
		# Draw Player1 score
		p2ScoreLabel = scoreFont.render(str(p2Score), True, p2Color)
		gameWin.blit(p2ScoreLabel, (winWidth - 60, 5))
		# Draw message
		messageLabel = messageFont.render(message, True, messageColor)
		messageLabelRect = messageLabel.get_rect(center = (winWidth / 2, 20))
		gameWin.blit(messageLabel, messageLabelRect)
		# Draw insult message
		insultMessageLabel = insultMessageFont.render(insultMessage, True, messageColor)
		insultMessageLabelRect = insultMessageLabel.get_rect(center = (winWidth / 2, 50))
		gameWin.blit(insultMessageLabel, insultMessageLabelRect)
		# Draw net
		pygame.draw.rect(gameWin, netColor, (winWidth / 2 - (netWidth / 2), winHeight - netHeight + (netWidth / 2), netWidth + 1, netHeight))
		drawAACircle(gameWin, int(winWidth / 2), int(winHeight - netHeight + (netWidth / 2)), int(netWidth / 2), netColor)
		# Draw ball
		drawAACircle(gameWin, int(x), int(y), ballRadius, ballColor)
		# If ball is off-screen, draw a dot indicating its horizontal location
		# The size of the dot indicates the height of the ball
		if y - ballRadius < -440:
			drawAACircle(gameWin, int(x), 10, 4, ballColor)
		elif y - ballRadius < -340:
			drawAACircle(gameWin, int(x), 10, 5, ballColor)
		elif y - ballRadius < -240:
			drawAACircle(gameWin, int(x), 10, 6, ballColor)
		elif y - ballRadius < -140:
			drawAACircle(gameWin, int(x), 10, 7, ballColor)
		elif y - ballRadius < -40:
			drawAACircle(gameWin, int(x), 10, 8, ballColor)
		
		pygame.display.update()
		frameCount += 1

	pygame.quit()

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

def getPlayerPupilShift(x, y, p_x, p_y, playerRadius, pupilFactor):
	(pupilShiftX, pupilShiftY) = (0, 0)
	XDiff = -(x - (p_x + playerRadius * 0.4))
	YDiff = -(y - (p_y - playerRadius / 2))
	if XDiff > 0:
		if YDiff > 0:
			Angle = math.degrees(math.atan(YDiff / XDiff))
			pupilShiftX = -pupilFactor * math.cos(math.radians(Angle))
			pupilShiftY = -pupilFactor * math.sin(math.radians(Angle))
		elif YDiff < 0:
			Angle = math.degrees(math.atan(YDiff / XDiff))
			pupilShiftX = -pupilFactor * math.cos(math.radians(Angle))
			pupilShiftY = -pupilFactor * math.sin(math.radians(Angle))
	elif XDiff < 0:
		if YDiff > 0:
			Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
			pupilShiftX = -pupilFactor * math.cos(math.radians(Angle))
			pupilShiftY = -pupilFactor * math.sin(math.radians(Angle))
		elif YDiff < 0:
			Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
			pupilShiftX = -pupilFactor * math.cos(math.radians(Angle))
			pupilShiftY = -pupilFactor * math.sin(math.radians(Angle))
	elif XDiff == 0:
		if YDiff > 0:
			Angle = -90
		else:
			Angle = 90
			pupilShiftX = pupilFactor * math.cos(math.radians(Angle))
			pupilShiftY = pupilFactor * math.sin(math.radians(Angle))
	elif YDiff == 0:
		if XDiff < 0:
			Angle = 0
		else:
			Angle = 180
			pupilShiftX = pupilFactor * math.cos(math.radians(Angle))
			pupilShiftY = pupilFactor * math.sin(math.radians(Angle))
	return (pupilShiftX, pupilShiftY)

# The loser of the point must be shamed. This function makes that happen.
def getInsultMessage(loser, insultsUsedAlready):
	insults =	[	" got REKT right there.", ", turn your f*cking brain on.", " brought dishonor to his family.",
					", how do you like them apples?", ", u mad bro?", " seems rattled.", " continues to suck some serious ass.",
					", wow, not even close.", ", I'm not mad, I'm just disappointed. In you. For that.",
					" is playing like a little bitch.", " is simply an embarassment.", " just found a whole new meaning for the word 'suck'.",
					".isScrub() == True", " just managed to look like a complete idiot.", " is trash. Plain and simple.",
					", the suckage is real."
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
	pygame.gfxdraw.aacircle(gameWin, x, y, r, color)
	pygame.gfxdraw.filled_circle(gameWin, x, y, r, color)

pygame.init()
playGame()