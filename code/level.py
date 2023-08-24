import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from utility import import_csv_layout,import_folder,add_outline_to_image
from random import choice,randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from projectile import ItemPlayer
from upgrade import Upgrade
from button import Button
import sys

class Level:
    def __init__(self):

        #get pygame display surface
        self.display_surface=pygame.display.get_surface()
        #sprite groups definitions
        self.visible_sprites=YSortCameraGroup()
        self.obstacle_sprites=pygame.sprite.Group()

         # stop states
        self.game_paused=False # True: if upgrade menu in use
        self.paused=False # True: if game on pause screen
        self.stopped=False # True: if player dies and on death screen

        # map scrolling
        self.xpos=0 # for 
        self.ypos=0

        self.mode=False # True for embedded map, more fps (30), False for individual tile implementation, less fps (25)

        #attack sprites
        self.current_attack=None
        self.attack_sprites=pygame.sprite.Group() # for weapons and projectiles
        self.attackable_sprites=pygame.sprite.Group() # for attackable objects, eg. monsters, grass

        # splash screen setup
        self.started=False
        self.start_img=pygame.image.load('../graphics/map_assets/6400 16x16 map.png')
        self.start_rect=self.start_img.get_rect()

        # importing images
        self.start_button_img=pygame.image.load('../graphics/buttons/start_button.png')
        self.quit_button_img=pygame.image.load('../graphics/buttons/quit_button.png')
        self.main_menu_button_img=pygame.image.load('../graphics/buttons/main_menu_button.png')
        self.mute_button_img=pygame.image.load('../graphics/buttons/mute_button.png')
        self.death_img=pygame.image.load('../graphics/test/rip.png')

        # starting coordinates of moving background on splash screen
        self.startx=-650
        self.starty=-650

        self.muted=False

        # initialising buttons
        self.start_button=Button(400,450,self.start_button_img)
        self.quit_button=Button(700,450,self.quit_button_img)
        self.main_menu_button=Button(400,350,self.main_menu_button_img)
        self.mute_button=Button(700,350,self.mute_button_img)
        self.death_main_menu_button=Button(525,400,self.main_menu_button_img)

        # fonts
        self.logo_font=pygame.font.Font(LOGO_FONT,80)
        self.ui_font=pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # map and sprite setup
        self.create_map()

        # ui
        self.ui=UI()
        self.upgrade=Upgrade(self.player)

        # ost
        self.main_ost=pygame.mixer.Sound('../audio/ost.ogg')
        self.starting_ost=pygame.mixer.Sound('../audio/starting_screen.ogg')
        self.main_ost.set_volume(0.5)
        self.starting_ost.set_volume(0.5)
        self.starting_ost.play(loops=-1)

        # sfx
        self.death_sfx=pygame.mixer.Sound("../audio/oof.mp3")
        self.death_sfx.set_volume(0.2)

        # particles
        self.animation_player=AnimationPlayer()
        self.magic_player=ItemPlayer(self.animation_player)

    def create_map(self):

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
        # generate map on intialisation
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
                            hit_id=int(col) if int(col) in [16,17,22,25,36,39,40,49,58,59,67,71,73,75,93,94,105,106,107] else 200 # all alpha tile ids that require specific hitboxes
                            if self.mode:
                                Tile((x,y),[self.obstacle_sprites],'invisible','invisible')
                            else:
                                Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf,hit_id) # add surf for actual objects

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
                                elif col=='392': monster_name='skeleton'
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

    def restart(self):
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.attack_sprites.empty()
        self.attackable_sprites.empty()
        self.create_map()

    def start_screen(self):
        self.screen=pygame.display.get_surface()
        self.startx-=0.5 # move background image of map across screen
        self.starty-=0.5
        self.screen.blit(self.start_img,(self.startx,self.starty))
        self.draw_game_font()
        if self.start_button.draw(self.screen):
            self.stopped=False
            self.started=True
            self.starting_ost.stop()
            self.main_ost.play(loops=-1)
        if self.quit_button.draw(self.screen):
            pygame.quit()
            sys.exit()
        self.paused=False
    
    def draw_game_font(self):
        text1=self.logo_font.render("Hexham's",1,LOGO_FONT_COLOR)
        text2=self.logo_font.render("Awakening",1,LOGO_FONT_COLOR)
        text1_outline=add_outline_to_image(text1,2,LOGO_OUTLINE_COLOR)
        text2_outline=add_outline_to_image(text2,2,LOGO_OUTLINE_COLOR)
        self.screen.blit(text1_outline,(500,200))
        self.screen.blit(text2_outline,(475,325))

    def mute(self):
        self.muted=not self.muted
        if self.muted:
            self.main_ost.stop()
        elif not self.muted:
            self.main_ost.play()

    def draw_text(self,text,color,x,y):
        text_drawn=self.ui_font.render(text,1,color)
        self.screen.blit(text_drawn,(x,y))

    def pause(self):
        # transparent black background
        pause_surface=pygame.Surface((WIDTH,HEIGHT))
        pause_surface.set_alpha(128)
        pause_surface.fill(BLACK)
        self.screen.blit(pause_surface,(0,0))

         # stats written on pause screen
        self.draw_text(f"Health: {self.player.health}",WHITE,560,440)
        self.draw_text(f"Energy: {self.player.energy}",WHITE,560,490)
        self.draw_text(f"Attack: {self.player.attack_stat}",WHITE,560,540)
        self.draw_text(f"Power: {self.player.power_stat}",WHITE,560,590)
        self.draw_text(f"Stamina: {round(self.player.stamina)}",WHITE,560,640)

        # paused text
        pause_text=self.logo_font.render("PAUSED",1,'red')
        pause_text_outline=add_outline_to_image(pause_text,2,LOGO_FONT_COLOR)
        self.screen.blit(pause_text_outline,(400,100))

        # buttons functionality
        if self.main_menu_button.draw(self.screen):
            self.started=False
            self.main_ost.stop()
            self.restart()
            self.starting_ost.play(loops=-1)
        if self.mute_button.draw(self.screen):
            self.mute()


    def check_death(self,pos):

        screen=pygame.display.get_surface()
        screen.blit(self.death_img,(pos))
        if self.player.health<=0:
            self.death_sfx.play()
            self.stopped=True

            # red tint to background
            death_surface=pygame.Surface((WIDTH,HEIGHT))
            death_surface.set_alpha(128)
            death_surface.fill((255,0,0))
            screen.blit(death_surface,(0,0))

             # death text
            death_text=self.logo_font.render("GAME''OVER!",1,'#853c41')
            death_text_outline=add_outline_to_image(death_text,2,BLACK)
            self.screen.blit(death_text_outline,(300,175))

            # button to restart by going to main menus
            if self.death_main_menu_button.draw(screen):
                self.started=False
                self.main_ost.stop()
                self.starting_ost.play(loops=-1)
                self.restart()
    
    def run(self):
        self.visible_sprites.custom_draw(self.player) # draw world
        self.ui.display(self.player)
        self.check_death(self.player.pos)
        #update and draw game
        if self.game_paused: # upgrade menu
            self.upgrade.display()
        elif self.paused: # pause screen
            self.pause()
        elif self.stopped: # if game ends
            pass
        else:
            # run game normally
            self.visible_sprites.update() # update visible sprites on screen
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
        #self.floor_surface=pygame.image.load('../graphics/map_assets/bigger_map.png').convert() # True
        self.floor_surface=pygame.image.load('../graphics/map_assets/12800_ground_map.png').convert() # False
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