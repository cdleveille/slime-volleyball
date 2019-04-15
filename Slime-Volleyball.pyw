import os, pygame
from Game import Game
from Player import Player
from Ball import Ball
from xinput import *

## Configure and start a new game
def main():
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.init()
	winWidth = 1200
	winHeight = 600
	backgroundColor = pygame.color.Color("lightblue")
	backgroundImage = None
	framerate = 144 # frames per second
	gravity = 0.1 # change in vertical speed per frame (acts on ball and players)
	bounceCoefficient = 0.98
	bounceCoefficientPlayer = 0.98
	bounceCoefficientNet = 0.75
	playerToBallMomentumTransfer = 0.12 # percentage of a player's velocity that gets transferred to the ball on contact
	playerToBallHorizontalBoost = 1.03 # extra boost to the x-velocity of the ball on contact with player
	netHeight = 100
	netWidth = 20
	netColor = pygame.color.Color("black")
	insultsEnabled = False
	fourPlayer = False

	playerSpeed = 5 # maximum change in position (# pixels) per frame
	playerAccel = 5 # change in velocity per frame
	playerJump = 5 # immediate upward velocity (pixels per frame) on jump
	playerRadius = 56
	ballRadius = 24
	ballColor = pygame.color.Color("darkgreen")

	# Set up XInput devices
	p1XInput = None
	p2XInput = None
	p3XInput = None
	p4XInput = None
	p1Message = "[W A S D]"
	p2Message = "[Arrow Keys]"
	p3Message = "[T F G H]"
	p4Message = "[I J K L]"
	controllers = XInputJoystick.enumerate_devices()
	if len(controllers) > 0:
		p1XInput = controllers[0]
		p1Message = "[Controller 1]"
	if len(controllers) > 1:
		p2XInput = controllers[1]
		p1Message = "[Controller 2]"
	if len(controllers) > 2:
		p3XInput = controllers[2]
		p1Message = "[Controller 3]"
	if len(controllers) > 3:
		p4XInput = controllers[3]
		p1Message = "[Controller 4]"

	if playerRadius == ballRadius * 2:
		playerRadius += 1

	p1 = Player("Blue", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("darkblue"), 
		[pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s], p1XInput, p1Message)
	p2 = Player("Red", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("darkred"), 
		[pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN], p2XInput, p2Message)
	p3 = Player("Pink", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("purple"), 
		[pygame.K_t, pygame.K_f, pygame.K_h, pygame.K_g], p3XInput, p3Message)
	p4 = Player("Yellow", playerRadius, playerSpeed, playerAccel, playerJump, pygame.color.Color("orange"), 
		[pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k], p4XInput, p4Message)

	# 1v1
	team1 = [p1] # controls: [W, A, D]
	team2 = [p2] # controls: [UP, LEFT, RIGHT]

	# 2v2
	if fourPlayer == True:
		team1.append(p3) # controls: [T, F, H]
		team2.append(p4) # controls: [I, J, L]

	ball = Ball(ballRadius, ballColor)

	game = Game(winWidth, winHeight, backgroundColor, backgroundImage, framerate, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
				playerToBallMomentumTransfer, playerToBallHorizontalBoost, insultsEnabled, netHeight, netWidth, netColor, team1, team2, ball)

	game.startGame()

if __name__ == "__main__":
	main()