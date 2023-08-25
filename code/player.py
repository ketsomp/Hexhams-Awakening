import pygame
from settings import *
from utility import import_folder
from entity import Entity
from time import sleep

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_proj):
        super().__init__(groups)
        self.display=pygame.display.get_surface()
        self.image=pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(-6,HITBOX_OFFSET['player']) #set hitbox within image instead of rectangle
        self.pos=pos

        #graphics
        self.import_player_assets()
        self.status='down'

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
        self.stats = {'health': 100,'energy':60,'attack': 10,'power': 4,'speed': 6*SPEED_OFFSET,'stamina':30}
        self.max_stats = {'health': 300, 'energy': 140, 'attack': 20, 'power' : 10, 'speed': 10,'stamina':50}
        self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'power' : 100, 'speed': 100,'stamina':100}
        self.health=self.stats['health']
        self.energy=self.stats['energy']
        self.xp=500
        self.speed=self.stats['speed']
        self.stamina=self.stats['stamina']
        self.attack_stat=self.stats['attack']
        self.power_stat=self.stats['power']

        #movement
        self.attacking=False
        self.attack_cd=400
        self.attack_duration=None
        self.sprinting=False
        self.sprinting_speed=self.speed*1.5

        # damage timer
        self.vulnerable=True
        self.hurt_time=None
        self.invulnerability_duration=500

        self.obstacle_sprites=obstacle_sprites

        # sfx
        self.weapon_attack_sfx=pygame.mixer.Sound('../audio/sword.wav')
        self.weapon_attack_sfx.set_volume(0.2)

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
                self.weapon_attack_sfx.play()
            
            # proj input
            if keys[pygame.K_f]:
                self.attacking=True
                self.attack_duration=pygame.time.get_ticks()

                style=list(proj_data.keys())[self.proj_index]
                strength=list(proj_data.values())[self.proj_index]['strength']+self.power_stat
                cost=list(proj_data.values())[self.proj_index]['cost']

                self.create_proj(style,strength,cost)

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
                self.proj=list(proj_data.keys())[self.proj_index]

            # sprinting
            if keys[pygame.K_LSHIFT] and self.stamina>0:
                self.sprinting=True
                self.sprint_end_cd=pygame.time.get_ticks()
            else:
                self.sprinting=False


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

        # player spawn time cd
        if not self.vulnerable:
            if current_time-self.hurt_time>=self.invulnerability_duration:
                self.vulnerable=True

    def animate(self):
        animation=self.animations[self.status]

        # loop over frame_index
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(animation):
            self.frame_index=0

        # set image
        self.image=animation[int(self.frame_index)].convert_alpha()
        self.rect=self.image.get_rect(center=self.hitbox.center)

        # flicker when hit
        if not self.vulnerable:
            alpha=self.wave_value() #flicker
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
   
    def get_weapon_damage(self):
        base_damage=self.attack_stat
        weapon_damage=weapon_data[self.weapon]['damage']
        return base_damage+weapon_damage
    
    def get_proj_damage(self):
        base_damage=self.power_stat
        spike_damage=proj_data[self.proj]['strength']
        return base_damage+spike_damage

    def get_value_by_index(self,index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self,index):
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self): # constant energy recovery after casting spells
        if self.energy<self.stats['energy']:
            self.energy+=0.01*self.power_stat # recovery rate updated by base power stat
        else:
            self.energy=self.stats['energy']

    def is_sprinting(self):
        if self.sprinting and self.stamina>0:
            self.stamina-=0.1
            self.speed=self.sprinting_speed
        elif not self.sprinting and self.stamina<self.stats['stamina']:
            self.stamina+=0.075
            self.speed=self.sprinting_speed*0.5

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
        self.is_sprinting()