"""
http://stackoverflow.com/a/15459868/190597 (unutbu)
Based on http://www.pygame.org/docs/tut/intro/intro.html
Draws a red ball bouncing around in the window.
Pressing the arrow keys moves the ball
"""

import sys
import pygame
import os

delta = {
    pygame.K_LEFT: (-10, 0),
    pygame.K_RIGHT: (+10, 0),
    pygame.K_UP: (0, -10),
    pygame.K_DOWN: (0, +10),  
    }

gravity = +1

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load('C:\\Users\\Chris\\source\\repos\\Slime Volleyball\\ball.png')
        self.rect = self.image.get_rect()
        self.speed = [0, 0]
        area = pygame.display.get_surface().get_rect()
        self.width, self.height = area.width, area.height

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > self.width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > self.height:
            self.speed[1] = -self.speed[1]
        self.rect.left = clip(self.rect.left, 0, self.width)
        self.rect.right = clip(self.rect.right, 0, self.width)        
        self.rect.top = clip(self.rect.top, 0, self.height)
        self.rect.bottom = clip(self.rect.bottom, 0, self.height)                

def clip(val, minval, maxval):
    return min(max(val, minval), maxval)

class Main(object):
    def __init__(self):
        self.setup()
    def setup(self):
        pygame.init()
        size = (self.width, self.height) = (640,360)
        self.screen = pygame.display.set_mode(size, 0, 32)
        self.ball = Ball()
        self.setup_background()
    def setup_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.ball.image, self.ball.rect)
        pygame.display.flip()
    def event_loop(self):
        ball = self.ball
        friction = 1
        while True:
            for event in pygame.event.get():
                if ((event.type == pygame.QUIT) or 
                    (event.type == pygame.KEYDOWN and 
                     event.key == pygame.K_ESCAPE)):
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    deltax, deltay = delta.get(event.key, (0, 0))
                    ball.speed[0] += deltax
                    ball.speed[1] += deltay
                    friction = 1
                elif event.type == pygame.KEYUP:
                    friction = 0.99

            ball.speed = [friction*s for s in ball.speed]
            ball.speed[1] += gravity
            ball.update()
            self.draw()
            pygame.time.delay(10)

if __name__ == '__main__':
    app = Main()
    app.event_loop()