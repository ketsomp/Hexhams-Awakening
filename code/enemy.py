import pygame
from settings import *
from entity import Entity
from utility import *
import math

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites):
        # general
        super().__init__(groups)
        self.sprite_type='enemy'

        # graphics
        self.import_graphics(monster_name)
        self.status='idle'
        self.image=self.animations[self.status][self.frame_index]
        self.rect=self.image.get_rect(topleft=pos)

        # enemy stats (dict from settings converted to attributes using monster_info)
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.aggro_radius = monster_info['aggro_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack=True
        self.attack_time=None
        self.attack_cooldown=400

        #movement
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(0,-10)
        self.obstacle_sprites=obstacle_sprites

    def import_graphics(self,name):
        self.animations={'idle':[],'move':[],'attack':[]}
        main_path=f"../graphics/monsters/{name}/"
        for animation in self.animations.keys():
            self.animations[animation]=import_folder(main_path+animation)

    def get_player_dist_dir(self,player):
        enemy_vector=pygame.math.Vector2(self.rect.center)
        player_vector=pygame.math.Vector2(player.rect.center)
        distance = (player_vector-enemy_vector).magnitude()
        if distance>0:
            direction=(player_vector-enemy_vector).normalize()
        else:
            direction=pygame.math.Vector2() # if player and enemy in same location set direction to 0,0
        return (distance,direction)
    
    # set current state of enemy
    def get_status(self,player):
        distance=self.get_player_dist_dir(player)[0]
        if distance<=self.attack_radius and self.can_attack:
            if self.status!='attack':
                self.frame_index=0
            self.status='attack'
        elif distance<=self.aggro_radius:
            self.status='move'
        else:
            self.status='idle'

    def actions(self,player):
        if self.status=='attack':
            print('attack')
            self.attack_time=pygame.time.get_ticks()
        elif self.status=='move':
            self.direction=self.get_player_dist_dir(player)[1] # get direction from method
        else:
            self.direction=pygame.math.Vector2() # if player moves out of aggro radius, enemy stops moving

    def animate(self):
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed # from entity inheritance
        if self.frame_index>=len(animation):
            if self.status=='attack':
                self.can_attack=False
            self.frame_index=0

        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)

    def attack_cd(self):
        if not self.can_attack:
            current_time=pygame.time.get_ticks()
            if current_time-self.attack_time>=self.attack_cooldown:
                self.can_attack=True

    def update(self):
        self.move(self.speed)
        self.animate()
        self.attack_cd()
    
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)