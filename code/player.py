import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image=pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect=self.image.get_rect(topleft=pos)

        self.direction=pygame.math.Vector2()
        self.speed=5

        self.obstacle_sprites=obstacle_sprites
    
    def input(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y=-1
        elif keys[pygame.K_s]:
            self.direction.y=1
        else:
            self.direction.y=0
        
        if keys[pygame.K_a]:
            self.direction.x=-1
        elif keys[pygame.K_d]:
            self.direction.x=1
        else:
            self.direction.x=0

    def move(self,speed):
        ''' to prevent diagonal speed boost
        if self.direction.magnitude()!=0:
            self.direction=self.direction.normalize()
        '''
        self.rect.x+=self.direction.x*speed
        self.collision('h')
        self.rect.y+=self.direction.y*speed
        self.collision('v')

    def collision(self,direction):
        if direction=='h':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x>0: #moving right
                        self.rect.right=sprite.rect.left
                    if self.direction.x<0: #moving left
                        self.rect.left=sprite.rect.right
        if direction=='v':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y<0: #moving down
                        self.rect.top=sprite.rect.bottom
                    if self.direction.y>0: #moving up
                        self.rect.bottom=sprite.rect.top
    
    def update(self):
        self.input()
        self.move(self.speed)