import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface=pygame.display.get_surface()
        self.font=pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect=pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect=pygame.Rect(10,35,ENERGY_BAR_WIDTH,BAR_HEIGHT) # (l,t,b,h)

    def display(self,player):
        pygame.draw.rect(self.display_surface,BLACK,self.health_bar_rect)