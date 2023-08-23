import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface=pygame.Surface((TILESIZE,TILESIZE)),id=200):
        super().__init__(groups)
        self.sprite_type=sprite_type
        x_offset=X_HITBOX_OFFSET[str(id)]
        y_offset=HITBOX_OFFSET[str(id)]
        self.image=surface.convert_alpha()
        if sprite_type=='object':
            #offset of larger sprites
            self.rect=self.image.get_rect(topleft=(pos[0],pos[1]-TILESIZE))
        else:
            self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(-x_offset,-y_offset) #set hitbox within image instead of rectangle