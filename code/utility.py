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
            img_files.remove( '.DS_Store') # .DS_Store is the bane of my existence

            print(img_files)
            img_files.sort(key=lambda id:int(id.split('.')[0]))
        else:
            img_files.sort()
        for image in img_files:
            print(image) if 'object' in path else 6+9
            full_path = path + '/' + image
            if not image.startswith('.DS'): # to prevent those blasted .DS_Store files from being parsed
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)

    return surface_list