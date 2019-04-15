## Chris Leveille
## April 2019

import configparser, os, pygame
from Game import Game
from Player import Player
from Ball import Ball
from xinput import *

## Read config file and start a new game
def main():
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.init()

	config = configparser.ConfigParser(allow_no_value = True)
	config.read('settings.ini')

	winWidth = config.getint('Settings', 'winWidth')
	winHeight = config.getint('Settings', 'winHeight')
	backgroundColor = pygame.color.Color(config['Settings']['backgroundColor'])
	backgroundImage = config['Settings']['backgroundImage']
	framerate = config.getint('Settings', 'framerate') # frames per second
	gravity = config.getfloat('Settings', 'gravity') # change in vertical speed per frame (acts on ball and players)
	bounceCoefficient = config.getfloat('Settings', 'bounceCoefficient')
	bounceCoefficientPlayer = config.getfloat('Settings', 'bounceCoefficientPlayer')
	bounceCoefficientNet = config.getfloat('Settings', 'bounceCoefficientNet')
	playerToBallMomentumTransfer = config.getfloat('Settings', 'playerToBallMomentumTransfer') # percentage of a player's velocity that gets transferred to the ball on contact
	playerToBallHorizontalBoost = config.getfloat('Settings', 'playerToBallHorizontalBoost') # extra boost to the x-velocity of the ball on contact with player
	netHeight = config.getint('Settings', 'netHeight')
	netWidth = config.getint('Settings', 'netWidth')
	netColor = pygame.color.Color(config['Settings']['netColor'])
	insultsEnabled = config.getboolean('Settings', 'insultsEnabled')
	fourPlayer = config.getboolean('Settings', 'fourPlayer')

	playerSpeed = config.getint('Settings', 'playerSpeed') # maximum change in position (# pixels) per frame
	playerAccel = config.getint('Settings', 'playerAccel') # change in velocity per frame
	playerJump = config.getint('Settings', 'playerJump') # immediate upward velocity (pixels per frame) on jump
	playerRadius = config.getint('Settings', 'playerRadius')
	ballRadius = config.getint('Settings', 'ballRadius')
	ballColor = pygame.color.Color(config['Settings']['ballColor'])

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
	team1 = [p1] # controls: [W A S D]
	team2 = [p2] # controls: [Arrow Keys]

	# 2v2
	if fourPlayer == True:
		team1.append(p3) # controls: [T F G H]
		team2.append(p4) # controls: [I J K L]

	ball = Ball(ballRadius, ballColor)

	game = Game(winWidth, winHeight, backgroundColor, backgroundImage, framerate, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
				playerToBallMomentumTransfer, playerToBallHorizontalBoost, insultsEnabled, netHeight, netWidth, netColor, team1, team2, ball)

	game.startGame()

if __name__ == "__main__":
	main()