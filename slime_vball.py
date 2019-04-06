import pygame
import math
import random

def playGame():
	pygame.init()

	# Initialize game window
	winWidth = 1000
	winHeight = 500
	gameWin = pygame.display.set_mode((winWidth, winHeight))

	## Initialize properties of game objects

	# Ball properties
	num = random.randint(1,2)
	if num == 1:
		x = winWidth / 4
	else:
		x = winWidth * (3 / 4)
	y = winHeight / 2
	x_v = 0
	y_v = 0
	gravity = 0.18
	bounceCoefficient = 0.97
	bounceCoefficientPlayer = 1
	bounceCoefficientNet = 0.75
	ballRadius = 25

	# Player1 properties
	p1_x = winWidth / 4
	p1_y = winHeight
	p1_x_v = 0
	p1_y_v = 0
	p1CanJump = True
	p1Score = 0

	# Player2 properties
	p2_x = winWidth * (3 / 4)
	p2_y = winHeight
	p2_x_v = 0
	p2_y_v = 0
	p2CanJump = True
	p2Score = 0

	# Shared player properties
	playerSpeed = 7
	playerJump = 7
	playerRadius = 50

	# Net properties
	netWidth = 40
	netHeight = 100

	myFont = pygame.font.Font(None,48)

	# Set colors of game objects
	backgroundColor = pygame.color.Color("lightblue")
	ballColor = pygame.color.Color("black")
	netColor = pygame.color.Color("black")
	p1Color = pygame.color.Color("darkblue")
	p2Color = pygame.color.Color("darkred")

	## Game loop
	gameOn = True
	while(gameOn):

		# Control framerate
		pygame.time.delay(10)

		# Draw backgound color
		gameWin.fill(backgroundColor)
		# Draw Player1
		pygame.draw.circle(gameWin, p1Color, (int(p1_x), int(p1_y)), playerRadius)
		pygame.draw.rect(gameWin, backgroundColor, (p1_x - playerRadius, p1_y, playerRadius * 2, playerRadius))
		# Draw Player2
		pygame.draw.circle(gameWin, p2Color, (int(p2_x), int(p2_y)), playerRadius)
		pygame.draw.rect(gameWin, backgroundColor, (p2_x - playerRadius, p2_y, playerRadius * 2, playerRadius))
		# Draw Player1 score
		p1ScoreLabel = myFont.render(str(p1Score), True, p1Color)
		gameWin.blit(p1ScoreLabel, (10,5))
        # Draw Player1 score
		p2ScoreLabel = myFont.render(str(p2Score), True, p2Color)
		gameWin.blit(p2ScoreLabel, (960,5))
		# Draw ball
		pygame.draw.circle(gameWin, ballColor, (int(x), int(y)), ballRadius)
		# If ball is off-screen, draw a dot indicting its horizontal location
		if y - ballRadius < 0:
			pygame.draw.circle(gameWin, ballColor, (int(x), 10), 5)
		# Draw net
		pygame.draw.rect(gameWin, netColor, (winWidth / 2 - (netWidth / 2), winHeight - netHeight + (netWidth / 2), netWidth, netHeight - (netWidth / 2)))
		pygame.draw.circle(gameWin, netColor, (int(winWidth / 2), int(winHeight - netHeight + (netWidth / 2))), int(netWidth / 2))

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
			p1_x_v = -(playerSpeed)
		elif keys[pygame.K_d]:
			p1_x_v = playerSpeed
		else:
			p1_x_v = 0
		if (p1CanJump == True):
			if keys[pygame.K_w]:
				p1_y_v = -(playerJump)
				p1CanJump = False

		# Player2 input
		if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
			p2_x_v = 0
		elif keys[pygame.K_LEFT]:
			p2_x_v = -(playerSpeed)
		elif keys[pygame.K_RIGHT]:
			p2_x_v = playerSpeed
		else:
			p2_x_v = 0
		if (p2CanJump == True):
			if keys[pygame.K_UP]:
				p2_y_v = -(playerJump)
				p2CanJump = False

		# Update ball position
		x += x_v
		y += y_v
		y_v += gravity

		# Ball contacts floor
		if y >= (winHeight - ballRadius):
			y = winHeight - ballRadius
			y_v = -(bounceCoefficient * y_v)
			if x > winWidth / 2:
				p1Score += 1
			elif x < winWidth / 2:
				p2Score += 1

		# Ball contacts wall
		if x - ballRadius < 0:
			x = ballRadius
			x_v = -(x_v * bounceCoefficient)
		elif x + ballRadius > winWidth:
			x = winWidth - ballRadius
			x_v = -(x_v * bounceCoefficient)

		# Update Player1 position
		p1_x += p1_x_v
		p1_y += p1_y_v
		if p1_y < winHeight:
			p1_y_v += gravity
		else:
			p1_y = winHeight
			p1CanJump = True
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
			p2CanJump = True
		if p2_x + playerRadius > winWidth:
			p2_x = winWidth - playerRadius
		elif p2_x - playerRadius < winWidth / 2 + netWidth / 2:
			p2_x = winWidth / 2 + netWidth / 2 + playerRadius

		# Handle Player1 collision with ball
		if math.sqrt( ((x - p1_x) ** 2) + ((y - p1_y) ** 2) ) <= (ballRadius + playerRadius):
			ballSpeed = math.sqrt((x_v ** 2)+(y_v ** 2))
			XDiff = -(x - p1_x)
			YDiff = -(y - p1_y)
			if XDiff > 0:
				if YDiff > 0:
					Angle = math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
				elif YDiff < 0:
					Angle = math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
			elif XDiff < 0:
				if YDiff > 0:
					Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
				elif YDiff < 0:
					Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
			elif XDiff == 0:
				if YDiff > 0:
					Angle = -90
				else:
					Angle = 90
				XSpeed = ballSpeed*math.cos(math.radians(Angle))
				YSpeed = ballSpeed*math.sin(math.radians(Angle))
			elif YDiff == 0:
				if XDiff < 0:
					Angle = 0
				else:
					Angle = 180
				XSpeed = ballSpeed*math.cos(math.radians(Angle))
				YSpeed = ballSpeed*math.sin(math.radians(Angle))
			x_v = (XSpeed * bounceCoefficientPlayer) + (p1_x_v * 0.15)
			y_v = (YSpeed * bounceCoefficientPlayer) + (p1_y_v * 0.15)

		# Handle Player2 collision with ball
		if math.sqrt( ((x - p2_x) ** 2) + ((y - p2_y) ** 2) ) <= (ballRadius + playerRadius):
			ballSpeed = math.sqrt((x_v ** 2)+(y_v ** 2))
			XDiff = -(x - p2_x)
			YDiff = -(y - p2_y)
			if XDiff > 0:
				if YDiff > 0:
					Angle = math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
				elif YDiff < 0:
					Angle = math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
			elif XDiff < 0:
				if YDiff > 0:
					Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
				elif YDiff < 0:
					Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
			elif XDiff == 0:
				if YDiff > 0:
					Angle = -90
				else:
					Angle = 90
				XSpeed = ballSpeed*math.cos(math.radians(Angle))
				YSpeed = ballSpeed*math.sin(math.radians(Angle))
			elif YDiff == 0:
				if XDiff < 0:
					Angle = 0
				else:
					Angle = 180
				XSpeed = ballSpeed*math.cos(math.radians(Angle))
				YSpeed = ballSpeed*math.sin(math.radians(Angle))
			x_v = (XSpeed * bounceCoefficientPlayer) + (p2_x_v * 0.15)
			y_v = (YSpeed * bounceCoefficientPlayer) + (p2_y_v * 0.15)

		## Handle ball collision with net

		# Ball contacts top of net
		topNet_x = winWidth / 2
		topNet_y = winHeight - netHeight + (netWidth / 2)
		if math.sqrt( ((x - topNet_x) ** 2) + ((y - topNet_y) ** 2) ) <= (ballRadius + (netWidth / 2)):
			ballSpeed = math.sqrt((x_v ** 2)+(y_v ** 2))
			XDiff = -(x - topNet_x)
			YDiff = -(y - topNet_y)
			if XDiff > 0:
				if YDiff > 0:
					Angle = math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
				elif YDiff < 0:
					Angle = math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
			elif XDiff < 0:
				if YDiff > 0:
					Angle = 180 + math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
				elif YDiff < 0:
					Angle = -180 + math.degrees(math.atan(YDiff/XDiff))
					XSpeed = -ballSpeed*math.cos(math.radians(Angle))
					YSpeed = -ballSpeed*math.sin(math.radians(Angle))
			elif XDiff == 0:
				if YDiff > 0:
					Angle = -90
				else:
					Angle = 90
				XSpeed = ballSpeed*math.cos(math.radians(Angle))
				YSpeed = ballSpeed*math.sin(math.radians(Angle))
			elif YDiff == 0:
				if XDiff < 0:
					Angle = 0
				else:
					Angle = 180
				XSpeed = ballSpeed*math.cos(math.radians(Angle))
				YSpeed = ballSpeed*math.sin(math.radians(Angle))
			x_v = XSpeed * bounceCoefficientNet
			y_v = YSpeed * bounceCoefficientNet
		
		pygame.display.update()

	pygame.quit()
	
playGame()