'''
Blobber Game
by Brett Huffman
and (add your name)
Comp Sci 333 - Computer Networking
(c)2023.  All Rights Reserved
-----------------------------------
Program Main Application
Install items:
- pygame (pip install pygame)
- tweener (pip install tweener)
- spatial (pip install spatial)
'''
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame as pg
import sys
import random
from settings import *
from blob import Blob
from playerblob import PlayerBlob
from math import hypot
from common import clamp, get_private_ip, GameModes
from tweener import *
from camera import Camera
from world import world
from spatial_hash import spatial_hash
from pygame.locals import *
from mainmenu import main_menu

# Tween motions
tween = Tween(begin=1.0, 
               end=1.05,
               duration=1000,
               easing=Easing.LINEAR,
               easing_mode=EasingMode.IN_OUT,
               boomerang=True,
               loop=True,
               reps=0) # Infinite Reps


# Main game object
class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.ip_address = get_private_ip()
        self.game_mode = GameModes.MAIN_MENU
        self.game_settings = START_BLOB[:]
        self.delta_time = 1
        self.blobs = []
        self.spatial_hash = None
        self.zoom_factor = 0
        self.world = world(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.spatial_hash = spatial_hash(COLLISION_CELL_SIZE)
        self.sounds = dict()
        self.blobs = []
        self.main_menu = main_menu(self.screen, self.sounds, self.game_settings)
        self.font = pg.font.SysFont(None, 72)
        self.load_sounds()
        self.new_game()

    def new_game(self):
        ''' Create a new game '''
        
        # Create blobs - Main Player first (so always in index=0 position)
        pb = PlayerBlob("main_player", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 20, (255,255,0), 0.5)
        self.blobs.append(pb)
        self.spatial_hash.insert(pb)  # For the PlayerBlob

        # Randomly add food blobs
        for i in range(200):
            fb = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, FOOD_COLOR_ARRAY[i%len(FOOD_COLOR_ARRAY)], 0, 1, 8, 6)
            self.blobs.append(fb)
            self.spatial_hash.insert(fb)  # For each food blob

    def load_sounds(self):
        pg.mixer.init() # initialize sound

        for snd in SOUNDS:
            name = snd.split('.')[0]
            value = pg.mixer.Sound('./sounds/' + snd)
            if name is not None and value is not None:
                self.sounds.update({name: value})


    def update(self):
        ''' Update executed once per frame '''
        # Caption for now        
        pg.display.set_caption(f'{self.clock.get_fps():.1f} fps')



        if self.game_settings[0]['answer'] == IS_SERVER:
            # Update the main player
            self.blobs[0].update(self.camera)

            # Update the spacial hash since things moved
            # only after everything is done moving
            # Clear the spatial hash
            self.spatial_hash.buckets.clear()

            # Update all other blobs
            player_dx = self.blobs[0].dx
            player_dy = self.blobs[0].dy
            for blob in self.blobs[1:]:
                blob.wander()
                blob.update(player_dx, player_dy)
                self.spatial_hash.insert(blob)

            # Retrieve the blobs using spatial hash
            nearby_blobs = self.spatial_hash.potential_collisions(self.blobs[0])

            # Handle collisions
            if self.game_mode == GameModes.PLAYING:
                for blob in nearby_blobs:
                    if blob != self.blobs[0] and blob.has_touched(self.blobs[0]):
                        temp_blob_type = blob.name
                        new_radius = (self.blobs[0].squared_size + blob.squared_size)**0.5
                        self.blobs[0].set_size(new_radius)
                        if GAME_SOUNDS:
                            self.sounds['collision'].play()
                        self.blobs.remove(blob)

                        if(temp_blob_type == 'food'):
                            fb = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, FOOD_COLOR_ARRAY[random.randint(0, len(FOOD_COLOR_ARRAY) - 1)], 0, 1)
                            self.blobs.append(fb)
        else:
            pass
        
    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')
        
        # Draw the world boundary
        self.world.draw(self.screen, self.camera)
        
        # Draw all the blobs
        for blob in self.blobs[::-1]:
            blob.draw(self.screen, self.camera)

        # Draw Paused if screen paused
        if self.game_mode == GameModes.PAUSED:
            name_text = self.font.render("P A U S E D", True, (240, 240, 240))
            text_rect = name_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2-100))
            self.screen.blit(name_text, text_rect)

        # Drawn screen to forefront
        pg.display.flip()


    def move_towards(self, blob, target_x, target_y):
        """Set blob's movement vectors to move it towards a target point."""

        # Calculate direction vector components
        dir_x = target_x - blob.x
        dir_y = target_y - blob.y

        # Calculate direction vector
        distance = hypot(target_x - blob.x, target_y - blob.y)
        # Avoid division by zero (when blob is already at the target position)
        if distance == 0:
            blob.dx = 0.0
            blob.dy = 0.0
            return
        
        # Scale the direction by the blob's speed to get the movement vector
        blob.dx = clamp(dir_x * distance / 9000, -MAX_BLOB_VELOCITY, MAX_BLOB_VELOCITY)
        blob.dy = clamp(dir_y * distance / 9000, -MAX_BLOB_VELOCITY, MAX_BLOB_VELOCITY)


    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                # End playing and go back to main menu
                self.game_mode = GameModes.MAIN_MENU
            # If Server Mode allow to switch between Paused and Playing
            elif self.game_settings[0]['answer'] == IS_SERVER and event.type == pg.KEYDOWN and event.key == pg.K_p:
                if self.game_mode == GameModes.PLAYING:
                    self.game_mode = GameModes.PAUSED
                elif self.game_mode == GameModes.PAUSED:
                    self.game_mode = GameModes.PLAYING
            # Check if the mouse has moved
            elif self.game_mode == GameModes.PLAYING and event.type == pg.MOUSEMOTION:
                mouseX, mouseY = event.pos
                if len(self.blobs) > 0:
                    self.move_towards(self.blobs[0], mouseX, mouseY)

    def run(self):
        frame_id = 0
        # Called once to manage whole game
        while True:
            # Order is very important here
            self.check_events()

            # If no Game Mode, show main menu
            if self.game_mode == GameModes.MAIN_MENU:
                self.game_settings = self.main_menu.show()
                # Set all settings from main menu:
                # name
                temp = self.game_settings[2]['answer']
                self.blobs[0].set_name(temp)
                # color
                temp = BLOB_COLOR_ARRAY[self.game_settings[1]['answer']]
                self.blobs[0].set_color(temp)
                # hair
                temp = self.game_settings[3]['answer']
                self.blobs[0].set_hair_count(temp * 14)
                self.blobs[0].set_hair_size(temp * 2 + 10)
                self.game_mode = GameModes.PAUSED
            else:
                if frame_id % 2 == 0: #Experimental
                    self.update()
                self.draw()
                    
                self.delta_time = self.clock.tick(FPS)
                frame_id += 1

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()