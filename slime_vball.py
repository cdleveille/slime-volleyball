import pygame
import math

def playGame():
	pygame.init()

	# Initialize game window
	winWidth = 1000
	winHeight = 500
	gameWin = pygame.display.set_mode((winWidth, winHeight))

	# Initialize game objects
	x = winWidth / 4
	y = winHeight / 2
	x_v = 0
	y_v = 0
	y_a = 0.18
	bounceCoefficient = -0.97
	bounceCoefficientPlayer = 0.98
	ballRadius = 25

	p1_x = winWidth / 4
	p1_y = winHeight
	p1_x_v = 0
	p1_y_v = 0
	p1CanJump = True

	playerSpeed = 5
	playerJump = 7
	playerRadius= 50

	netWidth = 20
	netHeight = 100

	backgroundColor = pygame.color.Color("lightblue")
	ballColor = pygame.color.Color("black")
	netColor = pygame.color.Color("black")
	p1Color = pygame.color.Color("black")

	gameOn = True
	while(gameOn):

		# Control framerate
		pygame.time.delay(10)

		# Draw game objects
		gameWin.fill(backgroundColor)
		pygame.draw.circle(gameWin, p1Color, (int(p1_x), int(p1_y)), playerRadius)
		pygame.draw.rect(gameWin, backgroundColor, (p1_x - playerRadius, p1_y, playerRadius * 2, playerRadius))
		pygame.draw.circle(gameWin, ballColor, (int(x), int(y)), ballRadius)
		pygame.draw.rect(gameWin, netColor, (winWidth / 2 - (netWidth / 2), winHeight - netHeight, netWidth, netHeight))

		# Handle player input
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameOn = False
			elif event.type == pygame.KEYDOWN:
				if pygame.key.name(event.key) == "up" and p1CanJump:
					p1_y_v = -1 * playerJump
					p1CanJump = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
			p1_x_v = 0
		elif keys[pygame.K_LEFT]:
			p1_x_v = -1 * playerSpeed
		elif keys[pygame.K_RIGHT]:
			p1_x_v = playerSpeed
		else:
			p1_x_v = 0

		# Update ball position
		x += x_v
		y += y_v
		y_v += y_a
		if y >= (winHeight - ballRadius):
			y = winHeight - ballRadius
			y_v = bounceCoefficient * y_v
		if x - ballRadius < 0:
			x = ballRadius
			x_v = -1 * x_v
		elif x + ballRadius > winWidth:
			x = winWidth - ballRadius
			x_v = -1 * x_v

		# Update Player1 position
		p1_x += p1_x_v
		p1_y += p1_y_v
		if p1_y < winHeight:
			p1_y_v += y_a
		else:
			p1_y = winHeight
			p1CanJump = True
		if p1_x - playerRadius < 0:
			p1_x = playerRadius
		elif p1_x + playerRadius > winWidth / 2 - netWidth / 2:
			p1_x = winWidth / 2 - netWidth / 2 - playerRadius

		# Handle Player1 collision with ball
		if math.sqrt( ((x-p1_x)**2) + ((y-p1_y)**2) ) <= (ballRadius + playerRadius):
			ballSpeed = math.sqrt((x_v**2)+(y_v**2))
			XDiff = -(x-p1_x)
			YDiff = -(y-p1_y)
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
			x_v = XSpeed * bounceCoefficientPlayer
			y_v = YSpeed * bounceCoefficientPlayer

		
		pygame.display.update()

	pygame.quit()
	
playGame()