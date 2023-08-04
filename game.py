import pygame
from player import Player
from game_state import GameState
import config

class Game:
    def __init__(self, screen):
        self.screen=screen
        self.objects=[]
        self.game_state=GameState.NONE
    
    def setup(self):
        player=Player(1,1) # (startx, starty)
        self.player=player
        self.objects.append(player)
        print('do setup')
        self.game_state=GameState.RUNNING
    
    def update(self):
        self.screen.fill(config.BLACK)
        print('update')
        self.handle_events()

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.game_state=GameState.END
            #handle key movements
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    self.game_state=GameState.END
                if event.key==pygame.K_w:
                    self.player.update_position(0,-1)
                if event.key==pygame.K_s:
                    self.player.update_position(0,1)
                if event.key==pygame.K_a:
                    self.player.update_position(-1,0)
                if event.key==pygame.K_d:
                    self.player.update_position(1,0)