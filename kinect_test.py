from visual import *
from pykinect import nui
from pykinect.nui import JointId
import pykinect
import pygame
import random
import time

pygame.init()

pygame.key.set_repeat(1)

BLACK = (0,0,0)
WHITE = (255,255,255)

size = (1000, 300)
screen = pygame.display.set_mode(size)
FPS = 60
speed = 6.0
speed2 = 0.5

done = False

clock = pygame.time.Clock()

class moving_block(pygame.sprite.Sprite):
	
	def __init__(self, xpos):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load("counter1.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x = 0 - self.rect.width + xpos
		self.rect.y = 300 - self.rect.height

	def update_position(self):
		self.rect.x += 5
		
class moving_block2(pygame.sprite.Sprite):
	
	def __init__(self, xpos):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load("counter2.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x = 0 - self.rect.width
		self.rect.y = 300 - (self.rect.height * 2)

	def update_position(self):
		self.rect.x += 5
		
class player(pygame.sprite.Sprite):
	
	change_y = 0 
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.image.load("counter3.png").convert()
		self.rect = self.image.get_rect()
		self.rect.x = 750
		self.rect.y = 300 - 100
		
	def update_position(self):
		
		self.calculate_gravity()
		
		self.rect.y += self.change_y
		
		block_hit_list = pygame.sprite.spritecollide(self, sprites, False)
		
		if len(block_hit_list) >= 1:
			print("crap, you hit one!")
			
	def calculate_gravity(self):
		if self.change_y == 0: #if the player isn't falling or jumpng
			self.change_y = 1 #make them move down 1 (check)
		else:
			self.change_y += 0.20 #else if they're falling or jumping, add gravity 
			
		if self.rect.y >= 200 and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = 200
			
	def jump(self):
		self.rect.y += 2
		platform_hit_list = pygame.sprite.spritecollide(self, sprites, False)
		self.rect.y -= 2
		
		if len(platform_hit_list) > 0 or self.rect.bottom >= 250:
			self.change_y = -5
			
def jump_detect():

	for skeleton in _kinect.skeleton_engine.get_next_frame().SkeletonData:
		if skeleton.eTrackingState == nui.SkeletonTrackingState.TRACKED:
		
			print(skeleton.SkeletonPositions[3].y)

			if skeleton.SkeletonPositions[3].y < 0.15:
				print("You Ducked")
			
			if skeleton.SkeletonPositions[3].y > 0.5:
				print("You Jumped")
				player.jump()

score = 0
ticktock = 1	
		
sprites = pygame.sprite.Group()
sprites2 = pygame.sprite.Group()
player1 = pygame.sprite.Group()

_kinect = nui.Runtime()
_kinect.skeleton_engine.enabled = True
_kinect.camera.elevation_angle = 15

player1.add(player())

for i in range(21):		
	sprites.add(moving_block(50*i))
		
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player.jump()
				
	screen.fill(BLACK)
		
	if ticktock % (FPS/speed) == 1:
		sprites.add(moving_block(0))
		jump_detect()
		
	if ticktock % (FPS/speed2) == 1:
		sprites2.add(moving_block2(0))

	for sprite in sprites:
		if sprite.rect.x > 1000:
			sprite.kill()
			
		sprite.update_position()
		
	for sprite in sprites2:
		if sprite.rect.x > 1000:
			score += 10
			print(score)
			sprite.kill()
			
		sprite.update_position()
	
	for player in player1:	
		player.update_position()

	sprites.draw(screen)
	sprites2.draw(screen)
	player1.draw(screen)
	
	
	pygame.display.flip()
	
	ticktock += 1
		
	clock.tick(FPS)