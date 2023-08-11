import pygame
from settings import *
from particles import AnimationPlayer

class ItemPlayer:
    def __init__(self,animation_player):
        self.animation_player=animation_player

    def heal(self,player,strength,cost,groups):
        if player.energy>=cost:
            player.health+=strength
            player.energy-=cost
            if player.health>=player.stats['health']: #checking if current health exceeds max health
                player.health=player.stats['health'] # cap at max health
            self.animation_player.create_particles('aura',player.rect.center,groups)
            self.animation_player.create_particles('heal',player.rect.center+pygame.math.Vector2(0,-60),groups)


    def shoot(self):
        pass