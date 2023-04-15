import pygame

WIDTH, HEIGHT =640, 484

class Text:
	''' This class returns an image '''
	def __init__(self, font, font_size):
		self.font = pygame.font.Font(font, font_size)

	def render(self, text, color):
		image = self.font.render(text, False, color)
		return image

class Message:
	''' This class blits an image at given position '''
	def __init__(self, x, y, size, text, font, color, win):
		self.win = win
		self.color = color
		self.x, self.y = x, y
		if not font:
			self.font = pygame.font.SysFont("Verdana", size)
			anti_alias = True
		else:
			self.font = pygame.font.Font(font, size)
			anti_alias = False
		self.image = self.font.render(text, anti_alias, color)
		self.rect = self.image.get_rect(center=(x,y))
		if self.color == (200, 200, 200):
				self.shadow_color = (255, 255, 255)
		else:
			self.shadow_color = (54,69,79)
		self.shadow = self.font.render(text, anti_alias, self.shadow_color)
		self.shadow_rect = self.image.get_rect(center=(x+2,y+2))
		
	def update(self, text=None, color=None, shadow=True):
		if text:
			if not color:
				color = self.color
			self.image = self.font.render(f"{text}", False, color)
			self.rect = self.image.get_rect(center=(self.x,self.y))
			self.shadow = self.font.render(f"{text}", False, self.shadow_color)
			self.shadow_rect = self.image.get_rect(center=(self.x+2,self.y+2))
		if shadow:
			self.win.blit(self.shadow, self.shadow_rect)
		self.win.blit(self.image, self.rect)

class BlinkingText(Message):
	''' This class creates a blinking text image surface '''
	def __init__(self, x, y, size, text, font, color, win):
		super(BlinkingText, self).__init__(x, y, size, text, font, color, win)
		self.index = 0
		self.show = True

	def update(self):
		self.index += 1
		if self.index % 40 == 0:
			self.show = not self.show

		if self.show:
			self.win.blit(self.image, self.rect)

def MessageBox(win, font, name, text):
	''' This class creates a message box and automatically fills the text '''
	WIDTH = 640
	HEIGHT = 284
	x = 35
	y = 65 # depends on message box location
	pygame.draw.rect(win, (255,255,255), (25, 25, WIDTH - 40, HEIGHT - 84), border_radius=10)
	for word in text.split(' '):
		rendered = font.render(word, 0, (0,0,0))
		width = rendered.get_width()
		if x + width >= WIDTH:
			x = 35
			y += 25
		win.blit(rendered, (x, y))
		x += width + 5


	title = font.render(name, 0, (0,0,0))
	title_width = 120
	pygame.draw.rect(win, (255,255,255), (WIDTH // 2 - title_width // 2 + 10, 10, 
					title_width, 30), border_radius=10)
	win.blit(title, (WIDTH // 2 - title.get_width()//2 + 10, 10))

def MessageBox(win, font, name, text, width=640, height=0, x=35, y=65, color=(0,0,0)):
	''' This class creates a message box and fills the text with line breaks'''
    
	lines = text.split('\n')

	message_width = max( font.render(line, 1, color).get_width() + 20 for line in lines )
	message_height = len(lines) * 25 + 20
	ww = max(width, message_width + 20)
	hh = message_height + 20
	if height!=0: hh = height
	background_rect = pygame.Rect(x - 10, y - 10, ww, hh)
	pygame.draw.rect(win, (255,255,255,0), background_rect, border_radius=10)

	lines = text.split('\n')
	for i, line in enumerate(lines):
		words = line.split(' ')
		line_x, line_y = x + 10, y + 10 + i*25
		for word in words:
			rendered = font.render(word, 1, color)
			word_width = rendered.get_width()
			# if line_x + word_width >= x + width - 10:
			# 	line_x = x + 10
			# 	line_y += 25
			win.blit(rendered, (line_x, line_y))
			line_x += word_width + 5
	if name != "":
		title = font.render(name, 0, (0,0,0))
		title_width = title.get_width() + 20
		rect_title = pygame.Rect(x + message_width // 2 - title_width // 2, y - 40, title_width, 30)
		pygame.draw.rect(win, (255,255,255), rect_title, border_radius=10)
		win.blit(title, (rect_title.centerx - title.get_width()//2, rect_title.centery - title.get_height()//2 ))
