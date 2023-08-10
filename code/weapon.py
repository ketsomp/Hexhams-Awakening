import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self,player,groups):
        super().__init__(groups)
        self.sprite_type='weapon'
        direction=player.status.split('_')[0]

        # graphic
        full_path=f"../graphics/weapons/{player.weapon}/{direction}.png"
        self.image=pygame.image.load(full_path).convert_alpha()

        #placement wrt player (on player)
        if direction=='right':
            self.rect=self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(-20,0))
        elif direction=='left':
            self.rect=self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(-20,0))
        elif direction=='down':
            self.rect=self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(0,-30))
        else:
            self.rect=self.image.get_rect(midbottom=player.rect.midtop+pygame.math.Vector2(0,0))