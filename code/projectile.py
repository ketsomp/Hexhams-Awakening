import pygame
from settings import *
from random import randint

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
            if player.status.split('_')[0]=='right':
                direction=pygame.math.Vector2(1,0)
            elif player.status.split('_')[0]=='left':
                direction=pygame.math.Vector2(-1,0)
            elif player.status.split('_')[0]=='up':
                direction=pygame.math.Vector2(0,-1)
            else:
                direction=pygame.math.Vector2(0,1)
                
            for i in range(1,6):
                if direction.x: 
                    offset_x=(direction.x*i)*TILESIZE
                    x=player.rect.centerx+offset_x+randint(-TILESIZE//3,TILESIZE//3)
                    y=player.rect.centery+randint(-TILESIZE//3,TILESIZE//3)
                    self.animation_player.create_particles('spike',(x,y),groups)
                else: 
                    offset_y=(direction.y*i)*TILESIZE
                    x=player.rect.centerx+randint(-TILESIZE//3,TILESIZE//3)
                    y=player.rect.centery+offset_y+randint(-TILESIZE//3,TILESIZE//3)                    
                    self.animation_player.create_particles('spike',(x,y),groups)
