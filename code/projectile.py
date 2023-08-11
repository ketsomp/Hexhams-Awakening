import pygame
from settings import *
from level import Level

class Knife(pygame.sprite.Sprite):
    def __init__(self,player,pos,direction):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.rotate(pygame.image.load('../graphics/projectiles/knife.png'),-45)
        self.rect=self.image.get_rect
        self.rect.x=pos[0]
        self.rect.y=pos[1]
        self.direction=player.status.split('_')[0]
        self.speed=5
    
    def update(self):
        if self.direction=='right':
            self.rect.x+=self.speed
        elif self.direction=='left':
            self.rect.x-=self.speed
        if self.rect.x>WIDTH or self.rect.x<0:
            self.kill()
        killed=pygame.sprite.spritecollide(self,Level.attackable_sprites,True)
        if killed:
            self.kill()

class ItemPlayer:
    def __init__(self,animation_player):
        self.animation_player=animation_player


    def heal(self,player,strength,cost,groups):
        if player.energy>=cost:
            player.health+=strength
            player.energy-=cost
            if player.health>=player.stats['health']: #checking if current health exceeds max health
                player.health=player.stats['health'] # cap at max health
            self.animation_player.create_particles('aura',player.rect.center,groups) # aura when cast
            self.animation_player.create_particles('heal',player.rect.center+pygame.math.Vector2(0,-60),groups) # healing thing when cast


    def throw(self,player,cost,groups):
        if player.energy>=cost:
            player.energy-=cost
            if player.status.split('_')[0]=='right:':
                direction=pygame.math.Vector2(1,0)
            elif player.status.split('_')[0]=='left:':
                direction=pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0]=='up:':
                direction=pygame.math.Vector2(0,-1)
            else:
                direction=pygame.math.Vector2(0,1)
                
            for i in range(1,6):
                if direction.x: 
                    offset_x=(direction.x*i)*TILESIZE
                    x=player.rect.centerx+offset_x
                    y=player.rect.centery
                    self.animation_player.create_particles('knife',(x,y),groups)
                else: pass