import pygame 


button_click_fx = pygame.mixer.Sound('Sounds/button_click.mp3')

class Button():
	last_click_time = 0
	click_delay = 500
	def __init__(self,x, y, image, scale, text=None, xoff=None):
		self.width = int(image.get_width() * scale)
		self.height = int(image.get_height() * scale)
		self.image = pygame.transform.scale(image, (self.width, self.height))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

		self.text = None
		if text:
			self.text = text
			if xoff:
				self.xoff = xoff
			else:
				self.xoff = self.text.get_width() // 2
			self.yoff = self.text.get_height() // 2

		self.clicked = False
		self.shot = False

	def draw(self, surface):
		action = False
		if self.shot:
			button_click_fx.play()
			self.shot =False
			return True
		#get mouse position
		pos = pygame.mouse.get_pos()
		current_time = pygame.time.get_ticks()
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False :
				if current_time - self.last_click_time > self.click_delay:
					action = True
					self.clicked = True
					button_click_fx.play()
					Button.last_click_time = current_time

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))
		if self.text:
			self.image.blit(self.text, (self.width//2 - self.xoff, self.height//2 - self.yoff))

		return action 
class RadioButton:
	def __init__(self, x, y, width, height, text, selected=False):
		self.rect = pygame.Rect(x, y, width, height)
		self.border_colors = (255, 0, 0)
		self.fill_color = (255, 255, 0)
		self.text = text
		self.selected = selected

	def draw(self, screen):
		# Draw border
		pygame.draw.rect(screen, self.border_colors[0] if not self.selected else self.border_colors[1], self.rect, 4)

		# Draw fill color
		pygame.draw.rect(screen, self.fill_color, pygame.Rect(self.rect.left + 4, self.rect.top + 4, self.rect.width - 8, self.rect.height - 8))

        # Draw text
		color_text = (0,0,0) if not self.selected else (255,0,0)
		text_surface = pygame.font.Font(None, 24).render(self.text, True, color_text)
		text_rect = text_surface.get_rect(center=self.rect.center)
		screen.blit(text_surface, text_rect)

	def select(self):
		button_click_fx.play()
		self.selected = True

	def deselect(self):
		self.selected = False
