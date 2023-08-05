import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        #get pygame display surface
        self.display_surface=pygame.display.get_surface()
        #sprite groups definitions
        self.visible_sprites=YSortCameraGroup()
        self.obstacle_sprites=pygame.sprite.Group()

        #sprite setup
        self.create_map()
    
    def create_map(self):
        for row_index,row in enumerate(WORLD_MAP):
            for col_index,col in enumerate(row):
                x=col_index*TILESIZE
                y=row_index*TILESIZE
                # col - current tile being iterated over
                # case for each type of data in WORLD_MAP
                if col=='x':
                    Tile((x,y),[self.visible_sprites,self.obstacle_sprites])
                if col=='p':
                    self.player=Player((x,y),[self.visible_sprites],self.obstacle_sprites)


    def run(self):
        #update and draw game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.half_width=self.display_surface.get_size()[0]//2
        self.half_height=self.display_surface.get_size()[1]//2
        self.offset=pygame.math.Vector2(100,200)
    
    def custom_draw(self,player):
        #getting offset
        self.offset.x=player.rect.centerx-self.half_width
        self.offset.y=player.rect.centery-self.half_height
        #camwera movement
        for sprite in self.sprites():
            offset_pos=sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image,offset_pos)