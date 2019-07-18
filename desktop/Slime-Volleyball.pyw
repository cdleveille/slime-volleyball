## Chris Leveille
## April 2019

import configparser, os, pygame
from Game import Game
from Player import Player
from Ball import Ball

## Read config file and start a new game
def main():

	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.init()

	config = configparser.ConfigParser(allow_no_value = True)
	config.read('settings.ini')

	fourPlayer = config.getboolean('Settings', 'fourPlayer')
	scoreLimit = config.getint('Settings', 'scoreLimit')
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

	playerSpeed = config.getint('Settings', 'playerSpeed') # maximum change in position (# pixels) per frame
	playerAccel = config.getint('Settings', 'playerAccel') # change in velocity per frame
	playerJump = config.getint('Settings', 'playerJump') # immediate upward velocity (pixels per frame) on jump
	playerRadius = config.getint('Settings', 'playerRadius')
	ballRadius = config.getint('Settings', 'ballRadius')
	ballColor = pygame.color.Color(config['Settings']['ballColor'])

	if playerRadius == ballRadius * 2:
		playerRadius += 1

	p1Name = config['Settings']['p1Name']
	p2Name = config['Settings']['p2Name']
	p3Name = config['Settings']['p3Name']
	p4Name = config['Settings']['p4Name']

	p1Color = pygame.color.Color(config['Settings']['p1Color'])
	p2Color = pygame.color.Color(config['Settings']['p2Color'])
	p3Color = pygame.color.Color(config['Settings']['p3Color'])
	p4Color = pygame.color.Color(config['Settings']['p4Color'])

	p1Keys = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s, pygame.K_q, pygame.K_e]
	p2Keys = [pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_RSHIFT, pygame.K_RCTRL]
	p3Keys = [pygame.K_t, pygame.K_f, pygame.K_h, pygame.K_g, pygame.K_r, pygame.K_y]
	p4Keys = [pygame.K_i, pygame.K_j, pygame.K_l, pygame.K_k, pygame.K_u, pygame.K_o]

	p1Messages = ["[W A S D]", "[Controller 1]"]
	p2Messages = ["[Arrow Keys]", "[Controller 2]"]
	p3Messages = ["[T F G H]", "[Controller 3]"]
	p4Messages = ["[I J K L]", "[Controller 4]"]

	p1IsAI = config.getboolean('Settings', 'p1IsAI')
	p2IsAI = config.getboolean('Settings', 'p2IsAI')
	p3IsAI = config.getboolean('Settings', 'p3IsAI')
	p4IsAI = config.getboolean('Settings', 'p4IsAI')

	p1 = Player(p1Name, playerRadius, playerSpeed, playerAccel, playerJump, p1Color, p1Keys, p1Messages, p1IsAI)
	p2 = Player(p2Name, playerRadius, playerSpeed, playerAccel, playerJump, p2Color, p2Keys, p2Messages, p2IsAI)
	p3 = Player(p3Name, playerRadius, playerSpeed, playerAccel, playerJump, p3Color, p3Keys, p3Messages, p3IsAI)
	p4 = Player(p4Name, playerRadius, playerSpeed, playerAccel, playerJump, p4Color, p4Keys, p4Messages, p4IsAI)

	# 1v1
	team1 = [p1] # controls: [W A S D]
	team2 = [p2] # controls: [Arrow Keys]

	# 2v2
	if fourPlayer == True:
		team1.append(p3) # controls: [T F G H]
		team2.append(p4) # controls: [I J K L]

	ball = Ball(ballRadius, ballColor)

	game = Game(scoreLimit, winWidth, winHeight, backgroundColor, backgroundImage, framerate, gravity, bounceCoefficient, bounceCoefficientPlayer, bounceCoefficientNet, 
				playerToBallMomentumTransfer, playerToBallHorizontalBoost, insultsEnabled, netHeight, netWidth, netColor, team1, team2, ball)

	game.startGame(True)

if __name__ == "__main__":
	main()