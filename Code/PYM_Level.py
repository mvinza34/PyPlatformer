import pygame
from PYM_Tiles import Tile, StaticTile, Crate, Coin, Palm
from PYM_Settings import TILESIZE, WIDTH, HEIGHT, CAMERA_BORDERS
from PYM_Player import Player
from PYM_Support import import_csv_layout, import_cut_graphics
from PYM_Enemy import Enemy
from PYM_Decoration import Sky, Water, Clouds
from PYM_Particles import Particle_Effect
from PYM_Game_Data import levels

class Level:
    def __init__(self,current_level,surface,create_overworld,change_coins,change_health): 
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None
        # sounds
        self.coin_sound = pygame.mixer.Sound('../Audio/effects/coin.wav')
        self.stomp_sound = pygame.mixer.Sound('../Audio/effects/stomp.wav')
        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        # sprite group setup
        self.visible_sprites = CameraGroup(self.display_surface) # draws any sprites in the group
        self.active_sprites = pygame.sprite.Group() # updates any sprites in the group
        self.collision_sprites = pygame.sprite.Group() # includes any collidable sprites in the group
        # level setup
        self.level_setup(change_coins,change_health)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()
        for row_index,row in enumerate(layout):
            for col_index,value in enumerate(row):
                if value != '-1':
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    if type == 'Terrain':
                        terrain_tile_list = import_cut_graphics('../Graphics/Terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(TILESIZE,x,y,[self.visible_sprites,self.collision_sprites,self.active_sprites],tile_surface)
                    if type == 'Grass':
                        grass_tile_list = import_cut_graphics('../Graphics/Decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(value)]
                        sprite = StaticTile(TILESIZE,x,y,[self.visible_sprites,self.active_sprites],tile_surface)
                    if type == 'Crates':
                        sprite = Crate(TILESIZE,x,y,[self.visible_sprites,self.active_sprites,self.collision_sprites])
                    if type == 'Coins':
                        if value == '0': sprite = Coin(TILESIZE,x,y,[self.visible_sprites,self.active_sprites],'../Graphics/Coins/gold',5)
                        if value == '1': sprite = Coin(TILESIZE,x,y,[self.visible_sprites,self.active_sprites],'../Graphics/Coins/silver',1)
                    if type == 'FG_Palms':
                        if value == '0': sprite = Palm(TILESIZE,x,y,[self.visible_sprites,self.active_sprites,self.collision_sprites],'../Graphics/Terrain/palm_small',38)
                        if value == '1': sprite = Palm(TILESIZE,x,y,[self.visible_sprites,self.active_sprites,self.collision_sprites],'../Graphics/Terrain/palm_large',64)
                    if type == 'BG_Palms':
                        sprite = Palm(TILESIZE,x,y,[self.visible_sprites,self.active_sprites],'../Graphics/Terrain/palm_bg',64)
                    if type == 'Enemies':
                        sprite = Enemy(TILESIZE,x,y,[self.visible_sprites,self.active_sprites])
                    if type == 'Constraints':
                        sprite = Tile(TILESIZE,x,y,self.active_sprites)
                    if type == 'Screen':
                        sprite = Tile(TILESIZE,x,y,[self.active_sprites,self.collision_sprites])
                    if type == 'Death':
                        sprite = Tile(TILESIZE,x,y,self.active_sprites)
                    sprite_group.add(sprite)
        return sprite_group

    def player_setup(self,layout,change_health):
        for row_index,row in enumerate(layout):
            for col_index,value in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if value == '0':
                    sprite = Player((x,y),[self.visible_sprites,self.active_sprites],self.collision_sprites,self.display_surface,self.create_jump_particles,change_health)
                    self.player.add(sprite)
                if value == '1':
                    hat_surface = pygame.image.load('../Graphics/Character/hat.png').convert_alpha()
                    sprite = StaticTile(TILESIZE,x,y,[self.visible_sprites,self.active_sprites],hat_surface)
                    self.goal.add(sprite)

    def level_setup(self,change_coins,change_health):
        level_data = levels[self.current_level]
        # player setup
        player_layout = import_csv_layout(level_data['Player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        # user interface
        self.change_coins = change_coins
        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        # explosion
        self.explosion_sprites = pygame.sprite.Group()
        # terrain
        terrain_layout = import_csv_layout(level_data['Terrain'])
        # decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0] * TILESIZE)
        self.clouds = Clouds(400,level_width,30,self.visible_sprites,self.active_sprites)
        # background palms
        bg_palm_layout = import_csv_layout(level_data['BG_Palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'BG_Palms')
        # player setup
        self.player_setup(player_layout,change_health)
        self.terrain_sprites = self.create_tile_group(terrain_layout,'Terrain')
        self.water = Water(HEIGHT + 120, level_width,self.visible_sprites) 
        # grass
        grass_layout = import_csv_layout(level_data['Grass'])
        self.grass_sprites = self.create_tile_group(grass_layout,'Grass')
        # foreground palms
        fg_palm_layout = import_csv_layout(level_data['FG_Palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'FG_Palms')
        # crate
        crate_layout = import_csv_layout(level_data['Crates'])
        self.crate_sprites = self.create_tile_group(crate_layout,'Crates')
        # coins 
        coin_layout = import_csv_layout(level_data['Coins'])
        self.coin_sprites = self.create_tile_group(coin_layout,'Coins')
        # enemies
        enemy_layout = import_csv_layout(level_data['Enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout,'Enemies')      
        # enemy constraints
        enemy_constraint_layout = import_csv_layout(level_data['Constraints'])
        self.enemy_constraint_sprites = self.create_tile_group(enemy_constraint_layout,'Constraints')
        # screeen constraints
        screen_constraint_layout = import_csv_layout(level_data['Screen'])
        self.screen_constraint_sprites = self.create_tile_group(screen_constraint_layout,'Screen')
        # death constraints
        death_constraint_layout = import_csv_layout(level_data['Death'])
        self.death_constraint_sprites = self.create_tile_group(death_constraint_layout,'Death')     
        # collisions
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites() + self.screen_constraint_sprites.sprites()
        self.collision_sprites.add(collidable_sprites)

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.constraint_sprites,False): enemy.reverse()

    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right: pos -= pygame.math.Vector2(10,5)
        else: pos += pygame.math.Vector2(10,5)
        jump_particle_sprite = Particle_Effect(pos,'jump',[self.visible_sprites,self.active_sprites])
        self.dust_sprite.add(jump_particle_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < WIDTH/4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 8
        elif player_x > WIDTH - (WIDTH/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 8
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground: self.player_on_ground = True
        else: self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right: offset = pygame.math.Vector2(10,15)
            else: offset = pygame.math.Vector2(-10,15)
            fall_dust_particle = Particle_Effect(self.player.sprite.rect.midbottom - offset,'land',[self.visible_sprites,self.active_sprites])
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.death_constraint_sprites,False): self.create_overworld(self.current_level,0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite,self.goal,False): self.create_overworld(self.current_level,self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                #self.coin_sound.play()
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explosion_sprite = Particle_Effect(enemy.rect.center,'explosion',[self.visible_sprites,self.active_sprites])
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        # run the entire game/level
        ## sky
        self.sky.draw(self.display_surface)
        ## draw and update all sprites included in the groups
        self.active_sprites.update(self.world_shift)
        self.visible_sprites.custom_draw(self.player.sprite)
        ## player gravity
        self.get_player_on_ground()
        self.create_landing_dust()
        # scrolling 
        # self.scroll_x() // commented out for now
        ## win or lose
        self.check_death()
        self.check_win()
        ## coin and enemy collisions
        self.check_coin_collisions()
        self.check_enemy_collisions()
        self.enemy_collision_reverse()

class CameraGroup(pygame.sprite.Group):
    def __init__(self,surface):
        super().__init__()
        self.display_surface = surface
        self.offset = pygame.math.Vector2(100,300)
        # camera setup
        cam_left = CAMERA_BORDERS['left']
        cam_top = CAMERA_BORDERS['top']
        cam_width = self.display_surface.get_size()[0] - (cam_left + CAMERA_BORDERS['right'])
        cam_height = self.display_surface.get_size()[1] - (cam_top + CAMERA_BORDERS['bottom'])
        self.camera_rect = pygame.Rect(cam_left,cam_top,cam_width,cam_height)

    def custom_draw(self,player):
        # getting the camera position
        if player.rect.left < self.camera_rect.left: self.camera_rect.left = player.rect.left # moving the camera left
        if player.rect.right > self.camera_rect.right: self.camera_rect.right = player.rect.right # moving the camera right         
        if player.rect.top < self.camera_rect.top: self.camera_rect.top = player.rect.top # moving the camera top
        if player.rect.bottom > self.camera_rect.bottom: self.camera_rect.bottom = player.rect.bottom # moving the camera bottom
        # camera offset
        self.offset = pygame.math.Vector2(self.camera_rect.left - CAMERA_BORDERS['left'], self.camera_rect.top - CAMERA_BORDERS['top'])
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

