from configparser import ConfigParser
import json
import pygame
import os
import pickle
import datetime
import random
import pygame_gui
from world import World, load_level
from player import Snow, Ignis, Warrior,Knight, PlayerSelectButton, Archer
from enemies import Ghost
from particles import Trail
from projectiles import Gun, Fireball, Grenade, Sword, Lance, Arrow
from button import Button, RadioButton
from texts import Text, Message, BlinkingText, MessageBox
from time import time, sleep
from scoreboard import User, Scoreboard
pygame.init()

WIDTH, HEIGHT =640, 484
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
about_font = 'Fonts/DalelandsUncialBold-82zA.ttf'

ghostbusters = Message(WIDTH//2 + 50, HEIGHT//2 - 90, 90,
                       "GhostBusters", title_font, (255, 255, 255), win)
left_key = Message(WIDTH//2 + 10, HEIGHT//2 - 190, 30,
                   "Press LEFT ARROW key to go left", instructions_font, (255, 255, 255), win)
right_key = Message(WIDTH//2 + 10, HEIGHT//2 - 140, 30,
                    "Press RIGHT ARROW key to go right", instructions_font, (255, 255, 255), win)
up_key = Message(WIDTH//2 + 10, HEIGHT//2 - 90, 30,
                 "Press UP ARROW key to jump", instructions_font, (255, 255, 255), win)
space_key = Message(WIDTH//2 + 10, HEIGHT//2 - 40, 30,
                    "Press SPACE key to use skill", instructions_font, (255, 255, 255), win)
g_key = Message(WIDTH//2 + 10, HEIGHT//2 + 10, 30,
                "Press G key to throw grenade", instructions_font, (255, 255, 255), win)
p_key = Message(WIDTH//2 + 10, HEIGHT//2 + 60, 30,
                "Press Q key to pause game", instructions_font, (255, 255, 255), win)
q_key = Message(WIDTH//2 + 10, HEIGHT//2 + 110, 30,
                "Press Q key to return to main menu", instructions_font, (255, 255, 255), win)
game_won_no_rank_msg = Message(WIDTH//2, 390 , 20,
                       "You won the game but not in the top 5 :<", instructions_font, (255, 255, 255), win)
paused_msg = Message(WIDTH//2 + 10, HEIGHT//4, 40,
                       "Do you want to stop the game?", instructions_font, (255, 255, 255), win)
enter_your_name_msg = Message(WIDTH//2, HEIGHT//4 + 70, 40,
                       "Enter your name", instructions_font, (255, 255, 255), win)
select_player_msg = Message(WIDTH//2, HEIGHT//2 - 200, 45,
                       "Select Players", title_font, (255, 255, 255), win)


t = Text(instructions_font, 18)
font_color = (12, 12, 12)
play = t.render('Play', font_color)
select = t.render('  Select', font_color)
load = t.render('Continue', font_color)
about = t.render('About', font_color)
scoreboard = t.render('Scoreboard', font_color)
controls = t.render('Controls', font_color)
main_menu = t.render('  Main Menu', font_color)
exit = t.render('Exit', font_color)
save = t.render('Save', font_color)
contiune1 = t.render('Contiune', font_color)
quit1 = t.render('Quit', font_color)

about_font = pygame.font.SysFont('Arial', 18)
with open('Data/about.txt') as f:
	info = f.read().replace('\n', ' ')

# BUTTONS *********************************************************************

ButtonBG = pygame.image.load('Assets/ButtonBG.png')
bwidth = ButtonBG.get_width()

play_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 35, ButtonBG, 0.5, play, 10)
load_btn = Button(WIDTH//2 - bwidth//4, HEIGHT //2, ButtonBG, 0.5, load, 10)
# about_btn = Button(WIDTH//2 - bwidth//4, HEIGHT //2 + 35, ButtonBG, 0.5, about, 10)
scoreboard_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 70, ButtonBG, 0.5, scoreboard, 10)
controls_btn = Button(WIDTH//2 - bwidth//4, HEIGHT//2 + 105, ButtonBG, 0.5, controls, 10)
exit_btn = Button(WIDTH//2 - bwidth//4, HEIGHT // 2 + 140, ButtonBG, 0.5, exit, 10)
main_menu_btn = Button(WIDTH//2 - bwidth//4, HEIGHT //2 + 175, ButtonBG, 0.5, main_menu, 20)

continue_btn = Button(WIDTH//2 - bwidth//4 + 70, HEIGHT //2 + 40, ButtonBG, 0.5, contiune1, 10)
quit_btn = Button(WIDTH//2 - bwidth//4 + 70, HEIGHT //2 + 75, ButtonBG, 0.5, quit1, 10)

select_btn= Button(WIDTH//2 - bwidth//4, HEIGHT //2 + 70, ButtonBG, 0.5, select, 20)

right_btn = Button(3*WIDTH//4 - 42 + 40, 180 - 48, pygame.image.load('./Assets/button_next_right.png'), 1.5)
left_btn = Button(WIDTH//4 - 42 - 40, 180 - 48, pygame.image.load('./Assets/button_next_left.png'), 1.5)
# MUSIC ***********************************************************************

pygame.mixer.music.load('./Sounds/wind-145331.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.6)
select_fx = pygame.mixer.Sound('./Sounds/button_select.wav')
diamond_fx = pygame.mixer.Sound('Sounds/point.mp3')
diamond_fx.set_volume(0.6)
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

level = 1
score = 0
level_length = 0
screen_scroll = 0
bg_scroll = 0
dx = 0
config = ConfigParser()
config.read(f'./Data/player.properties')
Scoreboard.read_file()
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
	global p_reload_time, p_reload_time2, p_class, p_weapon, img_skill, img_skill2, img_avt
	p_reload_time = float(config[type_]['reload_time'])
	#k = config[type_]['class']

	k = config[type_]['weapon']
	if k == 'Sword':
		p_class = Warrior
		p_weapon = Sword
	elif k=='Gun':
		p_class = Snow
		p_weapon = Gun
	elif k=='Fireball':
		p_class = Ignis
		p_weapon = Fireball
	elif k=='Lance':
		p_class = Knight
		p_weapon = Lance
	elif k=='Arrow':
		p_class = Archer
		p_weapon = Arrow

	img_avt = pygame.image.load( f'%s' %(str(config[type_]['img_avt'])) )
	img_avt = pygame.transform.scale(img_avt, (36, 36)) 

	img_skill = pygame.image.load( f'%s' %(str(config[type_]['img_skill'])) )
	img_skill = pygame.transform.scale(img_skill, (24, 24))
	if k=='Lance':
		img_skill = pygame.transform.scale(img_skill, (30, 30))
	try:
		img_skill2 = pygame.image.load(f'%s'%(str(config[type_]['img_skill2'])))
		img_skill2 = pygame.transform.scale(img_skill2, (24, 24))
		p_reload_time2 = float(config[type_]['reload_time2'])
	except:
		img_skill2 = None
		p_reload_time2 = 0
		pass

def reset_player():
	global p_type,p_class
	get_info_player(p_type)
	p = p_class(250, 50)
	moving_left = False
	moving_right = False
	return p, moving_left, moving_right

def save_data_game():
	with open("./Data/save_game", "wb") as f:
		pickle.dump(status, f)
	pass

def load_data_continue_pre_game():
	try:
		global level, p_type, p, status, score
		with open("./Data/save_game", "rb") as f:
			status = pickle.load(f)
		p_type = str(status['character']).lower()
		p = reset_player()[0]
		p.health = status['health']
		p.grenades = status['grenades']
		level = status['level']
		score = status['score']
		return True
	except:
		return False

def draw_image_skill(win, delta_time):
	global p_remain_reload, img_skill, img_skill2,p_remain_reload2, p_reload_time2, p_reload_time2
	if p_remain_reload>0 and p.attack == False:
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
	
	if p_remain_reload2>0 and p.attack2 == False:
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

def draw_scoreboard(win, forcus= None):
	s_width = 550
	s_height = 320
	cell_width = s_width // 6
	cell_height = s_height // 6
	border_rect = pygame.Rect(48, 48, s_width + 4, s_height + 4)
	pygame.draw.rect(win, (255, 0, 0), border_rect, 2)

	inner_rect = pygame.Rect(50, 50, s_width, s_height)
	pygame.draw.rect(win, (52, 53, 95), inner_rect)

	font_t = pygame.font.SysFont('Arial', 23)
	font = pygame.font.SysFont('Arial', 19)

	s_lst = Scoreboard.lst

	for i in range(len(s_lst)):
		cell_x = 50
		if i == 0:
			for j,txt in enumerate(['Top','Name','Class','Time','Death','Score']):
				if j == 0:
					cell_width_adj = cell_width // 2
				else:
					cell_width_adj = (s_width - cell_width // 2) // 5
				cell_x += cell_width_adj
				cell_text = font_t.render(txt, True,(255, 255, 255))
				cell_rect = cell_text.get_rect()
				cell_rect.center = (cell_x - cell_width_adj//2, 50 + cell_height // 2)
				win.blit(cell_text, cell_rect)

		if i == forcus:
			pygame.draw.rect(win, (255,255,0), (50 + 0,50 + cell_height * (i+1), s_width, cell_height))
		user = str(s_lst[i]).split('|')
		cell_x = 50
		for j in range(len(user)+1):
			color = (255,0,0) if i == forcus else (255,255,255)
			if j == 0:
				cell_width_adj = cell_width // 2
			else:
				cell_width_adj = (s_width - cell_width // 2) // 5
			if j > 0:
				cell_text = font.render(user[j-1], True,color)
			else:
				cell_text = font.render(f'{i+1}', True,color)
			cell_x += cell_width_adj
			cell_rect = cell_text.get_rect()
			cell_rect.center = (cell_x - cell_width_adj//2, 50 + cell_height * (i+1) + cell_height // 2)
			win.blit(cell_text, cell_rect)

	# vẽ đường kẻ giữa các ô
	for i in range(1, 6):
		if i == 1:
			line_pos = 50 + cell_width // 2
		else:
			line_pos = 50 + cell_width // 2 + (s_width - cell_width // 2) // 5 * (i - 1)
		pygame.draw.line(win, (78, 137, 198), (line_pos, 50+0), (line_pos, 50+s_height))
		pygame.draw.line(win, (78, 137, 198), (50+0, 50+cell_height * i), (50+s_width, 50+cell_height * i))

# player ...
p_remain_reload = p_remain_reload2 = 0
p_reload_time = p_reload_time2 = 0
p_type = 'snow'
p_class = None
p_weapon = None
img_skill = img_skill2 = None
p, moving_left, moving_right = reset_player()
moving_up = moving_down = False

# MAIN GAME *******************************************************************


main_menu = True
about_page = False
controls_page = False
scoreboard_page = False
exit_page = False
continue_game = False 
game_start = False

select_player = False  # add
game_won = False
game_pause = False
enter_name = False
running = True
p_select = PlayerSelectButton(210, HEIGHT//2+50)
bullet_select = pygame.sprite.Group()

lst_player = [Snow(220,142),Ignis(220,142),Warrior(220,142),Knight(220,142),Archer(220,142)]
lst_info_player = [ str(config[(class_p.__class__.__name__).lower()]['info']).replace(',',"\n") for class_p in lst_player ]
player_index = 0
player_select = lst_player[player_index]
counter_select = 0

animation_buttons = [
	RadioButton(WIDTH - 150, HEIGHT//4 + 150, 100, 40, "Idle", selected=True),
	RadioButton(WIDTH - 150, HEIGHT//4 + 200, 100, 40, "Attack"),
	RadioButton(WIDTH - 150, HEIGHT//4 + 250, 100, 40, "Walk"),
	RadioButton(WIDTH - 150, HEIGHT//4 + 300, 100, 40, "Dead")
]
animation_index = 0
animation_select = "Idle"

status = {
	'character': p_type.title(),
	'level' : level,
	'score': score,
	'time_play': 0,
	'die' : 0,
	'grenades': p.grenades,
	'health': p.health
}
status_c = status.copy()
rank = None
gui_manager = pygame_gui.UIManager((640, 480))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((170, 300), (160, 30)),
                                                  manager=gui_manager)
button_input = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((360, 300), (100, 30)),
                                      text='OK',object_id='ok_button',
                                      manager=gui_manager)
while running:
	buttons = []

	win.fill((0, 0, 0))
	for x in range(5):
		win.blit(BG1, ((x*WIDTH) - bg_scroll * 0.6, 0))
		win.blit(BG2, ((x*WIDTH) - bg_scroll * 0.7, 0))
		win.blit(BG3, ((x*WIDTH) - bg_scroll * 0.8, 0))

	if not game_start:
		win.blit(MOON, (-40, 150))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			if status != status_c:
				save_data_game()
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				if status != status_c:
					save_data_game()
				running = False
			if event.key == pygame.K_RETURN and enter_name:
				button_input.process_event(event)
				Scoreboard.lst[rank].name = text_input.text
				Scoreboard.save_file()
				enter_name = False

		if event.type == pygame_gui.UI_BUTTON_PRESSED and enter_name:
			if event.ui_object_id == "ok_button":
				Scoreboard.lst[rank].name = text_input.text
				Scoreboard.save_file()
				enter_name = False

		if event.type == pygame.KEYDOWN and not game_start and not select_player:

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

		elif event.type == pygame.KEYDOWN and game_start and p.health>0: # game_play
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
				if p_remain_reload == 0:
					x, y = p.rect.center
					direction = 1 if p.state_direction == 'right' else -1  # add
					try:
						bullet = p_weapon(x, y, direction, 1, win)
					except:
						bullet = p_weapon(x, y, direction, 1,win,p)
					bullet_group.add(bullet)
					if p_class == Ignis:
							p_reload_time = float(config['ignis']['reload_time']) * (1 - 0.2 * ((100 - p.health)//20))
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
				p_select.rect.x = 300
				pause_time = pygame.time.get_ticks()
				pass
			
		if event.type == pygame.KEYDOWN and event.key == pygame.K_q and not main_menu: # press q to quit
			main_menu = True
			about_page = False
			controls_page = False
			exit_page = False
			continue_game = False
			scoreboard_page = False 
			game_start = False
			select_player = False
			if status != status_c:
				save_data_game()
			pass 
		
		if event.type == pygame.KEYDOWN and select_player:
			if event.key == pygame.K_LEFT:
				player_index -= 1
				if player_index == -1:
					player_index += len(lst_player)
				player_select = lst_player[player_index]
			if event.key == pygame.K_RIGHT:
				player_index += 1
				player_index %= len(lst_player)
				player_select = lst_player[player_index]
			if event.key == pygame.K_UP:
				animation_index -= 1
				if animation_index <0: animation_index += len(animation_buttons)
				for button in animation_buttons:
					if button.text == animation_select:
						button.deselect()
				animation_buttons[animation_index].select()
				animation_select = animation_buttons[animation_index].text	
			if event.key == pygame.K_DOWN:
				animation_index += 1
				animation_index %= len(animation_buttons)
				for button in animation_buttons:
					if button.text == animation_select:
						button.deselect()
				animation_buttons[animation_index].select()
				animation_select = animation_buttons[animation_index].text	
			if event.key == pygame.K_SPACE:
				select_fx.play()
				game_start = True
				p_type = type(player_select).__name__.lower()
				 
		if event.type == pygame.MOUSEBUTTONDOWN and select_player:
			for button in animation_buttons:
				if button.rect.collidepoint(event.pos):
					for b in animation_buttons:
						b.deselect()
					button.select()
					animation_select = button.text

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_UP:
				moving_up = False
			if event.key == pygame.K_DOWN:
				moving_down = False
		
		gui_manager.process_events(event)

	if not game_start and not select_player:
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
			select_player = True  # add
			main_menu = False  # add

		if os.path.exists(f'./Data/save_game'):
			buttons.append(load_btn)
			if load_btn.draw(win):
				check = load_data_continue_pre_game()
				try:
					if check:
						last_time = time() # add
						world_data, level_length, w = reset_level(level)
						game_start = True
						main_menu = False
						bg_scroll = 0
						start_time = pygame.time.get_ticks() - status['time_play']*1000
						if p_class == Ignis:
							p_reload_time = float(config['ignis']['reload_time']) * (1 - 0.2 * ((100 - p.health)//20))
					else:
						os.remove(f'./Data/save_game')
				except:
					os.remove(f'./Data/save_game')

		if scoreboard_btn.draw(win):
			scoreboard_page = True
			main_menu= False

		if controls_btn.draw(win):
			controls_page = True
			main_menu = False

		if exit_btn.draw(win):
			running = False

		buttons.append(play_btn)
		buttons.append(scoreboard_btn)
		buttons.append(controls_btn)
		buttons.append(exit_btn)

	elif select_player:
		MessageBox(win, pygame.font.SysFont('Arial', 15), "", lst_info_player[player_index], 267, 265, 0, HEIGHT//2)
		select_player_msg.update()

		for animation_button in animation_buttons:
			animation_button.draw(win)
	
		counter_select += 1
		if counter_select % 7 == 0:
			if animation_select == "Idle":
				player_select.idle_index = (player_select.idle_index + 1) % len(player_select.idle_list)	
				player_select.image = player_select.idle_list[player_select.idle_index]
			elif animation_select == "Attack":
				player_select.attack_index = (player_select.attack_index + 1) % len(player_select.attack_list)	
				player_select.image = player_select.attack_list[player_select.attack_index]
			elif animation_select == "Walk":
				player_select.walk_index = (player_select.walk_index + 1) % len(player_select.walk_right)	
				player_select.image = player_select.walk_right[player_select.walk_index]
			elif animation_select == "Dead":
				player_select.death_index = (player_select.death_index + 1) % len(player_select.death_list)	
				player_select.image = player_select.death_list[player_select.death_index]

		if player_index == 3:
			player_select.image = pygame.transform.scale(player_select.image, (150, 150))
		else:
			player_select.image = pygame.transform.scale(player_select.image, (120, 120))

		rect = pygame.Rect(WIDTH // 2 - 100,  80, 200, 200)
		pygame.draw.rect(win, (52, 53, 95), rect) # nền select player
		pygame.draw.rect(win, (255, 0, 0), rect, 1) # Khung đỏ

		text = pygame.font.Font(None, 30).render(type(player_select).__name__, True, (255, 255, 255))
		text_rect = text.get_rect(midbottom=(rect.centerx, rect.bottom))
		win.blit(text, text_rect)

		player_select.rect = player_select.image.get_rect(center=rect.center)
		win.blit(player_select.image, player_select.rect)

		if right_btn.draw(win):
			player_index += 1
			player_index %= len(lst_player)
			player_select = lst_player[player_index]
		if left_btn.draw(win):
			player_index -= 1
			if player_index == -1:
				player_index += len(lst_player)
			player_select = lst_player[player_index]
			
		if select_btn.draw(win):
			game_start = True
			select_fx.play()
			p_type = type(player_select).__name__.lower()

		if main_menu_btn.draw(win):
			select_player = False
			main_menu = True

		if game_start:
			select_player = False
			world_data, level_length, w = reset_level(level)
			last_time = time() # add
			start_time = pygame.time.get_ticks()
			p, moving_left, moving_right = reset_player()
			# p2 = reset_player()[0]
			main_menu = False
			bg_scroll = 0

			status['character'] =  p_type.title()
			status['level'] = level
		
	elif about_page:
		MessageBox(win, about_font, 'GhostBusters', info)
		if main_menu_btn.draw(win):
			about_page = False
			main_menu = True

	elif scoreboard_page:
		draw_scoreboard(win)
		if main_menu_btn.draw(win):
			scoreboard_page = False
			main_menu = True
		buttons.append(main_menu_btn)
	
	elif controls_page:
		left_key.update()
		right_key.update()
		up_key.update()
		space_key.update()
		g_key.update()
		p_key.update()
		q_key.update()
		if main_menu_btn.draw(win):
			controls_page = False
			main_menu = True
		buttons.append(main_menu_btn)

	elif exit_page:
		pass

	elif game_won:
		if rank == None:
			draw_scoreboard(win)
			game_won_no_rank_msg.update()
			if main_menu_btn.draw(win):
				if os.path.exists(f'./Data/save_game'):
					os.remove(f'./Data/save_game')
				status = status_c
				game_won = False
				main_menu = True
				level = 1
		else:
			if enter_name:
				rect = pygame.Rect(140,100,360,300)
				pygame.draw.rect(win, (52, 53, 95), rect)
				enter_your_name_msg.update()
				gui_manager.update(pygame.time.Clock().tick(45) / 1000.0)
				gui_manager.draw_ui(win)
				text_input.update(pygame.time.Clock().tick(45) / 1000.0)
			else:
				draw_scoreboard(win,rank)
				if main_menu_btn.draw(win):
					if os.path.exists(f'./Data/save_game'):
						os.remove(f'./Data/save_game')
					status = status_c
					game_won = False
					main_menu = True
					level = 1

	elif game_pause:
		paused_msg.update()
		status_text = str(status).replace(',',"\n").replace('}','').replace('{','').replace("'",'').title()
		MessageBox(win, about_font,"Status", status_text, 200,284,100,265)
		if continue_btn.draw(win):
			game_pause = False
			game_start = True
			last_time = time() 
			start_time += pygame.time.get_ticks() - pause_time 
		if quit_btn.draw(win):
			game_pause = False
			main_menu = True
			game_start = False
			last_time = time() 
			save_data_game()
			start_time += pygame.time.get_ticks() - pause_time 

		buttons.append(continue_btn)
		buttons.append(quit_btn)
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
		# p2.update(False,False,w) 
		# p2.draw(win)
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

		if pygame.sprite.spritecollide(p, diamond_group, True):
			diamond_fx.play()
			score += 100
			pass

		if pygame.sprite.spritecollide(p, exit_group, False):
			next_level_fx.play()
			level += 1
			if level <= MAX_LEVEL:
				world_data, level_length, w = reset_level(level)
				p.revival(250, 50, p.health)
				p.grenades += 1
				screen_scroll = 0
				bg_scroll = 0
				status['level'] = level
				status['score'] = score
				status['grenades'] = p.grenades
				status['health'] = p.health
				print("Pass level", status)
			else:
				status['score'] = score
				user_new = User('a', status['character'],status['score'],status['time_play'],status['die'])
				rank = Scoreboard.add_user(user_new)
				if rank!=None:
					enter_name = True
				game_won = True

		potion = pygame.sprite.spritecollide(p, potion_group, False)
		if potion:
			if p.health < 100:
				potion[0].kill()
				add_health = min(15, 100 - p.health)
				p.health += add_health
				health_fx.play()
				p.add_notice(f"+{add_health}",1,win)
				
				if p_class == Ignis:
					p_reload_time = float(config['ignis']['reload_time']) * (1 - 0.2 * ((100 - p.health)//20))

		for bullet in bullet_group:
			enemy =  pygame.sprite.spritecollide(bullet, enemy_group, False)
			if enemy and bullet.type == 1 and enemy[0].on_death_bed == False:
				if p_class != Knight or (p_class == Knight and (enemy[0].id_get_damage != bullet.id or \
						    (enemy[0].direct_get_damge != bullet.state_direction and bullet.id == enemy[0].id_get_damage) )) :
					try:
						enemy[0].direct_get_damge = bullet.state_direction
						enemy[0].id_get_damage = bullet.id
					except:
						pass 

					get_dame = bullet.dame
					if enemy[0].health <= 0 and enemy[0].on_death_bed == False :
						score += 300
						enemy[0].on_death_bed = True
					if hasattr(bullet,'skill1'): # sword
						if bullet.skill1 == True: 
							p.health += (100-p.health)//10
							p.add_notice(f"+{(100-p.health)//10}",1,win)
						else:
							add_health = min(100*7//100, 100 - p.health)
							p.health += add_health
							p.add_notice(f"+{add_health}",1,win)
					if hasattr(bullet, 'crit'): # crit
						if random.randint(1, 100) <= bullet.crit:
							get_dame*=2
							p.add_notice("crit",1,win)
					
					enemy[0].hit = True
					enemy[0].get_hit(get_dame)

				if p_class != Knight:
					bullet.kill()

			if bullet.rect.colliderect(p):
				if bullet.type == 2:
					if not p.hit:
						p.hit = True
						if p_class == Knight:
							p.health -= 10
							p.add_notice("-10",2,win)
						else:
							p.health -= 20
							p.add_notice("-20",2,win)
						print(p.health)
					bullet.kill()

		# drawing variables *******************************************************
		
		pygame.draw.rect(win, (255,255,255) , (6, 6, 40, 40), border_radius=5)
		win.blit(img_avt,(6, 6, 40, 40))

		health_font = pygame.font.Font(None, 26)
		health_text = health_font.render(str(p.health), True, (0, 0, 255))
		pygame.draw.rect(win, (128,128,128) , (49, 8, 100, 20), border_radius=5)

		if p.alive:
			color = (0,255,0)
			if p.health <= 40:
				color = (255, 0, 0)
			pygame.draw.rect(win, color, (49, 8, p.health, 20), border_radius=5)
		pygame.draw.rect(win, (255, 255, 255), (49, 8, 100, 20), 2, border_radius=5)

		win.blit(health_text, (50 - health_text.get_width()/2 + 49, 10))

		for i in range(p.grenades):
			pygame.draw.circle(win, (200, 200, 200), (20 + 15*i + 49, 40), 5)
			pygame.draw.circle(win, (255, 50, 50), (20 + 15*i + 49, 40), 4)
			pygame.draw.circle(win, (0, 0, 0), (20 + 15*i + 49, 40), 1)
		
		draw_image_skill(win,delta_time)

		if p.health <= 0 and p.revive:
			screen_scroll = 0
			bg_scroll = 0
			world_data, level_length, w = reset_level(level)
			p.revival(250, 50)
			score = status['score']
			status['health'] = p.health
			status['die'] += 1
			print("Die",status)

		last_time = time()

			# draw die 
		text = pygame.font.Font(None, 36).render(\
			f"Die: {status['die']}", True, (255, 0, 0))
		text_rect = text.get_rect(center=(WIDTH - text.get_width(), 20))
		win.blit(text, text_rect)
			# draw time
		status['time_play'] = time_play = (pygame.time.get_ticks() - start_time)// 1000
		text = pygame.font.Font(None, 36).render(\
			f"{ datetime.timedelta(seconds= time_play)}", True, (255, 255, 255))
		text_rect = text.get_rect(center=(WIDTH//2, 20))
		win.blit(text, text_rect)
			# draw score
		text = pygame.font.Font(None, 36).render(\
			f"Score: {score}", True, (255, 255, 255))
		text_rect = text.get_rect(center=(80, HEIGHT - text.get_height()) )
		win.blit(text, text_rect)
			# draw level
		text = pygame.font.Font(None, 36).render(\
			f"Level: {status['level']}", True, (255, 255, 255))
		text_rect = text.get_rect(center=(WIDTH - text.get_width() + 20, HEIGHT - text.get_height()) )
		win.blit(text, text_rect)

	if not game_start and not select_player:
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