import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from utility import import_csv_layout,import_folder
from random import choice,randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from projectile import ItemPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):
        #get pygame display surface
        self.display_surface=pygame.display.get_surface()
        #sprite groups definitions
        self.visible_sprites=YSortCameraGroup()
        self.obstacle_sprites=pygame.sprite.Group()

        self.game_paused=False
        self.xpos=0
        self.ypos=0

        #attack sprites
        self.current_attack=None
        self.attack_sprites=pygame.sprite.Group() # for weapons and projectiles
        self.attackable_sprites=pygame.sprite.Group() # for attackable objects, eg. monsters, grass

        #sprite setup
        self.create_map()

        # ui
        self.ui=UI()
        self.upgrade=Upgrade(self.player)

        # particles
        self.animation_player=AnimationPlayer()
        self.magic_player=ItemPlayer(self.animation_player)

    def create_map(self):
        #        # col - current tile being iterated over
        #        # case for each type of data in WORLD_MAP
        #        if col=='x':
        #            Tile((x,y),[self.visi  ble_sprites,self.obstacle_sprites])
        #        if col=='p':
        #            self.player=Player((x,y),[self.visible_sprites],self.obstacle_sprites)
        layout={
            'boundary':import_csv_layout('../graphics/maps/beal_FloorBlocks.csv'),
            'grass':import_csv_layout('../graphics/maps/map_Grass.csv'),
            'object':import_csv_layout('../graphics/maps/beal_Objects.csv'),
            'entities':import_csv_layout('../graphics/maps/beal_Entities.csv')

        }
        graphics={
            'grass':import_folder('../graphics/grass'),
            'objects': import_folder('../graphics/objects')
        }
        for style,layout in layout.items():
            for row_index,row in enumerate(layout):
                for col_index,col in enumerate(row):
                    if col!='-1':
                        x=col_index*TILESIZE
                        self.xpos=x
                        y=row_index*TILESIZE
                        self.ypos=x
                        if style=='boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style=='grass':
                            rand_grass_image=choice(graphics['grass']).convert()
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',rand_grass_image)
                        if style=='object':
                            surf=graphics['objects'][int(col)]
                            #Tile((x,y),[self.obstacle_sprites],'invisible')
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf) # add surf for actual objects

                        if style=='entities':
                            if col=='394':
                                self.player=Player(
                                                    (x,y),
                                                    [self.visible_sprites],self.obstacle_sprites,
                                                    self.create_attack,self.destroy_attack,
                                                    self.create_proj)
                            else: # check which enemy the entity that isnt player is
                                if col=='390': monster_name='flying_eye'
                                elif col=='391': monster_name='mushroom'
                                elif col=='392': monster_name='goblin'
                                else: monster_name='skeleton'
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visible_sprites,self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_xp)

    def create_attack(self):
        self.current_attack=Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def create_proj(self,item,strength,cost):
        if item=='hp_potion':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])
        if item=='spike':
            self.magic_player.throw(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack=None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites=pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False) # if sprite collides with any sprite in the group
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type=='grass':
                            pos=target_sprite.rect.center
                            offset=pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos-offset,[self.visible_sprites])
                            target_sprite.kill()
                        elif target_sprite.sprite_type=='enemy':
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health-=amount
            self.player.vulnerable=False
            self.player.hurt_time=pygame.time.get_ticks()
            #self.animation_player.create_particles(attack_type,self.player.rect.center,self.visible_sprites)
            #for animation effect created by enemy attacks (unecessary with current enemy sprites)

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def add_xp(self,amount):
        self.player.xp+=amount

    def toggle_menu(self):
        self.game_paused=not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player) # draw world
        self.ui.display(self.player)
        #update and draw game
        if self.game_paused:
            self.upgrade.display()
            print(self.visible_sprites)
            # display upgrade menu
        else:
            # run game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.half_width=self.display_surface.get_size()[0]//2
        self.half_height=self.display_surface.get_size()[1]//2
        self.offset=pygame.math.Vector2(100,200)

        #creating floor
        self.floor_surface=pygame.image.load('../graphics/map_assets/12800_ground_map.png').convert()
        self.floor_rect=self.floor_surface.get_rect(topleft=(0,0))
    
    def custom_draw(self,player):

        #getting offset
        self.offset.x=player.rect.centerx-self.half_width
        self.offset.y=player.rect.centery-self.half_height

        #drawing floor
        floor_offset_pos=self.floor_rect.topleft-self.offset
        self.display_surface.blit(self.floor_surface,floor_offset_pos)

        for sprite in sorted(self.sprites(),key=lambda sprite:sprite.rect.centery):
            offset_pos=sprite.rect.topleft-self.offset
            self.display_surface.blit(sprite.image,offset_pos) # draw sprites on screen

    def enemy_update(self,player):
        enemy_sprites=[sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type=='enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)