import pygame
from settings import *
from entity import Entity
from utility import *
class Enemy(Entity):
    def __init__(self,monster_name,pos,groups):
        # general
        super().__init__(groups)
        self.sprite_type='enemy'

        # graphics
        self.import_graphics(monster_name)
        self.status='idle'
        self.image=self.animations[self.status][self.frame_index]
        self.rect=self.image.get_rect(topleft=pos)

    def import_graphics(self,name):
        self.animations={'idle':[],'move':[],'attack':[]} # 4:22:46
        main_path=f"../graphics/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation]=import_folder(main_path+animation)