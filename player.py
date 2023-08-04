import pygame
import config 


class Player:
    def __init__(self,x,y):
        print('player created')
        self.position=[x,y]

    def update(self):
        print("Player update")
    
    def render(self,screen):
        print('played rendered')
        pygame.draw.rect(screen,config.WHITE,(self.position[0]*config.SCALE,self.position[1]*config.SCALE,config.SCALE,config.SCALE),4) #(posx, posy, height, width)
    
    def update_position(self,dx,dy):
        self.position[0]+=dx
        self.position[1]+=dy