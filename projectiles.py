import math
import pygame
from particles import Explosion

WIDTH, HEIGHT =640, 484

pygame.mixer.init()
grenade_blast_fx = pygame.mixer.Sound(f'./Sounds/grenade blast.wav')
grenade_blast_fx.set_volume(0.6)

gun_fx =  pygame.mixer.Sound(f'./Sounds/bullet.wav')
gun_fx.set_volume(0.6)
sword1_fx = pygame.mixer.Sound(f'./Sounds/sword1.wav')
sword1_fx.set_volume(0.6)
sword2_fx = pygame.mixer.Sound(f'./Sounds/sword2.mp3')
sword2_fx.set_volume(0.6)
fireball_fx = pygame.mixer.Sound(f'./Sounds/fireball.ogg')
fireball_fx.set_volume(0.6)
knight_fx = pygame.mixer.Sound(f'./Sounds/knight.mp3')
knight_fx.set_volume(0.6)
arrow1_fx = pygame.mixer.Sound(f'./Sounds/arrow1.ogg')
arrow1_fx.set_volume(0.6)
arrow2_fx = pygame.mixer.Sound(f'./Sounds/arrow2.mp3')
arrow2_fx.set_volume(0.6)

class Gun(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, type_, win, ):
		super(Gun, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.color = (240, 240, 240)
		self.type = type_
		self.win = win

		if self.type == 2:
			self.color = (160, 160, 160)

		self.dame = 21
		self.crit = 1 # add after

		self.speed = 10
		self.radius = 4
		gun_fx.play()
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)
		self.start_x = x

	def update(self, screen_scroll, world):
		if self.direction == -1:
			self.x -= self.speed + screen_scroll
		if self.direction == 0 or self.direction == 1:
			self.x += self.speed + screen_scroll

		if world != None:
			for tile in world.ground_list:
				if tile[1].collidepoint(self.x, self.y):
					self.kill()
			for tile in world.rock_list:
				if tile[1].collidepoint(self.x, self.y):
					self.kill()
		if abs(self.start_x - self.x) > WIDTH:
			self.kill()
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

class Fireball(pygame.sprite.Sprite): 
	def __init__(self, x, y, direction, type_, win) :
		super(Fireball, self).__init__()
		self.direction = direction
		self.type = type_
		self.speed = 4
		self.win = win
		self.image = pygame.image.load(f'Assets/Fireball.png')
		self.rect = self.image.get_rect(center=(x, y))
		space_x = self.rect.width//2 * direction
		self.x = x  + space_x
		self.y = y 
		self.dame = 34
		self.crit = 10
		if self.direction == -1: 
			self.image = pygame.transform.flip(self.image, True, False) 
		fireball_fx.play()
		self.time_start = pygame.time.get_ticks()

	def update(self, screen_scroll, world):
		if self.direction == -1:
			self.x -= self.speed + screen_scroll
			
		if self.direction == 0 or self.direction == 1:
			self.x += self.speed + screen_scroll
		self.rect.x = self.x
		for tile in world.ground_list:
			if tile[1].collidepoint(self.rect.x, self.rect.y):
				fireball_fx.stop()
				self.kill()
		for tile in world.rock_list:
			if tile[1].collidepoint(self.rect.x, self.rect.y):
				fireball_fx.stop()
				self.kill() 
		if pygame.time.get_ticks() - self.time_start >= 950:
			fireball_fx.stop()
			self.kill()
		self.win.blit(self.image, (self.x -self.rect.width//2, self.y-self.rect.height//2))
		
class Sword(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, type_, win, skill1=True):
		super(Sword, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.color = (240, 240, 240,0)
		self.type = type_
		self.win = win
		self.dame = 50
		self.speed = 2
		self.radius = 4
		self.time_start = pygame.time.get_ticks()
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)
		self.skill1 = skill1
		if skill1:
			sword1_fx.play()
		else:
			sword2_fx.play()

	def update(self, screen_scroll, world):
		if pygame.time.get_ticks() - self.time_start <= 400 and not self.skill1:
			return
		# if not self.skill1:
		# 	print(pygame.time.get_ticks() - self.time_start)
		if self.direction == -1:
			self.x -= self.speed + screen_scroll
		if self.direction == 0 or self.direction == 1:
			self.x += self.speed + screen_scroll

		for tile in world.ground_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()
		for tile in world.rock_list:
			if tile[1].collidepoint(self.x, self.y):
				self.kill()
		time_step = 100 if self.skill1 else 421
		if pygame.time.get_ticks() - self.time_start >= time_step:
			self.kill()
		self.rect = pygame.draw.circle(self.win, self.color, (self.x, self.y), self.radius)

class Lance(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, type_, win_, p):
		super(Lance, self).__init__()
		self.p = p
		self.color =(0,0,0,0)
		self.radius = 4
		self.win = win_
		self.dame = 34
		self.type = type_
		self.rect = p.rect
		if p.state_direction == 'right':
			self.rect = pygame.Rect(p.rect.right-2,p.rect.centery-2, 4, 4)
		else:
			self.rect = pygame.Rect(p.rect.left-2, p.rect.centery-2, 4, 4)
		knight_fx.play()

	def update(self, screen_scroll, world):
		if self.p.attack == False:
			self.kill()
		if self.p.state_direction == 'right':
			self.rect = pygame.Rect(self.p.rect.right-2, self.p.rect.centery-2, 4, 4)
		else:
			self.rect = pygame.Rect(self.p.rect.left-2, self.p.rect.centery-2, 4, 4)

class Arrow(pygame.sprite.Sprite): 
	def __init__(self, x, y, direction, type_, win, p) :
		super(Arrow, self).__init__()
		self.type = type_
		self.speed = 7
		self.win = win
		self.image = pygame.image.load(f'Assets/Arrow.png')
		self.rect = self.image.get_rect(center=(x, y))
		self.dame = 50
		self.crit = 10
		self.p = p
		self.start = False
		arrow1_fx.play()
		

	def update(self, screen_scroll, world):
		if self.p.attack_index == 5 and self.start == False: 
			self.start = True
			self.direction = 1 if self.p.state_direction == 'right' else -1 
			x,y = self.p.rect.center
			self.rect = self.image.get_rect(center=(x, y))
			if self.direction == -1: 
				self.image = pygame.transform.flip(self.image, True, False) 
			self.x = x  + self.rect.width//2 * self.direction
			self.y = y
			arrow2_fx.play()
		if self.start == False:
			return

		if self.direction == -1:
			self.x -= self.speed + screen_scroll
			
		if self.direction == 0 or self.direction == 1:
			self.x += self.speed + screen_scroll

		self.rect.x = self.x
		for tile in world.ground_list:
			if tile[1].collidepoint(self.rect.x, self.rect.y):
				self.kill()
		for tile in world.rock_list:
			if tile[1].collidepoint(self.rect.x, self.rect.y):
				self.kill() 

		self.win.blit(self.image, (self.x -self.rect.width//2, self.y-self.rect.height//2))

class Grenade(pygame.sprite.Sprite):
	def __init__(self, x, y, direction, win):
		super(Grenade, self).__init__()

		self.x = x
		self.y = y
		self.direction = direction
		self.win = win

		self.speed = 10
		self.vel_y = -11
		self.timer = 15
		self.radius = 4

		if self.direction == 0:
			self.direction = 1

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius+1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)

	def update(self, screen_scroll, p, enemy_group, explosion_group, world):
		self.vel_y += 1
		dx = self.direction * self.speed
		dy = self.vel_y

		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y, self.rect.width, self.rect.height):
				if self.rect.y <= tile[1].y:
					dy = 0
					self.speed -= 1
					if self.speed <= 0:
						self.speed = 0

		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
				self.direction *= -1
				dx = self.direction * self.speed
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
				if self.rect.y <= tile[1].y:
					dy = 0
					self.speed -= 1
					if self.speed <= 0:
						self.speed = 0

		if self.rect.y > WIDTH:
			self.kill()

		if self.speed == 0:
			self.timer -= 1
			if self.timer <= 0:
				grenade_blast_fx.play()
				for _ in range(30):
					explosion = Explosion(self.x, self.y, self.win)
					explosion_group.add(explosion)

				p_distance = math.sqrt((p.rect.centerx - self.x) ** 2 + (p.rect.centery - self.y) ** 2 )
				if p_distance <= 100:
					if p_distance > 80:
						p.health -= 20
					elif p_distance > 40:
						p.health -= 50
					elif p_distance >= 0:
						p.health -= 80
					p.hit = True

				for e in enemy_group:
					e_distance = math.sqrt((e.rect.centerx - self.x) ** 2 + (e.rect.centery - self.y) ** 2)
					if e_distance < 80:
						e.health -= 100

				self.kill()
 
		self.x += dx + screen_scroll
		self.y += dy

		pygame.draw.circle(self.win, (200, 200, 200), (self.x, self.y), self.radius+1)
		self.rect = pygame.draw.circle(self.win, (255, 50, 50), (self.x, self.y), self.radius)
		pygame.draw.circle(self.win, (0, 0, 0), (self.x, self.y), 1)