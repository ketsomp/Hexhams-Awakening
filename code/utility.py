from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    terrain_map=[]
    with open(path) as level_map:
        layout=reader(level_map,delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
def import_folder(path):
    surface_list = []

    for a,b,img_files in walk(path):
        if 'object' in path:
            try:img_files.remove( '.DS_Store') 
            except: pass # .DS_Store is the bane of my existence
            img_files.sort(key=lambda id:int(id.split('.')[0]))
        else:
            img_files.sort()
        for image in img_files:
            full_path = path + '/' + image
            if not image.startswith('.DS'): # to prevent those blasted .DS_Store files from being parsed
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)

    return surface_list

def add_outline_to_image(image: pygame.Surface, thickness: int, color: tuple, color_key: tuple = (255, 0, 255)) -> pygame.Surface:
    mask = pygame.mask.from_surface(image)
    mask_surf = mask.to_surface(setcolor=color)
    mask_surf.set_colorkey((0, 0, 0))

    new_img = pygame.Surface((image.get_width() + 2, image.get_height() + 2))
    new_img.fill(color_key)
    new_img.set_colorkey(color_key)

    for i in -thickness, thickness:
        new_img.blit(mask_surf, (i + thickness, thickness))
        new_img.blit(mask_surf, (thickness, i + thickness))
    new_img.blit(image, (thickness, thickness))

    return new_img