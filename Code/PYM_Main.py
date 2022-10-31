import pygame, sys, os
from PYM_Settings import *
from PYM_Level import Level
from PYM_Overworld import Overworld
from PYM_UI import UI
from PYM_Decoration import Sky

# Ensures that all assets will import properly 
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Game:
    def __init__(self): 
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_active = False
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
        # pause setup
        self.RUNNING, self.PAUSE = 0, 1
        self.state = self.RUNNING

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
            
    def title_screen(self):
        self.sky = Sky(8)
        self.sky.draw(self.screen)
        title_surf = self.font.render("Platformer",False,(0,0,0))
        title_rect = title_surf.get_rect(center = (620,150))
        self.screen.blit(title_surf,title_rect)	
        instruct_surf = self.font.render("Press [Enter] to start",False,(0,0,0))
        instruct_rect = instruct_surf.get_rect(center = (620,650))
        self.screen.blit(instruct_surf,instruct_rect)

    def game_manager(self):
        if self.status == 'overworld': self.overworld.run()
        else: self.level.run(), self.ui.show_health(self.cur_health,self.max_health), self.ui.show_coins(self.coins), self.check_game_over()

    def pause(self):
        pause_surf = self.font.render("Game Paused",False,(0,0,0))
        pause_rect = pause_surf.get_rect(center = (610,160))
        self.screen.blit(pause_surf,pause_rect)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(), sys.exit()
                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p: self.state = self.PAUSE
                        if event.key == pygame.K_s: self.state = self.RUNNING
                        if event.key == pygame.K_q: pygame.quit(), sys.exit
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: self.game_active = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_q: pygame.quit(), sys.exit
            self.screen.fill('grey')
            if self.game_active and self.state == self.RUNNING: self.game_manager()
            elif self.game_active and self.state == self.PAUSE: self.pause()
            else: self.title_screen()
            pygame.display.update()
            self.clock.tick(FPS)
 
if __name__ == '__main__':
    game = Game()
    game.run()
