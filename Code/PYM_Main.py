import pygame, sys, os
from PYM_Settings import *
from PYM_Level import Level
from PYM_Overworld import Overworld
from PYM_UI import UI

# Ensures that all assets will import properly 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Game:
    def __init__(self): 
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        # music
        self.level_bg_music = pygame.mixer.Sound('../Audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound('../Audio/overworld_music.wav')
        # UI setup
        self.ui = UI(self.screen)
        # overworld setup
        self.overworld = Overworld(0,self.max_level,self.screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)

    def create_level(self,current_level):
        self.level = Level(current_level,self.screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)

    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level: self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,self.screen,self.create_level)
        self.status = 'overworld'
        self.level_bg_music.stop()
        self.overworld_bg_music.play(loops = -1)

    def change_coins(self,amount):
        self.coins += amount

    def change_health(self,amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0:
            self.cur_health = 0
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0,self.max_level,self.screen,self.create_level)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops = -1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(), sys.exit()
            self.screen.fill('grey')
            if self.status == 'overworld': self.overworld.run()
            else: self.level.run(), self.ui.show_health(self.cur_health,self.max_health), self.ui.show_coins(self.coins), self.check_game_over()
            #self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
 
if __name__ == '__main__':
    game = Game()
    game.run()
