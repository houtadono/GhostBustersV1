from configparser import ConfigParser
import json
import pygame
import os

from world import World, load_level
from player import Player, Warrior, PlayerSelectButton
from enemies import Ghost
from particles import Trail
from projectiles import Gun, Fireball, Grenade, Sword
from button import Button
from texts import Text, Message, BlinkingText, MessageBox
from time import time, sleep

pygame.init()

WIDTH, HEIGHT = 640, 384
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
TILE_SIZE = 16

clock = pygame.time.Clock()
FPS = 45

# IMAGES **********************************************************************

BG1 = pygame.transform.scale(
    pygame.image.load('assets/BG1.png'), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(
    pygame.image.load('assets/BG2.png'), (WIDTH, HEIGHT))
BG3 = pygame.transform.scale(
    pygame.image.load('assets/BG3.png'), (WIDTH, HEIGHT))
MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

GREY_LAYER = pygame.Surface((35, 35), pygame.SRCALPHA)
GREY_LAYER.fill((128, 128, 128, 200))

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
instructions_font = 'Fonts/BubblegumSans-Regular.ttf'
# about_font = 'Fonts/DalelandsUncialBold-82zA.ttf'

ghostbusters = Message(WIDTH//2 + 50, HEIGHT//2 - 90, 90,
                       "GhostBusters", title_font, (255, 255, 255), win)
left_key = Message(WIDTH//2 + 10, HEIGHT//2 - 90, 20,
                   "Press left arrow key to go left", instructions_font, (255, 255, 255), win)
right_key = Message(WIDTH//2 + 10, HEIGHT//2 - 65, 20,
                    "Press right arrow key to go right", instructions_font, (255, 255, 255), win)
up_key = Message(WIDTH//2 + 10, HEIGHT//2 - 45, 20,
                 "Press up arrow key to jump", instructions_font, (255, 255, 255), win)
space_key = Message(WIDTH//2 + 10, HEIGHT//2 - 25, 20,
                    "Press space key to shoot", instructions_font, (255, 255, 255), win)
g_key = Message(WIDTH//2 + 10, HEIGHT//2 - 5, 20,
                "Press g key to throw grenade", instructions_font, (255, 255, 255), win)
game_won_msg = Message(WIDTH//2 + 10, HEIGHT//2 - 5, 20,
                       "You have won the game", instructions_font, (255, 255, 255), win)
paused_msg = Message(WIDTH//2 + 10, HEIGHT//4, 40,
                       "Do you want to stop the game?", instructions_font, (255, 255, 255), win)
loadMessage1_game = Message(WIDTH//2 + 70, HEIGHT//2 - 5, 20,
                            "Can't load the save game. Start a new game?", instructions_font, (255, 255, 255), win)
loadMessage2_game = Message(WIDTH//2 + 70, HEIGHT//2 + 30,
                            20, "Y for yes", instructions_font, (255, 255, 255), win)


t = Text(instructions_font, 18)
font_color = (12, 12, 12)
play = t.render('Play', font_color)
load = t.render('Continue', font_color)
about = t.render('About', font_color)
controls = t.render('Controls', font_color)
exit = t.render('Exit', font_color)
main_menu = t.render('Main Menu', font_color)

save = t.render('Save', font_color)
contiune1 = t.render('Contiune', font_color)

about_font = pygame.font.SysFont('Times New Roman', 20)
with open('Data/about.txt') as f:
	info = f.read().replace('\n', ' ')

# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 35, ButtonBG, 0.5, play, 10)
load_btn = Button(WIDTH//2 - bwidth//4, HEIGHT //2, ButtonBG, 0.5, load, 10)
# about_btn = Button(WIDTH//2 - bwidth//4, HEIGHT //2 + 35, ButtonBG, 0.5, about, 10)
controls_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 70, ButtonBG, 0.5, controls, 10)
exit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT // 2 + 105, ButtonBG, 0.5, exit, 10)
main_menu_btn = Button(WIDTH//2 - bwidth//4, HEIGHT //2 + 140, ButtonBG, 0.5, main_menu, 20)

red_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2+35, ButtonBG,0.5, t.render('Red', font_color), 10)
white_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 70, ButtonBG,0.5, t.render('White', font_color), 10)
warrior_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 105, ButtonBG,0.5, t.render('Warrior', font_color), 10)

continue_btn = Button(WIDTH//2 - bwidth//4 + 70, HEIGHT //2 + 40, ButtonBG, 0.5, contiune1, 10)
save_btn = Button(WIDTH//2 - bwidth//4 + 70, HEIGHT //2 + 75, ButtonBG, 0.5, save, 10)
exit1_btn = Button(WIDTH//2 - bwidth//4 + 70, HEIGHT //2 + 110, ButtonBG, 0.5, exit, 10)
exit2_btn = Button(WIDTH//2 - bwidth//4 + 70, HEIGHT //2 + 75, ButtonBG, 0.5, exit, 10)

# MUSIC ***********************************************************************

pygame.mixer.music.load('Sounds/mixkit-complex-desire-1093.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0)

diamond_fx = pygame.mixer.Sound('Sounds/point.mp3')
diamond_fx.set_volume(0.6)
bullet_fx = pygame.mixer.Sound('Sounds/bullet.wav')
jump_fx = pygame.mixer.Sound('Sounds/jump.mp3')
health_fx = pygame.mixer.Sound('Sounds/health.wav')
menu_click_fx = pygame.mixer.Sound('Sounds/menu.mp3')
next_level_fx = pygame.mixer.Sound('Sounds/level.mp3')
grenade_throw_fx = pygame.mixer.Sound('Sounds/grenade throw.wav')
grenade_throw_fx.set_volume(0.6)

# GROUPS **********************************************************************

trail_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
diamond_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

objects_group = [water_group, diamond_group,
    potion_group, enemy_group, exit_group]

# LEVEL VARIABLES **************************************************************

ROWS = 24
COLS = 40
SCROLL_THRES = 200
MAX_LEVEL = 3

level = 0
points = 0
pre_level = 0
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0

# RESET ***********************************************************************


def reset_level(level):
	trail_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	enemy_group.empty()
	water_group.empty()
	diamond_group.empty()
	potion_group.empty()
	exit_group.empty()

	# LOAD LEVEL WORLD

	world_data, level_length = load_level(level)
	w = World(objects_group)
	w.generate_world(world_data, win)

	return world_data, level_length, w

def get_info_player(type_):
	config = ConfigParser()
	config.read(f'./Data/player.properties')
	global p_reload_time, p_reload_time2, p_path_img, p_class, p_weapon, img_skill, img_skill2
	p_reload_time = float(config[type_]['reload_time'])
	k = config[type_]['class']

	k = config[type_]['weapon']
	if k == 'Sword':
		p_class = Warrior
		p_weapon = Sword
	elif k=='Gun':
		p_class = Player
		p_weapon = Gun
	elif k=='Fireball':
		p_class = Player
		p_weapon = Fireball

	p_path_img = config[type_]['image_folder']
	img_skill = pygame.image.load( f'%s' %(str(config[type_]['img_skill'])) )
	img_skill = pygame.transform.scale(img_skill, (24, 24))
	try:
		img_skill2 = pygame.image.load(f'%s'%(str(config[type_]['img_skill2'])))
		img_skill2 = pygame.transform.scale(img_skill2, (24, 24))
		p_reload_time2 = float(config[type_]['reload_time2'])
	except:
		img_skill2 = None
		p_reload_time2 = 0
		pass

def reset_player():
	global p_path_img,p_type,p_class
	get_info_player(p_type)
	p = p_class(250, 50, p_path_img)
	moving_left = False
	moving_right = False
	return p, moving_left, moving_right

def load_data_continue_pre_game():
	try:
		global level, p_type, p_path_img, p
		with open(f'./Data/save_level') as f :
			p_type_new = f.readline()[:-1] 
			level, health, grenades, scoures = map(int,f.readline().split())
		if p_type_new != p_type:
			p_type = p_type_new
			p = reset_player()[0]
		p.health = health
		p.grenades = grenades
		return True
	except:
		return False

def draw_image_skill(win, delta_time):
	global p_remain_reload, img_skill, img_skill2,p_remain_reload2, p_reload_time2, p_reload_time2
	if p_remain_reload>0:
		p_remain_reload -= delta_time
		if p_remain_reload<0:
			p_remain_reload = 0
	
	image_rect = img_skill.get_rect()
	image_rect.center = (25, 70)
	frame_size = (35, 35)
	frame_rect = pygame.Rect(0, 0, *frame_size)
	frame_rect.center = image_rect.center

	if p_remain_reload == 0:
		frame_color = (0, 0, 0)
	else:
		frame_color = (128,128,128)

	copy = img_skill.copy()
	x = 35*(1-p_remain_reload/p_reload_time)

		# vẽ nền đỏ đằng sau
	pygame.draw.rect(win, (255, 0, 0), frame_rect)
		# lớp phủ đè lên img_skill
	copy.blit(GREY_LAYER, (0, x,35,35))
		# vẽ ra lớp phủ 
	win.blit(copy, image_rect)
		# vẽ khung
	pygame.draw.rect(win, frame_color, frame_rect, 2)


	# draw skill 2:
	if img_skill2 == None:
		return
	
	if p_remain_reload2>0:
		p_remain_reload2 -= delta_time
		if p_remain_reload2<0:
			p_remain_reload2 = 0
	
	image_rect = img_skill2.get_rect()
	image_rect.center = (65, 70)
	frame_size = (35, 35)
	frame_rect = pygame.Rect(0, 0, *frame_size)
	frame_rect.center = image_rect.center

	if p_remain_reload == 0:
		frame_color = (0, 0, 0)
	else:
		frame_color = (128,128,128)

	copy = img_skill2.copy()
	x = 35*(1-p_remain_reload2/p_reload_time2)

		# vẽ nền đỏ đằng sau
	pygame.draw.rect(win, (255, 0, 0), frame_rect)
		# lớp phủ đè lên img_skill2
	copy.blit(GREY_LAYER, (0, x,35,35))
		# vẽ ra lớp phủ 
	win.blit(copy, image_rect)
		# vẽ khung
	pygame.draw.rect(win, frame_color, frame_rect, 2)

	
# player ...
p_remain_reload = p_remain_reload2 = 0
p_reload_time = p_reload_time2 = 0
p_path_img = None
p_type = 'adminwhite'
p_class = None
p_weapon = None
img_skill = img_skill2 = None
p, moving_left, moving_right = reset_player()
moving_up = moving_down = False

# MAIN GAME *******************************************************************


main_menu = True
about_page = False
controls_page = False
exit_page = False
continue_game = False 
game_start = False

select_player = False  # add
game_won = False
game_pause = False
running = True

p_select = PlayerSelectButton(210, HEIGHT//2+50, f'Assets/Player')
bullet_select = pygame.sprite.Group()

while running:
	buttons = []
	if level != pre_level:
		status = '|'.join([str(level),str(points),type(p_class).__name__])
		print(status)
		pre_level = level

	win.fill((0, 0, 0))
	for x in range(5):
		win.blit(BG1, ((x*WIDTH) - bg_scroll * 0.6, 0))
		win.blit(BG2, ((x*WIDTH) - bg_scroll * 0.7, 0))
		win.blit(BG3, ((x*WIDTH) - bg_scroll * 0.8, 0))

	if not game_start:
		win.blit(MOON, (-40, 150))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False

		if event.type == pygame.KEYDOWN and not game_start:

			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				moving_up = True
			if event.key == pygame.K_DOWN:
				moving_down = True
			if event.key == pygame.K_SPACE:
				x, y = (p_select.rect.center)
				bullet = Gun(x, y, 1 if p_select.state_direction == 'right' else -1, 1, win)
				bullet_select.add(bullet)
				p_select.attack = True

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP:
				if p.above_ground and not p.jump:
					p.jump = True
					p.above_ground = False
					jump_fx.play()
			if event.key == pygame.K_SPACE:
				if p_remain_reload == 0 :
					x, y = p.rect.center
					direction = 1 if p.state_direction == 'right' else -1  # add

					bullet = p_weapon(x, y, direction, 1, win)
					bullet_group.add(bullet)

					p_remain_reload = p_reload_time
					p.attack = True
				elif p_reload_time2 != 0 and p_remain_reload2 == 0 and p.attack_index < 4 and p.attack_index >0:
					x, y = p.rect.center
					direction = 1 if p.state_direction == 'right' else -1
					bullet = p_weapon(x, y, direction, 1, win, False)
					bullet_group.add(bullet)
					p_remain_reload2 = p_reload_time2
					p.attack2 = True
					pass
			if event.key == pygame.K_g:
				if p.grenades:
					p.grenades -= 1
					grenade = Grenade(p.rect.centerx, p.rect.centery,
					                  1 if p.state_direction == 'right' else -1, win)
					grenade_group.add(grenade)
					grenade_throw_fx.play()
			if event.key == pygame.K_p: # press p to pause
				game_pause = True
				game_start = False
				pass
			
			if event.key == pygame.K_q: # press q to quit
				pass 

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_UP:
				moving_up = False
			if event.key == pygame.K_DOWN:
				moving_down = False

	if not game_start:
		trail_group.update()
		p_select.update(moving_left, moving_right, moving_up, moving_down)
		p_select.draw(win)
		t = Trail(p_select.rect.center, (220, 220, 220), win)
		trail_group.add(t)
		bullet_select.update(0,None)
	else:
		p_select.kill()

	if main_menu:
		ghostbusters.update()
		if play_btn.draw(win):
			menu_click_fx.play()
			# world_data, level_length, w = reset_level(level)
			# p, moving_left, moving_right = reset_player()

			select_player = True  # add
			main_menu = False  # add
		if os.path.exists(f'./Data/save_level'):
			buttons.append(load_btn)
			if load_btn.draw(win):
				menu_click_fx.play()
				check = load_data_continue_pre_game()
				if check:
					last_time = time() # add
					game_start = True
					main_menu = False
				else:
					os.remove(f'./Data/save_level')
		# if about_btn.draw(win):
		# 	menu_click_fx.play()
		# 	about_page = True
		# 	main_menu = False

		if controls_btn.draw(win):
			menu_click_fx.play()
			controls_page = True
			main_menu = False

		if exit_btn.draw(win):
			menu_click_fx.play()
			running = False
	
		buttons.append(play_btn)
		buttons.append(controls_btn)
		buttons.append(exit_btn)

	elif select_player:
		if red_btn.draw(win):
			game_start = True
			p_type='adminred'

		if white_btn.draw(win):
			game_start = True
			p_type='adminwhite'

		if warrior_btn.draw(win):
			game_start = True
			p_type = 'warrior'

		if game_start:
			select_player = False
			menu_click_fx.play()
			level += 1
			world_data, level_length, w = reset_level(level)
			last_time = time() # add
			p, moving_left, moving_right = reset_player()
			main_menu = False

		if main_menu_btn.draw(win):
			menu_click_fx.play()
			select_player = False
			main_menu = True
		buttons.append(red_btn)
		buttons.append(white_btn)
		buttons.append(warrior_btn)
		buttons.append(main_menu_btn)
		
	elif about_page:
		MessageBox(win, about_font, 'GhostBusters', info)
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			about_page = False
			main_menu = True

	elif controls_page:
		left_key.update()
		right_key.update()
		up_key.update()
		space_key.update()
		g_key.update()

		if main_menu_btn.draw(win):
			menu_click_fx.play()
			controls_page = False
			main_menu = True
		buttons.append(main_menu_btn)

	elif exit_page:
		pass

	elif game_won:
		game_won_msg.update()
		if main_menu_btn.draw(win):
			menu_click_fx.play()
			controls_page = False
			main_menu = True
			level = 1
	elif game_pause:
		paused_msg.update()
		if load_btn.draw(win):
			game_pause = False
			game_start = True
			last_time = time() 
		buttons.append(load_btn)
		pass	
	elif game_start:
		current_time = time() 
		delta_time = current_time - last_time # add
		win.blit(MOON, (-40, -10))
		w.draw_world(win, screen_scroll)

		# Updating Objects ********************************************************

		bullet_group.update(screen_scroll, w)
		grenade_group.update(screen_scroll, p, enemy_group, explosion_group, w)
		explosion_group.update(screen_scroll)
		trail_group.update()
		water_group.update(screen_scroll)
		water_group.draw(win)
		diamond_group.update(screen_scroll)
		diamond_group.draw(win)
		potion_group.update(screen_scroll)
		potion_group.draw(win)
		exit_group.update(screen_scroll)
		exit_group.draw(win)

		enemy_group.update(screen_scroll, bullet_group, p)
		enemy_group.draw(win)

		if p.jump:
			t = Trail(p.rect.center, (220, 220, 220), win)
			trail_group.add(t)

		screen_scroll = 0
		p.update(moving_left, moving_right, w)
		p.draw(win)

		if (p.rect.right >= WIDTH - SCROLL_THRES and bg_scroll < (level_length*TILE_SIZE) - WIDTH) \
			or (p.rect.left <= SCROLL_THRES and bg_scroll > abs(dx)):
			dx = p.dx
			p.rect.x -= dx
			screen_scroll = -dx
			bg_scroll -= screen_scroll


		# Collision Detetction ****************************************************

		if p.rect.bottom > HEIGHT:
			p.health = 0

		if pygame.sprite.spritecollide(p, water_group, False):
			p.health = 0
			level = 1

		if pygame.sprite.spritecollide(p, diamond_group, True):
			diamond_fx.play()
			pass

		if pygame.sprite.spritecollide(p, exit_group, False):
			next_level_fx.play()
			level += 1
			if level <= MAX_LEVEL:
				health = p.health

				world_data, level_length, w = reset_level(level)
				p, moving_left, moving_right = reset_player() 
				p.health = health

				screen_scroll = 0
				bg_scroll = 0
			else:
				game_won = True


		potion = pygame.sprite.spritecollide(p, potion_group, False)
		if potion:
			if p.health < 100:
				potion[0].kill()
				p.health += 15
				health_fx.play()
				if p.health > 100:
					p.health = 100


		for bullet in bullet_group:
			enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
			if enemy and bullet.type == 1:
				if not enemy[0].hit:
					enemy[0].hit = True
					enemy[0].health -= bullet.dame # add
					if hasattr(bullet,'skill1') and bullet.skill1 == False:
						p.health += (100-p.health)//20
				bullet.kill()
			if bullet.rect.colliderect(p):
				if bullet.type == 2:
					if not p.hit:
						p.hit = True
						p.health -= 20
						print(p.health)
					bullet.kill()

		# drawing variables *******************************************************

		if p.alive:
			color = (0, 255, 0)
			if p.health <= 40:
				color = (255, 0, 0)
			pygame.draw.rect(win, color, (6, 8, p.health, 20), border_radius=10)
		pygame.draw.rect(win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

		for i in range(p.grenades):
			pygame.draw.circle(win, (200, 200, 200), (20 + 15*i, 40), 5)
			pygame.draw.circle(win, (255, 50, 50), (20 + 15*i, 40), 4)
			pygame.draw.circle(win, (0, 0, 0), (20 + 15*i, 40), 1)
		
		draw_image_skill(win,delta_time)

		if p.health <= 0:
			level -= 1 
			screen_scroll = 0
			bg_scroll = 0

			main_menu = True
			about_page = False
			controls_page = False
			game_start = False
		last_time = time()

	if not game_start:
		check = False
		for bullet in bullet_select:
			for bt in buttons:
				if bt.rect.collidepoint(bullet.rect.x, bullet.rect.y):
					bt.shot = True
					check = True
					break
			if check:
				bullet_select = pygame.sprite.Group()
				break

	pygame.draw.rect(win, (255, 255,255), (0, 0, WIDTH, HEIGHT), 4, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()