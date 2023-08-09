import pygame
from settings import *
from utility import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_proj):
        super().__init__(groups)
        self.image=pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(-35,-26) #set hitbox within image instead of rectangle

        #graphics
        self.import_player_assets()
        self.status='down'

        #movement
        self.attacking=False
        self.attack_cd=400
        self.attack_duration=None

        #weapon
        self.create_attack=create_attack
        self.destroy_attack=destroy_attack
        self.weapon_index=0 # id of weapon
        self.weapon=list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon=True
        self.weapon_switch_cd=None

        self.switch_duration_cd=200

        # projectiles
        self.create_proj=create_proj
        self.proj_index=0
        self.proj=list(proj_data.keys())[self.proj_index]
        self.can_switch_proj=True
        self.proj_switch_cd=None


        #stats
        self.stats = {'health': 100,'energy':60,'attack': 10,'power': 4,'speed': 6}
        self.health=self.stats['health']
        self.energy=self.stats['energy']
        self.xp=696
        self.speed=self.stats['speed']

        self.obstacle_sprites=obstacle_sprites

    def import_player_assets(self):
        character_path='../graphics/player/'
        self.animations = {'up':[],'down':[],'left':[],'right':[],
                           'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
                           'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        for animation in self.animations.keys():
            full_path=character_path+animation
            self.animations[animation]=import_folder(full_path)

    def input(self):
        if not self.attacking:
            keys=pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_w]:
                self.direction.y=-1
                self.status='up'
            elif keys[pygame.K_s]:
                self.direction.y=1
                self.status='down'
            else:
                self.direction.y=0
            
            if keys[pygame.K_a]:
                self.direction.x=-1
                self.status='left'
            elif keys[pygame.K_d]:
                self.direction.x=1
                self.status='right'
            else:
                self.direction.x=0

            #attack input
            if keys[pygame.K_SPACE]:
                self.attacking=True
                self.attack_duration=pygame.time.get_ticks()
                self.create_attack()
            
            # proj input
            if keys[pygame.K_RETURN]:
                self.attacking=True
                self.attack_duration=pygame.time.get_ticks()

                style=list(proj_data.keys())[self.proj_index]
                strength=list(proj_data.values())[self.proj_index]['strength']+self.stats['power']
                count=list(proj_data.values())[self.proj_index]['count']

                self.create_proj(style,strength,count)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon=False
                self.weapon_switch_cd=pygame.time.get_ticks()

                # make sure cycle between weapons instead of going out of range
                if self.weapon_index<len(list(weapon_data.keys()))-1:
                    self.weapon_index+=1
                else:
                    self.weapon_index=0
                self.weapon=list(weapon_data.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_proj:
                self.can_switch_proj=False
                self.proj_switch_cd=pygame.time.get_ticks()

                # make sure cycle between projectiles instead of going out of range
                if self.proj_index<len(list(proj_data.keys()))-1:
                    self.proj_index+=1
                else:
                    self.proj_index=0
                self.proj=list(weapon_data.keys())[self.proj_index]

    def get_status(self):
        # idle
        if self.direction.x==0 and self.direction.y==0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status+='_idle'
        if self.attacking:
            self.direction.x=self.direction.y=0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status=self.status.replace('_idle','_attack')
                else:
                    self.status+='_attack'
        else:
                if 'attack' in self.status:
                    self.status=self.status.replace('_attack','')

    
    def cooldowns(self):
        current_time=pygame.time.get_ticks()
        if self.attacking:
            if current_time-self.attack_duration>=self.attack_cd:
                self.attacking=False
                self.destroy_attack() 
        
        # weapon switch cooldown
        if not self.can_switch_weapon:
            if current_time-self.weapon_switch_cd>=self.switch_duration_cd:
                self.can_switch_weapon=True

        # projectile switch cooldown
        if not self.can_switch_proj:
            if current_time-self.proj_switch_cd>=self.switch_duration_cd:
                self.can_switch_proj=True

    def animate(self):
        animation=self.animations[self.status]

        # loop over frame_index
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(animation):
            self.frame_index=0

        # set image
        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)
    
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)