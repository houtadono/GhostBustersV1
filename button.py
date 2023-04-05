import pygame 

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
					Button.last_click_time = current_time

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))
		if self.text:
			self.image.blit(self.text, (self.width//2 - self.xoff, self.height//2 - self.yoff))

		return action 