import pygame
WIDTH, HEIGHT =640, 484

class Snow(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Snow, self).__init__()
		self.x = x
		self.y = y
		self.lst_notice = []

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.revive = False
		self.size = 24
		path_img = './Assets/'+ str(self.__class__.__name__).title()
		
		for i in range(1,3):
			image = pygame.image.load(f'{path_img}/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,6):
			image = pygame.image.load(f'{path_img}/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'{path_img}/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1,11):
			image = pygame.image.load(f'{path_img}/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'{path_img}/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0
		self.state_direction = 'right'

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False
		self.above_ground = True
		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
				# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True
				# print(self.vel, dy)
				
		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					# self.jump = False
					# self.vel = self.jump_height
					self.vel = - self.vel
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True


		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
					self.revive = True
					self.death_index = 0
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.state_direction != 'right': # add
					self.image = pygame.transform.flip(self.image, True, False) # add
				# if self.direction == -1:
				# 	self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]

		if self.alive and len(self.lst_notice)>0:
			for i in range(len(self.lst_notice)):
				try:
					notice = self.lst_notice[i]
					if notice[3] > 0:
						notice[3] -= 10
						if notice[3] <= 150:
							notice[3] -= 5
						notice[2] -= 1
						notice[0].set_alpha(notice[3])
						self.win.blit(notice[0], (notice[1], notice[2]))
					else:
						self.lst_notice.pop(i)
						i-=1
				except:
					print('null')
					i-=1

	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.state_direction = 'left' # add 
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.state_direction = 'right' # add
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump :
			self.above_ground = False
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity
			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		if self.attack and not self.jump: # khi skill , đứng yên
			self.dx = 0
		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()
	
	def revival(self, x, y, health=100):
		self.rect = self.image.get_rect(center=(x, y))
		self.health = health
		self.revive = False
		self.alive = True
		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.attack = False
		
	def draw(self, win):
		win.blit(self.image, self.rect)
	
class Ignis(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Ignis, self).__init__()
		self.x = x
		self.y = y
		self.lst_notice = []

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.revive = False
		self.size = 24

		path_img = './Assets/'+ str(self.__class__.__name__).title()
		
		for i in range(1,3):
			image = pygame.image.load(f'{path_img}/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,6):
			image = pygame.image.load(f'{path_img}/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'{path_img}/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1,11):
			image = pygame.image.load(f'{path_img}/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'{path_img}/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0
		self.state_direction = 'right'

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False
		self.above_ground = True
		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
				# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True
				# print(self.vel, dy)
				
		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					# self.jump = False
					# self.vel = self.jump_height
					self.vel = - self.vel
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True


		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
					self.revive = True
					self.death_index = 0
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.state_direction != 'right': # add
					self.image = pygame.transform.flip(self.image, True, False) # add
				# if self.direction == -1:
				# 	self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]

		if self.alive and len(self.lst_notice)>0:
			for i in range(len(self.lst_notice)):
				try:
					notice = self.lst_notice[i]
					if notice[3] > 0:
						notice[3] -= 10
						if notice[3] <= 150:
							notice[3] -= 5
						notice[2] -= 1
						notice[0].set_alpha(notice[3])
						self.win.blit(notice[0], (notice[1], notice[2]))
					else:
						self.lst_notice.pop(i)
						i-=1
				except:
					print('null')
					i-=1


	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.state_direction = 'left' # add 
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.state_direction = 'right' # add
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump :
			self.above_ground = False
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity
			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		if self.attack and not self.jump: # khi skill , đứng yên
			self.dx = 0
		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()
	
	def revival(self, x, y, health=100):
		self.rect = self.image.get_rect(center=(x, y))
		self.health = health
		self.revive = False
		self.alive = True
		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.attack = False
		
		
	def draw(self, win):
		win.blit(self.image, self.rect)
	
	def add_notice(self, notice, type, win):
		if not hasattr(self,'win'):
			self.win = win
		notice_text = pygame.font.Font(None, 20).render(notice, True, (255,0,0) if type==2 else (0,255,0))
		notice_text_x = self.rect.x + 20
		notice_text_y = self.rect.y - 20
		notice_text_time = 255
		self.lst_notice.append([notice_text,notice_text_x,notice_text_y,notice_text_time])

class Warrior(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Warrior, self).__init__()
		self.x = x
		self.y = y
		self.lst_notice = []

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.revive = False
		self.size = 24

		path_img = './Assets/'+ str(self.__class__.__name__).title()
		for i in range(1,5):
			image = pygame.image.load(f'{path_img}/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'{path_img}/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 9): # attack
			image = pygame.image.load(f'{path_img}/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'{path_img}/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'{path_img}/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0
		self.state_direction = 'right'

		self.alive = True
		self.attack = False
		self.attack2 = False
		self.hit = False
		self.jump = False
		self.above_ground = True
		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
				# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True
				# print(self.vel, dy)
				
		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					# self.jump = False
					# self.vel = self.jump_height
					self.vel = - self.vel
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True
		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
					self.revive = True
					self.death_index = 0
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack2:
						if self.attack_index >= len(self.attack_list):
							self.attack_index = 0
							self.attack2 = False
							self.attack = False
						pass
					elif self.attack_index == 5:
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.state_direction != 'right': # add
					self.image = pygame.transform.flip(self.image, True, False) # add
				# if self.direction == -1:
				# 	self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]

		if self.alive and len(self.lst_notice)>0:
			for i in range(len(self.lst_notice)):
				try:
					notice = self.lst_notice[i]
					if notice[3] > 0:
						notice[3] -= 10
						if notice[3] <= 150:
							notice[3] -= 5
						notice[2] -= 1
						notice[0].set_alpha(notice[3])
						self.win.blit(notice[0], (notice[1], notice[2]))
					else:
						self.lst_notice.pop(i)
						i-=1
				except:
					print('null')
					i-=1


	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.state_direction = 'left' # add 
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.state_direction = 'right' # add
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump :
			self.above_ground = False
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity
			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel
		if self.attack and not self.jump: # khi skill , đứng yên
			self.dx = 0
		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()

	def revival(self, x, y, health=100):
		self.rect = self.image.get_rect(center=(x, y))
		self.health = health
		self.revive = False
		self.alive = True
		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.attack = False
			
	def draw(self, win):
		win.blit(self.image, self.rect)
	
	def add_notice(self, notice, type, win):
		if not hasattr(self,'win'):
			self.win = win
		notice_text = pygame.font.Font(None, 20).render(notice, True, (255,0,0) if type==2 else (0,255,0))
		notice_text_x = self.rect.x + 20
		notice_text_y = self.rect.y - 20
		notice_text_time = 255
		self.lst_notice.append([notice_text,notice_text_x,notice_text_y,notice_text_time])

class Knight(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Knight, self).__init__()
		self.x = x
		self.y = y
		self.lst_notice = []

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []
		self.revive = False
		self.size = 32

		path_img = './Assets/'+ str(self.__class__.__name__).title()
		for i in range(1,6):
			image = pygame.image.load(f'{path_img}/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (32,32))
			self.idle_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'{path_img}/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (32,32))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)

		for i in range(1, 6):
			image = pygame.image.load(f'{path_img}/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (32,32))
			self.attack_list.append(image)
		for i in range(1,12):
			image = pygame.image.load(f'{path_img}/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (32,32))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'{path_img}/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (32,32))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0
		self.state_direction = 'right'

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False
		self.above_ground = True
		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (32,32))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
				# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True
				# print(self.vel, dy)
				
		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					# self.jump = False
					# self.vel = self.jump_height
					self.vel = - self.vel
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True


		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
					self.revive = True
					self.death_index = 0
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.state_direction != 'right': # add
					self.image = pygame.transform.flip(self.image, True, False) # add
				# if self.direction == -1:
				# 	self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]

		if self.alive and len(self.lst_notice)>0:
			for i in range(len(self.lst_notice)):
				try:
					notice = self.lst_notice[i]
					if notice[3] > 0:
						notice[3] -= 10
						if notice[3] <= 150:
							notice[3] -= 5
						notice[2] -= 1
						notice[0].set_alpha(notice[3])
						self.win.blit(notice[0], (notice[1], notice[2]))
					else:
						self.lst_notice.pop(i)
						i-=1
				except:
					print('null')
					i-=1


	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.state_direction = 'left' # add 
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.state_direction = 'right' # add
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump :
			self.above_ground = False
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity
			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		if self.attack:
			k = 1 if self.state_direction == 'right' else -1
			self.dx += self.speed*k

		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()

	def revival(self, x, y, health=100):
		self.rect = self.image.get_rect(center=(x, y))
		self.health = health
		self.revive = False
		self.alive = True
		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.attack = False
		
	def draw(self, win):
		win.blit(self.image, self.rect)
	
	def add_notice(self, notice, type, win):
		if not hasattr(self,'win'):
			self.win = win
		notice_text = pygame.font.Font(None, 20).render(notice, True, (255,0,0) if type==2 else (0,255,0))
		notice_text_x = self.rect.x + 20
		notice_text_y = self.rect.y - 20
		notice_text_time = 255
		self.lst_notice.append([notice_text,notice_text_x,notice_text_y,notice_text_time])

class Archer(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Archer, self).__init__()
		self.x = x
		self.y = y
		self.lst_notice = []

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.death_list = []
		self.hit_list = []

		self.revive = False
		self.size = 24

		path_img = './Assets/'+ str(self.__class__.__name__).title()
		for i in range(1,6):
			image = pygame.image.load(f'{path_img}/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,11):
			image = pygame.image.load(f'{path_img}/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)

		for i in range(1, 10):
			image = pygame.image.load(f'{path_img}/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)
		for i in range(1,8):
			image = pygame.image.load(f'{path_img}/PlayerDead{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.death_list.append(image)
		for i in range(1, 3):
			image = pygame.image.load(f'{path_img}/PlayerHit{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.hit_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		

		self.jump_height = 15
		self.speed = 3
		self.vel = self.jump_height
		self.mass = 1
		self.gravity = 1

		self.counter = 0
		self.direction = 0
		self.state_direction = 'right'

		self.alive = True
		self.attack = False
		self.hit = False
		self.jump = False
		self.above_ground = True
		self.grenades = 5
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def check_collision(self, world, dx, dy):
		# Checking collision with ground
		for tile in world.ground_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# above ground
				if self.rect.y + dy <= tile[1].y:
				# if self.vel < 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True
				# print(self.vel, dy)
				
		# Checking collision with rocks & stones
		for tile in world.rock_list:
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
				# left / right collision
				dx = 0
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
				# below ground
				if self.vel > 0 and self.vel != self.jump_height:
					dy = 0
					# self.jump = False
					# self.vel = self.jump_height
					self.vel = - self.vel
				# above ground
				elif self.vel <= 0 or self.vel == self.jump_height:
					dy = tile[1].top - self.rect.bottom
					self.above_ground = True


		return dx, dy

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.health <= 0:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.alive = False
					self.revive = True
					self.death_index = 0
			else:
				if self.attack:
					self.attack_index += 1
					if self.attack_index >= len(self.attack_list):
						self.attack_index = 0
						self.attack = False
				if self.hit:
					self.hit_index += 1
					if self.hit_index >= len(self.hit_list):
						self.hit_index = 0
						self.hit = False
				if self.direction == 0:
					self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
				if self.direction == -1 or self.direction == 1:
					self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.health <= 0:
				self.image = self.death_list[self.death_index]
			elif self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.state_direction != 'right': # add
					self.image = pygame.transform.flip(self.image, True, False) # add
				# if self.direction == -1:
				# 	self.image = pygame.transform.flip(self.image, True, False)
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]		

		if self.alive and len(self.lst_notice)>0:
			for i in range(len(self.lst_notice)):
				try:
					notice = self.lst_notice[i]
					if notice[3] > 0:
						notice[3] -= 10
						if notice[3] <= 150:
							notice[3] -= 5
						notice[2] -= 1
						notice[0].set_alpha(notice[3])
						self.win.blit(notice[0], (notice[1], notice[2]))
					else:
						self.lst_notice.pop(i)
						i-=1
				except:
					print('null')


	def update(self, moving_left, moving_right, world):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.state_direction = 'left' # add 
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.state_direction = 'right' # add
		if (not moving_left and not moving_right) and not self.jump:
			self.direction = 0
			self.walk_index = 0

		if self.jump :
			self.above_ground = False
			F = (1/2) * self.mass * self.vel
			self.dy -= F
			self.vel -= self.gravity
			if self.vel < -15:
				self.vel = self.jump_height
				self.jump = False
		else:
			self.dy += self.vel

		if self.attack and not self.jump: # khi skill , đứng yên
			self.dx = 0
		self.dx, self.dy = self.check_collision(world, self.dx, self.dy)

		if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
			self.dx = 0

		self.rect.x += self.dx
		self.rect.y += self.dy

		self.update_animation()

	def revival(self, x, y, health=100):
		self.rect = self.image.get_rect(center=(x, y))
		self.health = health
		self.revive = False
		self.alive = True
		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.attack = False
			
	def draw(self, win):
		win.blit(self.image, self.rect)
	
	def add_notice(self, notice, type, win):
		if not hasattr(self,'win'):
			self.win = win
		notice_text = pygame.font.Font(None, 20).render(notice, True, (255,0,0) if type==2 else (0,255,0))
		notice_text_x = self.rect.x + 20
		notice_text_y = self.rect.y - 20
		notice_text_time = 255
		self.lst_notice.append([notice_text,notice_text_x,notice_text_y,notice_text_time])

class PlayerSelectButton(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(PlayerSelectButton, self).__init__()
		self.x = x
		self.y = y

		self.idle_list = []
		self.walk_left = []
		self.walk_right = []
		self.attack_list = []
		self.size = 24
		path_img = './Assets/Snow'
		for i in range(1,3):
			image = pygame.image.load(f'{path_img}/PlayerIdle{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.idle_list.append(image)
		for i in range(1,6):
			image = pygame.image.load(f'{path_img}/PlayerWalk{i}.png')
			right = pygame.transform.scale(image, (24, 24))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 5):
			image = pygame.image.load(f'{path_img}/PlayerAttack{i}.png')
			image = pygame.transform.scale(image, (24, 24))
			self.attack_list.append(image)

		self.idle_index = 0
		self.walk_index = 0
		self.attack_index = 0

		self.speed = 6

		self.counter = 0
		self.direction = 0
		self.state_direction = 'right'

		self.alive = True
		self.attack = False
		self.health = 100

		self.image = self.idle_list[self.idle_index]
		self.image = pygame.transform.scale(self.image, (24, 24))
		self.rect = self.image.get_rect(center=(x, y))

	def update_animation(self):
		self.counter += 1
		if self.counter % 7 == 0:
			if self.attack:
				self.attack_index += 1
				if self.attack_index >= len(self.attack_list):
					self.attack_index = 0
					self.attack = False
			if self.direction == 0:
				self.idle_index = (self.idle_index + 1) % len(self.idle_list)			
			if self.direction == -1 or self.direction == 1:
				self.walk_index = (self.walk_index + 1) % len(self.walk_left)
			self.counter = 0

		if self.alive:
			if self.attack:
				self.image = self.attack_list[self.attack_index]
				if self.state_direction != 'right': # add
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == 0:
				self.image = self.idle_list[self.idle_index]
				if self.state_direction != 'right':
					self.image = pygame.transform.flip(self.image, True, False)
			elif self.direction == -1:
				self.image = self.walk_left[self.walk_index]
			elif self.direction == 1:
				self.image = self.walk_right[self.walk_index]


	def update(self, moving_left, moving_right, moving_up, moving_down):
		self.dx = 0
		self.dy = 0

		if moving_left:
			self.dx = -self.speed
			self.direction = -1
			self.state_direction = 'left' # add 
		if moving_right:
			self.dx = self.speed
			self.direction = 1
			self.state_direction = 'right' # add
		if (not moving_left and not moving_right):
			self.direction = 0
			self.walk_index = 0
		if moving_up:
			self.dy -= self.speed
		if moving_down:
			self.dy += self.speed

		self.rect.x += self.dx
		self.rect.y += self.dy

		if self.rect.x > WIDTH:
			self.rect.x -= WIDTH
		if self.rect.x < 0:
			self.rect.x += WIDTH
		if self.rect.y > HEIGHT:
			self.rect.y -= HEIGHT
		if self.rect.y < 0:
			self.rect.y += HEIGHT

		self.update_animation()

		
	def draw(self, win):
		win.blit(self.image, self.rect)
