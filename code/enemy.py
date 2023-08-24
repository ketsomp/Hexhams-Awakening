import pygame
from settings import *
from entity import Entity
from utility import *
from time import time

class Enemy(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_xp):
        # general
        super().__init__(groups)
        self.sprite_type='enemy'

        # graphics
        self.import_graphics(monster_name)
        self.status='idle'
        self.image=self.animations[self.status][self.frame_index].convert_alpha()
        self.rect=self.image.get_rect(topleft=pos)

        # enemy stats (dict from settings converted to attributes using monster_info)
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.xp = monster_info['xp']
        self.speed = monster_info['speed']*SPEED_OFFSET
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.aggro_radius = monster_info['aggro_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack=True
        self.attack_time=None
        self.attack_cooldown=monster_info['atk_delay']
        self.damage_play=damage_player
        self.trigger_death_particles=trigger_death_particles
        self.add_xp=add_xp

        # procs
        self.vulnerable=True
        self.hit_time=None
        self.invincibility_duration=300

        #movement
        self.rect=self.image.get_rect(topleft=pos)
        self.hitbox=self.rect.inflate(0,-10)
        self.obstacle_sprites=obstacle_sprites
        self.can_move=True
        self.passive_movement_cd=30
        self.passive_movement_counter=0
        self.passive_movement_bool=1

        # sfx
        self.death_sound=pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound=pygame.mixer.Sound('../audio/hit.wav')
        self.attack_sound=pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.1)
        self.hit_sound.set_volume(0.1)
        self.attack_sound.set_volume(0.2)

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
        elif distance>self.aggro_radius:
            self.status='idle'

    def actions(self,player):
        current_time=pygame.time.get_ticks()
        if self.status=='attack':
            self.attack_time=pygame.time.get_ticks()
            self.attack_sound.play()
            self.damage_play(self.attack_damage,self.attack_type)
        elif self.status=='move':
            self.direction=self.get_player_dist_dir(player)[1] # get direction from method
        else:
            # idling side to side
            if self.can_move:
                self.direction=pygame.math.Vector2((1,0))
            else:
                self.direction=pygame.math.Vector2((-1,0))

    def animate(self):
        animation=self.animations[self.status]
        self.frame_index+=self.animation_speed # from entity inheritance
        if self.frame_index>=len(animation):
            if self.status=='attack':
                self.can_attack=False
            self.frame_index=0

        self.image=animation[int(self.frame_index)]
        self.rect=self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha=self.wave_value() #flicker
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time=pygame.time.get_ticks()
        self.passive_movement_counter+=1
        if self.passive_movement_counter>self.passive_movement_cd:
            self.can_move=not self.can_move
            self.passive_movement_counter=0
            
        if not self.can_attack:
            current_time=pygame.time.get_ticks()
            if current_time-self.attack_time>=self.attack_cooldown:
                self.can_attack=True
                #print('attack,',time())
        if not self.vulnerable:
            if current_time-self.hit_time>=self.invincibility_duration:
                self.vulnerable=True


    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction=self.get_player_dist_dir(player)[1]
            if attack_type=='weapon':
                self.health-=player.get_weapon_damage()
            else: # proj damage
                self.health-=player.get_proj_damage()
            self.hit_time=pygame.time.get_ticks()
            self.vulnerable=False

    def check_death(self):
        if self.health<=0:
            self.kill()
            self.death_sound.play()
            self.add_xp(self.xp)
            self.trigger_death_particles(self.rect.center,self.monster_name) # monster_name as key of particles dict is monster names
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction*=-self.resistance # knockback


    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.cooldowns()
        self.animate()
        self.check_death()
    
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)