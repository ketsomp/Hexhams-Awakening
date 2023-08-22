import pygame
from settings import *

class Upgrade:
    def __init__(self,player):

        #general setup
        self.display_surface=pygame.display.get_surface()
        self.player=player
        self.attribute_key=len(player.stats)
        self.attribute_names=list(player.stats.keys())
        self.max_values=list(player.max_stats.values())
        self.font=pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        #item dimensions
        self.height=self.display_surface.get_size()[1]*0.8
        self.width=self.display_surface.get_size()[0]//6
        self.create_items()

        # selection system
        self.selection_index=0
        self.selection_time=None
        self.can_move=True

    def input(self):
        keys=pygame.key.get_pressed()
        if self.can_move:
            if keys[pygame.K_RIGHT] and self.selection_index<=self.attribute_key:
                self.selection_index+=1
                self.can_move=False
                self.selection_time=pygame.time.get_ticks()
            elif keys[pygame.K_LEFT] and self.selection_index>=1:
                self.selection_index-=1
                self.can_move=False
                self.selection_time=pygame.time.get_ticks()
            if keys[pygame.K_SPACE]:
                self.can_move=False
                self.selection_time=pygame.time.get_ticks()
                self.item_list[self.selection_index].trigger(self.player)

            if self.selection_index<=0:
                self.selection_index=6
            if self.selection_index>=6:
                self.selection_index=0

    def selection_cooldown(self):
        if not self.can_move:
            current_time=pygame.time.get_ticks()
            if current_time-self.selection_time>=100: # delay between key presses (actions)
                self.can_move=True
    
    def create_items(self):
        self.item_list=[]
        
        for item,index in enumerate(range(self.attribute_key)):
            #horizontal position
            full_width=self.display_surface.get_size()[0]
            increment=full_width//self.attribute_key
            left=(item*increment)+(increment-self.width)//2

            # vertical position
            top=self.display_surface.get_size()[1]*0.1

            # create the object
            item=Item(left,top,self.width,self.height,index,self.font)
            self.item_list.append(item)

    def display(self):
        self.input()
        self.selection_cooldown()
        
        for index,item in enumerate(self.item_list):
            # get attributes
            name=self.attribute_names[index]
            value=self.player.get_value_by_index(index)
            max_value=self.max_values[index]
            cost=self.player.get_cost_by_index(index)
            item.display(self.display_surface,self.selection_index,name,value,max_value,cost)

class Item:
    def __init__(self,l,t,w,h,index,font):
        self.rect=pygame.Rect(l,t,w,h)
        self.font=font
        self.index=index

    def display_names(self,surface,name,cost,selected):
        # color
        color=TEXT_COLOR_SELECTED if selected else TEXT_COLOR
        # title
        title_surf=self.font.render(name,False,color)
        title_rect=title_surf.get_rect(midtop=self.rect.midtop+pygame.math.Vector2(0,20))

        # cost
        cost_surf=self.font.render(f'{int(cost)}',False,color)
        cost_rect=title_surf.get_rect(midbottom=self.rect.midbottom-pygame.math.Vector2(0,20))

        #draw
        surface.blit(title_surf,title_rect)
        surface.blit(cost_surf,cost_rect)

    def display_bar(self,surface,value,max_value,selected):
        # drawing setup
        top=self.rect.midtop+pygame.math.Vector2(0,60)
        bottom=self.rect.midbottom-pygame.math.Vector2(0,60)
        color=BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_height=bottom[1]-top[1]
        relative_number=(value/max_value)*full_height # meter on bar
        value_rect=pygame.Rect(top[0]-15,bottom[1]-relative_number,30,10)

        # draw elements
        pygame.draw.line(surface,color,top,bottom,5)
        pygame.draw.rect(surface,color,value_rect)

    def trigger(self,player):
        upgrade_attribute=list(player.stats.keys())[self.index]
        
        if player.xp>=player.upgrade_cost[upgrade_attribute] and player.stats[upgrade_attribute]<player.max_stats[upgrade_attribute]:
            player.xp-=player.upgrade_cost[upgrade_attribute]
            player.stats[upgrade_attribute]*=1.2
            player.upgrade_cost[upgrade_attribute]*=1.4 # more value, more cost

    def display(self,surface,selection_num,name,value,max_value,cost):
        if self.index==selection_num:
            pygame.draw.rect(surface,UPGRADE_BG_COLOR_SELECTED,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4) # for border    
        else:
            pygame.draw.rect(surface,UI_BG_COLOR,self.rect)
            pygame.draw.rect(surface,UI_BORDER_COLOR,self.rect,4)
        self.display_names(surface,name,cost,self.index==selection_num)
        self.display_bar(surface,value,max_value,self.index==selection_num )