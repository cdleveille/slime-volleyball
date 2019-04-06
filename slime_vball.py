import pygame
import math
import random

def playGame():
	pygame.init()

	# Initialize game window
	winWidth = 1000
	winHeight = 500
	pygame.display.set_caption("Slime Volleyball")
	gameWin = pygame.display.set_mode((winWidth, winHeight))

	## Initialize properties of game objects

	#myimage = pygame.image.load("test.png")
	#imagerect = myimage.get_rect()

	ballRadius = 25

	# Gravity/bounce properties
	gravity = 0.18
	bounceCoefficient = 0.98
	bounceCoefficientNet = 0.75
	playerToBallTransfer = 0.15

	# Shared player properties
	playerSpeed = 6.5
	playerJump = 7
	playerRadius = 50

	# Net properties
	netWidth = 20
	netHeight = 100

	# Set up game fonts
	scoreFont = pygame.font.Font(None,48)
	messageFont = pygame.font.Font(None,42)
	messageDetailFont = pygame.font.Font(None,24)

	message = ""
	messageDetail = ""

	# Set player scores to 0
	p1Score = 0
	p2Score = 0

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

		if (newPoint == True):
			num = random.randint(1, 2)
			if num == 1:
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

		if (frameCount >= 300):
			message = ""
			messageDetail = ""

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
			if x >= winWidth / 2:
				p1Score += 1
				message = "P1 Scores!"
				messageDetail = getMessageDetail("P2")
			elif x < winWidth / 2:
				p2Score += 1
				message = "P2 Scores!"
				messageDetail = getMessageDetail("P1")
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
		if math.sqrt( ((x - p1_x) ** 2) + ((y - p1_y) ** 2) ) <= (ballRadius + playerRadius):
			ballSpeed = math.sqrt((x_v ** 2) + (y_v ** 2))
			XDiff = -(x - p1_x)
			YDiff = -(y - p1_y)
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
			x_v = (XSpeed + (p1_x_v * playerToBallTransfer)) * bounceCoefficient
			y_v = (YSpeed + (p1_y_v * playerToBallTransfer)) * bounceCoefficient

		# Ball contacts Player2
		if math.sqrt( ((x - p2_x) ** 2) + ((y - p2_y) ** 2) ) <= (ballRadius + playerRadius):
			ballSpeed = math.sqrt((x_v ** 2) + (y_v ** 2))
			XDiff = -(x - p2_x)
			YDiff = -(y - p2_y)
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
			x_v = (XSpeed + (p2_x_v * playerToBallTransfer)) * bounceCoefficient
			y_v = (YSpeed + (p2_y_v * playerToBallTransfer)) * bounceCoefficient

		# Ball contacts top of net
		topNet_x = winWidth / 2
		topNet_y = winHeight - netHeight + (netWidth / 2)
		if math.sqrt( ((x - topNet_x) ** 2) + ((y - topNet_y) ** 2) ) <= (ballRadius + (netWidth / 2)):
			ballSpeed = math.sqrt((x_v ** 2) + (y_v ** 2))
			XDiff = -(x - topNet_x)
			YDiff = -(y - topNet_y)
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
			x_v = XSpeed * bounceCoefficientNet
			y_v = YSpeed * bounceCoefficientNet

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

		# Control framerate
		pygame.time.delay(10)

		## Draw game objects
		# Draw backgound color
		gameWin.fill(backgroundColor)
		# Draw Player1
		pygame.draw.circle(gameWin, p1Color, (int(p1_x), int(p1_y)), playerRadius)
		pygame.draw.rect(gameWin, backgroundColor, (p1_x - playerRadius, p1_y, playerRadius * 2, playerRadius))
		# Draw Player2
		pygame.draw.circle(gameWin, p2Color, (int(p2_x), int(p2_y)), playerRadius)
		pygame.draw.rect(gameWin, backgroundColor, (p2_x - playerRadius, p2_y, playerRadius * 2, playerRadius))
		# Draw Player1 score
		p1ScoreLabel = scoreFont.render(str(p1Score), True, p1Color)
		gameWin.blit(p1ScoreLabel, (30, 5))
		# Draw Player1 score
		p2ScoreLabel = scoreFont.render(str(p2Score), True, p2Color)
		gameWin.blit(p2ScoreLabel, (winWidth - 60, 5))
		# Draw message
		messageLabel = messageFont.render(message, True, messageColor)
		gameWin.blit(messageLabel, (winWidth / 2 - 80, 10))
		# Draw detail message
		messageDetailLabel = messageDetailFont.render(messageDetail, True, messageColor)
		gameWin.blit(messageDetailLabel, (winWidth / 2 - 60, 40))
		# Draw ball
		pygame.draw.circle(gameWin, ballColor, (int(x), int(y)), ballRadius)
		# If ball is off-screen, draw a dot indicating its horizontal location
		# The size of the dot indicates the height of the ball
		if y - ballRadius < -400:
			pygame.draw.circle(gameWin, ballColor, (int(x), 10), 4)
		elif y - ballRadius < -300:
			pygame.draw.circle(gameWin, ballColor, (int(x), 10), 5)
		elif y - ballRadius < -200:
			pygame.draw.circle(gameWin, ballColor, (int(x), 10), 6)
		elif y - ballRadius < -100:
			pygame.draw.circle(gameWin, ballColor, (int(x), 10), 7)
		elif y - ballRadius < 0:
			pygame.draw.circle(gameWin, ballColor, (int(x), 10), 8)
		# Draw net
		pygame.draw.rect(gameWin, netColor, (winWidth / 2 - (netWidth / 2), winHeight - netHeight + (netWidth / 2), netWidth, netHeight))
		pygame.draw.circle(gameWin, netColor, (int(winWidth / 2), int(winHeight - netHeight + (netWidth / 2))), int(netWidth / 2))
		
		pygame.display.update()
		frameCount += 1

	pygame.quit()

def getMessageDetail(loser):
	return "get rekt, " + str(loser)
	
playGame()