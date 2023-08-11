import pygame,sys
from settings import *
from level import Level

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Hexham's Awakening")
        pygame.display.set_icon(pygame.image.load('../graphics/logo/ha_logo.png').convert_alpha())
        self.clock = pygame.time.Clock()

        self.level=Level()
    
    def run(self):
        #game loop
        while True:
            #keys pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #to prevent errors after closing display
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_TAB or event.key==pygame.K_ESCAPE:
                        self.level.toggle_menu()
            #graphics drawn
            self.screen.fill(BLACK)
            self.level.run()

            #update display
            pygame.display.update()
            self.clock.tick(FPS)

if __name__== '__main__':
    game = Game()
    game.run()