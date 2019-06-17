## Chris Leveille
## April 2019

import pygame, pygame.gfxdraw, math
from AI import AI
from PIL import Image, ImageDraw

class Player():

	## Create new player
	def __init__(self, name, radius, speed, accel, jump, color, keyInputs, messages, isAI):
		
		self.x = 0
		self.y = 0
		self.xv = 0
		self.yv = 0
		self.powerX = 0
		self.powerY = 0
		self.powerWidth = 120
		self.powerPct = 0.00
		self.powerActive = False
		self.color = color
		self.name = name
		self.radius = radius
		self.normalRadius = radius
		self.speed = speed
		self.accel = accel
		self.jump = jump
		self.jumpEnabled = True
		self.alwaysJump = False
		self.eyeX = self.radius / 2
		self.eyeY = self.radius * (3 / 5)
		self.pupilOffsetRatio = self.radius / 10
		self.messages = messages
		self.displayMessage = messages[0]
		self.messageFont = pygame.font.Font(None, 24)
		self.messageStartFrame = 0
		self.pillow = self.initPlayerPillowBody()
		self.frameMarker = 0
		self.jumpInput = keyInputs[0]
		self.leftInput = keyInputs[1]
		self.rightInput = keyInputs[2]
		self.slowInput = keyInputs[3]
		self.power1Input = keyInputs[4]
		self.power2Input = keyInputs[5]
		self.xinput = None
		self.isAI = isAI
		self.AI = AI()

	def getPlayerAction(self, keys, currentFrame, game):

		if self.isAI == False:
			self.handleInput(keys, currentFrame)
		else:
			self.getAIAction(game)

		self.enforceMaxSpeed()

	## Update movement properties based on the immediate inputs
	def handleInput(self, keys, currentFrame):

		# Get XInput device input
		if self.xinput is not None:
			self.pollForXInput(currentFrame)

		# Handle keyboard input
		else:
			if keys[self.leftInput] and keys[self.rightInput]:
				if self.xv < 0:
					self.xv += self.accel
					if self.xv > 0:
						self.xv = 0
				elif self.xv > 0:
					self.xv -= self.accel
					if self.xv < 0:
						self.xv = 0
			elif keys[self.leftInput]:
				self.xv -= self.accel
			elif keys[self.rightInput]:
				self.xv += self.accel
			else:
				if self.xv < 0:
					self.xv += self.accel
					if self.xv > 0:
						self.xv = 0
				elif self.xv > 0:
					self.xv -= self.accel
					if self.xv < 0:
						self.xv = 0

			if keys[self.jumpInput] and (self.jumpEnabled == True or self.alwaysJump == True):
				self.yv = -self.jump
				self.jumpEnabled = False

			if keys[self.power1Input] and self.powerPct == 1.0 and self.powerActive == False:
				self.powerActive = True
				self.activatePower1()

			if keys[self.power2Input] and self.powerPct == 1.0 and self.powerActive == False:
				self.powerActive = True
				self.activatePower2()

			# Halve the player's horizontal velocity if the 'slow' input is used
			if keys[self.slowInput]:
				self.xv = self.xv / 2

	## Enforce the player's maximum horizontal speed
	def enforceMaxSpeed(self):

		if abs(self.xv) > self.speed:
			self.xv = self.speed * (self.xv / abs(self.xv))

	## Handle XInput device input
	def pollForXInput(self, currentFrame):

		# Poll the controller for input
		stickPct = self.xinput.pollLeftStick(0.1)
		jump = self.xinput.pollButton(3)
		power1 = self.xinput.pollButton(1)
		power2 = self.xinput.pollButton(2)

		# Disconnect the controller if it does not have a pulse
		if None in [stickPct, jump, power1, power2]:
			self.xinput = None
			self.displayMessage = self.messages[0]
			self.messageStartFrame = currentFrame
			return

		if stickPct > 0:
			self.xv += self.accel
		elif stickPct < 0:
			self.xv -= self.accel
		else:
			if self.xv < 0:
				self.xv += self.accel
				if self.xv > 0:
					self.xv = 0
			elif self.xv > 0:
				self.xv -= self.accel
				if self.xv < 0:
					self.xv = 0
		
		if jump == 1 and (self.jumpEnabled == True or self.alwaysJump == True):
			self.yv = -self.jump
			self.jumpEnabled = False

		if power1 == 1 and self.powerPct == 1.0 and self.powerActive == False:
			self.activatePower1()

		if power2 == 1 and self.powerPct == 1.0 and self.powerActive == False:
			self.activatePower2()

		# Enforce the player's maximum horizontal speed (based on how far the stick is tilted)
		if abs(self.xv) > abs(self.speed * stickPct):
			self.xv = abs(self.speed * stickPct) * (self.xv / abs(self.xv))


	def getAIAction(self, game):

		ballLandX = self.AI.predictBallLandingPosition(game)

		# Player on Team 1
		if self.x < game.winWidth / 2:
			if ballLandX < game.winWidth:
				a = 1 #go to where ball will land
			else:
				if self.x < game.winWidth / 4:
					self.xv += self.accel
				elif self.x > game.winWidth / 4:
					self.xv -= self.accel

				if abs(self.x - game.winWidth / 4) < self.speed:
					self.xv = 0
		# Player on Team 2
		else:
			if ballLandX > game.winWidth:
				a = 1 #go to where ball will land
			else:
				if self.x < game.winWidth  * (3 / 4):
					self.xv += self.accel
				elif self.x > game.winWidth * (3 / 4):
					self.xv -= self.accel

				if abs(self.x - game.winWidth * (3 / 4)) < self.speed:
					self.xv = 0

	## Initialize XInput controller device
	def setXInput(self, device, messageStartFrame):

		self.xinput = device
		self.displayMessage = self.messages[1]
		self.messageStartFrame = messageStartFrame

	## Calculate the amount to shift the pupil from the center of the eye based on the location of the ball
	def getPupilOffset(self, ball, pupilX):
		
		(pupilShiftX, pupilShiftY) = (0, 0)
		XDiff = -(ball.x - (self.x + pupilX))
		YDiff = -(ball.y - (self.y - self.radius / 2))
		if XDiff > 0:
			if YDiff > 0:
				Angle = math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif XDiff < 0:
			if YDiff > 0:
				Angle = 180 + math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
			elif YDiff < 0:
				Angle = -180 + math.degrees(math.atan(YDiff / XDiff))
				pupilShiftX = -self.pupilOffsetRatio * math.cos(math.radians(Angle))
				pupilShiftY = -self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif XDiff == 0:
			if YDiff > 0:
				Angle = -90
			else:
				Angle = 90
			pupilShiftX = self.pupilOffsetRatio * math.cos(math.radians(Angle))
			pupilShiftY = self.pupilOffsetRatio * math.sin(math.radians(Angle))
		elif YDiff == 0:
			if XDiff < 0:
				Angle = 0
			else:
				Angle = 180
			pupilShiftX = self.pupilOffsetRatio * math.cos(math.radians(Angle))
			pupilShiftY = self.pupilOffsetRatio * math.sin(math.radians(Angle))
		return (pupilShiftX, pupilShiftY)

	## Update position properties given a gravity value
	def updatePosition(self, gravity):
		
		self.yv += gravity
		self.x += self.xv
		self.y += self.yv

	## Initialize the Pillow semi-circle used for the player's body
	def initPlayerPillowBody(self):

		pil_size = self.radius * 2
		pil_image = Image.new("RGBA", (pil_size, pil_size))
		pil_draw = ImageDraw.Draw(pil_image)
		pil_draw.pieslice((0, 0, pil_size, pil_size), 180, 0, fill = (self.color.r, self.color.g, self.color.b))
		return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)

	## Add the given amount to the player's power bar percentage
	def incrementPowerPct(self, amt):

		self.powerPct += amt
		if self.powerPct > 1.0:
			self.powerPct = 1.0
		if self.powerPct <= 0.0:
			self.powerPct = 0.0
			self.deactivatePowers()

	## Make the player 50% bigger
	def activatePower1(self):
		
		self.powerActive = True
		self.radius = int(self.radius * (3 / 2))
		self.pillow = self.initPlayerPillowBody()

	## Allow the player to jump at all times
	def activatePower2(self):

		self.powerActive = True
		self.alwaysJump = True

	## Return the player to its original state
	def deactivatePowers(self):

		self.powerActive = False
		self.radius = self.normalRadius
		self.pillow = self.initPlayerPillowBody()
		self.jumpEnabled = False
		self.alwaysJump = False

	## Draw the player
	def draw(self, gameWin, backgroundColor, ball, pillowDrawInd, drawMessage, drawPowerBarOutline):
		
		if (pillowDrawInd == True):
			self.drawBodyPillow(gameWin)
		else:
			self.drawBody(gameWin, backgroundColor)
		self.drawEye(gameWin, ball)

		if drawMessage == True:
			self.drawMessage(gameWin)

		self.drawPowerBar(gameWin, drawPowerBarOutline)

	## Draw the player's body (anti-aliased and more resource efficient, but draws rectangle hiding bottom of player)
	def drawBody(self, gameWin, backgroundColor):

		self.drawAACircle(gameWin, int(self.x), int(self.y), int(self.radius), self.color)
		pygame.draw.rect(gameWin, backgroundColor, (self.x - self.radius, self.y, self.radius * 2 + 1, self.radius + 1))
		pygame.gfxdraw.line(gameWin, int(self.x - self.radius), int(self.y), int(self.x + self.radius), int(self.y), pygame.color.Color("black"))

	## Draw the player's body (does not draw rectangle hiding bottom of player, but is more resource intensive)
	def drawBodyPillow(self, gameWin):
		
		image_rect = self.pillow.get_rect(center = (self.x, self.y))
		gameWin.blit(self.pillow, image_rect)
		pygame.gfxdraw.arc(gameWin, int(self.x), int(self.y), int(self.radius), 180, 360, pygame.color.Color("black"))
		pygame.gfxdraw.line(gameWin, int(self.x - self.radius), int(self.y), int(self.x + self.radius), int(self.y), pygame.color.Color("black"))

	## Draw the player's eye
	def drawEye(self, gameWin, ball):
		
		# If the ball contacts the ground on this player's side, widen the white of his eye
		if ball.y + ball.radius >= pygame.display.get_surface().get_height():
			if self.x < pygame.display.get_surface().get_width() / 2 and ball.x < pygame.display.get_surface().get_width() / 2:
				eyeRadius = self.radius / 3
			elif self.x > pygame.display.get_surface().get_width() / 2 and ball.x > pygame.display.get_surface().get_width() / 2:
				eyeRadius = self.radius / 3
			else:
				eyeRadius = self.radius / 4
		else:
			eyeRadius = self.radius / 4

		self.eyeX = self.radius / 2
		self.eyeY = self.radius * (3 / 5)
		self.pupilOffsetRatio = self.radius / 10

		if (self.x < pygame.display.get_surface().get_width() / 2):
			self.drawAACircle(gameWin, int(self.x + self.eyeX), int(self.y - self.eyeY), int(eyeRadius), pygame.color.Color("lightgray"))
		else:
			self.drawAACircle(gameWin, int(self.x - self.eyeX), int(self.y - self.eyeY), int(eyeRadius), pygame.color.Color("lightgray"))
		
		self.drawPupil(gameWin, ball)

	## Draw the pupil within the player's eye
	def drawPupil(self, gameWin, ball):
		
		# Draw the pupil so it is tracking the ball's location
		if self.x < pygame.display.get_surface().get_width() / 2:
			(pupilOffsetX, pupilOffsetY) = self.getPupilOffset(ball, self.eyeX)
		else:
			(pupilOffsetX, pupilOffsetY) = self.getPupilOffset(ball, -self.eyeX)

		if (self.x < pygame.display.get_surface().get_width() / 2):
			self.drawAACircle(gameWin, int(self.x + self.eyeX + pupilOffsetX), int(self.y - self.eyeY + pupilOffsetY), int(self.radius / 8), pygame.color.Color("black"))
		else:
			self.drawAACircle(gameWin, int(self.x - self.eyeX + pupilOffsetX), int(self.y - self.eyeY + pupilOffsetY), int(self.radius / 8), pygame.color.Color("black"))

	## Draw the message shown above the player
	def drawMessage(self, gameWin):
		
		messageLabel = self.messageFont.render(self.displayMessage, True, pygame.color.Color("black"))
		messageLabelRect = messageLabel.get_rect(center = (self.x, self.y - self.radius - 20))
		gameWin.blit(messageLabel, messageLabelRect)

	## Draw a circle with smooth edges using anti-aliasing
	def drawAACircle(self, gameWin, x, y, r, color):
		
		pygame.gfxdraw.filled_circle(gameWin, int(x), int(y), int(r), color)
		pygame.gfxdraw.aacircle(gameWin, int(x), int(y), int(r), pygame.color.Color("black"))

	## Draw the player's power bar at the top of the screen
	def drawPowerBar(self, gameWin, drawPowerBarOutline):

		pygame.draw.rect(gameWin, pygame.color.Color("lightgray"), [self.powerX, self.powerY, self.powerWidth, 12])
		pygame.draw.rect(gameWin, pygame.color.Color("black"), [self.powerX, self.powerY, self.powerWidth, 12], 1)
		if self.powerPct > 0:
			pygame.draw.rect(gameWin, self.color, [self.powerX + 1, self.powerY + 1, int(self.powerPct * (self.powerWidth - 2)), 10])
		if self.powerPct >= 1.0 and self.powerActive == False:
			self.powerPct = 1.0
			pygame.draw.rect(gameWin, pygame.color.Color("yellow"), [self.powerX - 3, self.powerY - 3, self.powerWidth + 6, 18], 3)
		elif drawPowerBarOutline == True and self.powerActive == True:
			pygame.draw.rect(gameWin, pygame.color.Color("yellow"), [self.powerX - 3, self.powerY - 3, self.powerWidth + 6, 18], 3)
