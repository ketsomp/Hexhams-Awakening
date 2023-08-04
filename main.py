import pygame
import config
from game import Game
from game_state import GameState

#initialize pygame
pygame.init()

#set up screen
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Hexham's Awakening")

#handle framerate
clock=pygame.time.Clock()
fps=60

#call game from game.py
game=Game(screen)
game.setup()

#fill screen
screen.fill(config.BLACK)

#game loop
while game.game_state==GameState.RUNNING:
    clock.tick(fps)
    game.update()
    pygame.display.update()