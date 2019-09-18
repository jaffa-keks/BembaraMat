import pygame
from inputmng import InputMng
from world import World
from ui import UI

class App:

    def __init__(self):
        self.running = True
        self.display = None
        self.size = self.weight, self.height = 1024, 1024
        pygame.init()
        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Car")
        self.inputmng = InputMng()
        self.world = World(self.inputmng)
        self.ui = UI(self.world.car)
        self.clock = pygame.time.Clock()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        else:
            self.inputmng.on_event(event)
            
    def on_loop(self):
        self.world.update()
    
    def on_render(self):
        self.display.fill((0, 0, 0))
        self.world.render(self.display)
        self.ui.render(self.display)
        pygame.display.flip()
    
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        while( self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(30)
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
