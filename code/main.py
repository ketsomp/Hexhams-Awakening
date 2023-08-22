import pygame,sys
from settings import *
from level import Level

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

class Game:
    def __init__(self):
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # ,flags,16
        pygame.display.set_caption("Hexham's Awakening")
        pygame.display.set_icon(pygame.image.load('../graphics/logo/ha_logo.png').convert_alpha())
        self.clock = pygame.time.Clock()
        self.font=pygame.font.Font(UI_FONT,20)

        self.screen.fill(BG_COLOR)


        self.level=Level()

        # ost
        self.main_ost=pygame.mixer.Sound('../audio/ost.ogg')
        self.starting_ost=pygame.mixer.Sound('../audio/starting_screen.ogg')
        self.main_ost.set_volume(0.5)
        self.starting_ost.set_volume(0.5)
        self.starting_ost.play(loops=-1)

    def render(self):
        self.text=self.font.render(str(round(self.clock.get_fps())),1,(255,255,255)) # render fps
        self.screen.blit(self.text,(WIDTH-50,0))  
    
    def run(self):
        #game loop 
        while True:
            if not self.level.started:
                self.level.start_screen()
                self.level.draw_game_font()
                if self.level.start_button.draw(self.screen):
                    self.level.started=True
                    self.starting_ost.stop()
                    self.main_ost.play(loops=-1)
                if self.level.quit_button.draw(self.screen):
                    pygame.quit()
                    sys.exit()
            #keys pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() #to prevent errors after closing display
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_TAB:
                        self.level.toggle_menu()
                    if event.key==pygame.K_ESCAPE:
                        self.level.paused=not self.level.paused

            #graphics drawn
            if self.level.started:
                self.level.run()
                self.render()

            #update display
            pygame.display.update()
            self.clock.tick(FPS)


if __name__== '__main__':
    game = Game()
    game.run()