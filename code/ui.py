import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface=pygame.display.get_surface()
        self.font=pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect=pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect=pygame.Rect(10,35,ENERGY_BAR_WIDTH,BAR_HEIGHT) # (l,t,b,h)

        # convert weapon dict
        self.weapon_graphics=[]
        for weapon in weapon_data.values():
            path=weapon['graphic']
            weapon=pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # convert projectile dict
        self.proj_graphics=[]
        for proj in proj_data.values():
            path=proj['graphic']
            proj=pygame.image.load(path).convert_alpha()
            self.proj_graphics.append(proj)

    def display_bar(self,current,max_amount,bg_rect,color):
        # draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        # converting current health to pixels in bar
        ratio=current/max_amount # if health half, ratio = 50/100 = 0.5
        current_width=bg_rect.width*ratio # current width of hp bar = 200 * 0.5 = 100 instead of full bar of 200
        current_rect = bg_rect.copy()
        current_rect.width=current_width

        # drawing bar
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect,3) # border around red hp bar, 4th parameter makes box outlined

    def display_xp(self,xp):
        xp_offset=20
        text_surf=self.font.render(str(int(xp)),False,BLACK)
        x=self.display_surface.get_size()[0]-xp_offset
        y=self.display_surface.get_size()[1]-xp_offset
        text_rect=text_surf.get_rect(bottomright=(x,y))

        pygame.draw.rect(self.display_surface,XP_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def hotbox(self,left,top,has_switched):
        bg_rect=pygame.Rect(left,top,HOTBOX_SIZE,HOTBOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect=self.hotbox(10,630,has_switched) 
        weapon_surf=self.weapon_graphics[weapon_index]
        weapon_rect=weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf,weapon_rect)

    def proj_overlay(self,proj_index,has_switched):
        bg_rect=self.hotbox(80,635,has_switched) 
        proj_surf=self.proj_graphics[proj_index]
        proj_rect=proj_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(proj_surf,proj_rect)

    def display(self,player):
        # display bars by calling above method
        self.display_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.display_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)

        self.display_xp(player.xp)

        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
        self.proj_overlay(player.proj_index,not player.can_switch_proj)