from os import walk
from csv import reader
from PYM_Settings import TILESIZE
import pygame

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map,delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILESIZE)
    tile_num_y = int(surface.get_size()[1] / TILESIZE)
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surface = pygame.Surface((TILESIZE,TILESIZE),flags = pygame.SRCALPHA)
            new_surface.blit(surface,(0,0),pygame.Rect(x,y,TILESIZE,TILESIZE))  # pygame.Rect(t,l,w,h)
            cut_tiles.append(new_surface)
    return cut_tiles