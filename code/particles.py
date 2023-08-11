import pygame
from utility import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
    # particle dictionary
        self.frames = {
                # magic
                'aura': import_folder('../graphics/particles/aura'),
                'heal': import_folder('../graphics/particles/heal/frames'),
                'spike': import_folder('../graphics/particles/spike'),
                
                # attacks 
                'claw': import_folder('../graphics/particles/claw'),
                'slash': import_folder('../graphics/particles/slash'),
                'sparkle': import_folder('../graphics/particles/sparkle'),
                'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
                'thunder': import_folder('../graphics/particles/thunder'),
    
                # monster deaths
                'skeleton': import_folder('../graphics/particles/sdeath'),
                'mushroom': import_folder('../graphics/particles/mdeath'),
                'goblin': import_folder('../graphics/particles/gdeath'),
                'flying_eye': import_folder('../graphics/particles/fdeath'),
                
                # leafs 
                'leaf': (
                    import_folder('../graphics/particles/leaf1'),
                    import_folder('../graphics/particles/leaf2'),
                    import_folder('../graphics/particles/leaf3'),
                    import_folder('../graphics/particles/leaf4'),
                    import_folder('../graphics/particles/leaf5'),
                    import_folder('../graphics/particles/leaf6'),
                    self.reflect_images(import_folder('../graphics/particles/leaf1')),
                    self.reflect_images(import_folder('../graphics/particles/leaf2')),
                    self.reflect_images(import_folder('../graphics/particles/leaf3')),
                    self.reflect_images(import_folder('../graphics/particles/leaf4')),
                    self.reflect_images(import_folder('../graphics/particles/leaf5')),
                    self.reflect_images(import_folder('../graphics/particles/leaf6'))
                    )
                }
    def reflect_images(self,frames):
        new_frames=[]
        for frame in frames:
            flip=pygame.transform.flip(frame,True,False) # flip on x axis and not y axis
            new_frames.append(flip)
        return new_frames
    
    def create_grass_particles(self,pos,group):
        animation_frames=choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames,group)
    
    def create_particles(self,animation_type,pos,groups):
        animation_frames=self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.frame_index=0
        self.animation_speed=0.15
        self.frames=animation_frames
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_rect(center=pos)
    
    def animate(self):
        self.frame_index+=self.animation_speed
        if self.frame_index>=len(self.frames):
            self.kill()
        else:
            self.image=self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()