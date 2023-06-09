import random
import pygame
from projectiles import Gun

TILE_SIZE = 16

pygame.mixer.init()
bullet_fx = pygame.mixer.Sound('Sounds/ghost_shot.mp3')

class Ghost(pygame.sprite.Sprite):
	def __init__(self, x, y, win):
		super(Ghost, self).__init__()

		self.x = x
		self.y = y
		self.win = win
		self.initial_pos_x = x

		self.size = 24
		
		self.walk_left = []
		self.walk_right = []
		self.hit_list = []
		self.death_list = []

		for i in range(1,6):
			image = pygame.image.load(f'Assets/Ghost/Enemywalk{i}.png')
			right = right = pygame.transform.scale(image, (self.size, self.size))
			left = pygame.transform.flip(right, True, False)
			self.walk_right.append(right)
			self.walk_left.append(left)
		for i in range(1, 3):
			image = pygame.image.load(f'Assets/Ghost/Enemyhit{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			self.hit_list.append(image)
		for i in range(1,9):
			image = pygame.image.load(f'Assets/Ghost/Enemydead{i}.png')
			image = pygame.transform.scale(image, (self.size, self.size))
			self.death_list.append(image)

		self.walk_index = 0
		self.death_index = 0
		self.hit_index = 0
		self.counter = 0

		self.dx = random.choice([-1, 1])
		self.alive = True
		self.health = 100
		self.max_health = 100
		self.hit = False
		self.on_death_bed = False
		self.direct_get_damge = ''
		self.id_get_damage = 0
		
		self.image = self.walk_right[self.walk_index]
		self.rect = self.image.get_rect(center=(self.x, self.y))
		self.get_damage_aplha = 0

	def get_hit(self, dame):
		self.health -= dame
		self.get_damage_text = pygame.font.Font(None, 20).render(f"-{dame}", True, (255,0,0))
		self.get_damage_x = self.rect.x + 30
		self.get_damage_y = self.rect.y - 30
		self.get_damage_aplha = 255
		self.win.blit(self.get_damage_text, (self.get_damage_x, self.get_damage_y))


	def update(self, screen_scroll, bullet_group, p):
		if self.health >0:
			self.rect.x += (self.dx + screen_scroll)
			self.x += screen_scroll
			if abs(self.rect.x - self.x) >= 2 * TILE_SIZE:
				self.dx *= -1

		if self.health <= 0:
			self.on_death_bed = True

		self.counter += 1
		if self.counter % 5 == 0:
			if self.on_death_bed:
				self.death_index += 1
				if self.death_index >= len(self.death_list):
					self.kill()
					self.alive = False
			if self.hit:
				self.hit_index += 1
				if self.hit_index >= len(self.hit_list):
					self.hit_index = 0
					self.hit = False
			else:
				self.walk_index  = (self.walk_index + 1) % len(self.walk_left)
				
		if self.counter % 50 == 0:
			if self.health > 0 and (abs(p.rect.x - self.rect.x) <= 200):
				x, y = self.rect.center
				direction = self.dx
				bullet = Gun(x, y, direction, 2, self.win)
				bullet_group.add(bullet)

		if self.alive:
			if self.on_death_bed:
				self.image = self.death_list[self.death_index]
			elif self.hit:
				self.image = self.hit_list[self.hit_index]
			else:
				if self.dx == -1:
					self.image = self.walk_left[self.walk_index]
				elif self.dx == 1:
					self.image = self.walk_right[self.walk_index]
			pygame.draw.rect(self.win, (255, 0, 0), (self.rect.x+5, self.rect.y - 10, 24, 5))
			pygame.draw.rect(self.win, (0, 255, 0), (self.rect.x+5, self.rect.y - 10, 24 * (self.health / self.max_health), 5))
		
		if self.get_damage_aplha > 0:
			self.get_damage_aplha -= 10
			if self.get_damage_aplha <= 150:
				self.get_damage_aplha -= 5
			self.get_damage_y -= 1
			self.get_damage_text.set_alpha(self.get_damage_aplha)
			self.win.blit(self.get_damage_text, (self.get_damage_x, self.get_damage_y))

	def draw(self, win):
		win.blit(self.image, self.rect)