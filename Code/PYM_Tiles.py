from PYM_Support import import_folder
import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,size,x,y,groups):
        super().__init__(groups)
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
    def update(self,shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self,size,x,y,groups,surface):
         super().__init__(size,x,y,groups)
         self.image = surface

class Crate(StaticTile):
    def __init__(self,size,x,y,groups):
        super().__init__(size,x,y,groups,pygame.image.load('../Graphics/Terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
    def __init__(self,size,x,y,groups,path):
        super().__init__(size,x,y,groups)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    def update(self,shift):
        self.animate()
        self.rect.x += shift

class Coin(AnimatedTile):
    def __init__(self,size,x,y,groups,path,value):
        super().__init__(size,x,y,groups,path)
        center_x = x + int(size/2)
        center_y = y + int(size/2) 
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.value = value

class Palm(AnimatedTile):
    def __init__(self,size,x,y,groups,path,offset):
        super().__init__(size,x,y,groups,path)
        offset_y = y - offset
        self.rect.topleft = (x,offset_y)
