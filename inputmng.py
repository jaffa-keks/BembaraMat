import pygame

class InputMng:

    def __init__(self):
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
        self.space = 0
        self.hor = 0
        self.ver = 0
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_b = 0
    
    def on_key_down(self, event):
        self.set_keys()
        
    def on_key_up(self, event):
        self.set_keys()

    def on_mouse_move(self, event):
        self.mouse_x = pygame.mouse.get_pos()[0]
        self.mouse_y = pygame.mouse.get_pos()[1]

    def on_mb_down(self, event):
        self.mouse_b = event.button
        if self.mouse_b == 3:
            self.car.path.append((self.mouse_x, self.mouse_y))
        if self.mouse_b == 2:
            self.car.path = []

    def on_mb_up(self, event):
        self.mouse_b = 0

    def set_keys(self):
        pressed = pygame.key.get_pressed()
        self.up = pressed[pygame.K_UP] or pressed[pygame.K_w]
        self.down = pressed[pygame.K_DOWN] or pressed[pygame.K_s]
        self.left = pressed[pygame.K_LEFT] or pressed[pygame.K_a]
        self.right = pressed[pygame.K_RIGHT] or pressed[pygame.K_d]
        self.space = pressed[pygame.K_SPACE]
        self.hor = -1 if self.left else 1 if self.right else 0
        self.ver = -1 if self.up else 1 if self.down else 0

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.on_key_down(event)
        elif event.type == pygame.KEYUP:
            self.on_key_up(event)
        elif event.type == pygame.MOUSEMOTION:
            self.on_mouse_move(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mb_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_mb_up(event)
        return