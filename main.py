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
- OpenSimplex (pip install OpenSimplex)
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

import pickle

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
        self.current_player_index = -1
        self.main_menu = main_menu(self.screen, self.sounds, self.game_settings)
        self.font = pg.font.SysFont(None, 72)
        self.font_sm = pg.font.SysFont(None, 24)
        self.is_eaten = False
        self.eater = None
        self.load_sounds()
        self.new_game()

    def new_game(self):
        ''' Create a new game '''
        
        # Create blobs - Main Player
        new_x, new_y = self.find_safe_spot(300)
        pb = PlayerBlob("main_player", new_x, new_y, 20, (255,255,0), 0.5)
        self.camera.set_center(new_x, new_y)
        self.blobs.append(pb)
        self.current_player_index = len(self.blobs)-1
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
            if type(self.blobs[self.current_player_index]) == PlayerBlob:
                self.blobs[self.current_player_index].update(self.camera)

            # Update the spacial hash since things moved
            # only after everything is done moving
            # Clear the spatial hash
            self.spatial_hash.buckets.clear()

            # Update all other blobs
            player_dx = self.blobs[self.current_player_index].dx
            player_dy = self.blobs[self.current_player_index].dy
            for blob in self.blobs[1:]:
                blob.wander()
                blob.update(player_dx, player_dy)
                self.spatial_hash.insert(blob)

            # Retrieve the blobs using spatial hash
            nearby_blobs = self.spatial_hash.potential_collisions(self.blobs[self.current_player_index])

            # Handle collisions
            if self.game_mode == GameModes.PLAYING:
                for blob in nearby_blobs:
                    if blob != self.blobs[self.current_player_index] and blob.has_touched(self.blobs[self.current_player_index]):

                        if(blob.name == 'food'):
                            # Add the size
                            new_radius = (self.blobs[self.current_player_index].squared_size + blob.squared_size)**0.5
                            self.blobs[self.current_player_index].set_size(new_radius)

                            # Remove the old one
                            if GAME_SOUNDS:
                                self.sounds['collision'].play()
                            self.blobs.remove(blob)
                            # Make a new food blob
                            fb = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, FOOD_COLOR_ARRAY[random.randint(0, len(FOOD_COLOR_ARRAY) - 1)], 0, 1)
                            self.blobs.append(fb)

                        # Else if this is a blob eating another blob...
                        elif self.blobs[self.current_player_index].is_eaten == False and isinstance(blob, PlayerBlob) and isinstance(self.blobs[self.current_player_index], PlayerBlob):
                            # Determine which blob is bigger, hence the eater
                            if blob.size > self.blobs[self.current_player_index].size:
                                # You got eaten!
                                self.is_eaten = True
                                eater_blob = blob
                                eaten_player = self.blobs[self.current_player_index]
                            else: # You are the eater!
                                
                                eater_blob = self.blobs[self.current_player_index]
                                eaten_player = blob

                    # Check if only one PlayerBlob remains that is not eaten
#                if self.game_mode == GameModes.PLAYING and len([b for b in self.blobs if isinstance(b, PlayerBlob) and not b.is_eaten]) == 1:
                    # End game condition met
#                    self.game_mode = GameModes.GAME_OVER

            # Prepare everything to send to clients
#            serialized_data = pickle.dumps(self.blobs)
        else:
            pass
        
    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')
        
        # Draw the world boundary
        self.world.draw(self.screen, self.camera)
        
        # Draw all the blobs
        for blob in self.blobs:  # TO DO: Make sure they are within the screen
            blob.draw(self.screen, self.camera)
            if blob.name != 'food': # Show the player name
                name_text = self.font_sm.render(blob.name, True, (200, 200, 200))
                self.screen.blit(name_text, (blob.x + blob.size, blob.y))
        
        # Draw Paused if screen paused
        if self.game_mode == GameModes.PAUSED:
            name_text = self.font.render("P A U S E D", True, (240, 240, 240))
            text_rect = name_text.get_rect(center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2-100))
            self.screen.blit(name_text, text_rect)

        # Drawn screen to forefront
        pg.display.flip()

    def find_safe_spot(self, safe_distance=500):
        """
        Find a spot on the screen to place a new user 
        that is not within 'safe_distance' pixels of other users.
        """
        while True:
            # Randomly select a position within the world bounds
            x = random.randint(50, WORLD_WIDTH-100)
            y = random.randint(50, WORLD_HEIGHT-100)

            # Check if any blob is within the safe distance
            too_close = any(
                hypot(blob.x - x, blob.y - y) < safe_distance
                for blob in self.blobs
            )

            # If a safe spot is found, return the coordinates
            if not too_close:
                return x, y

    def move_towards(self, blob, target_x, target_y):
        """Set blob's movement vectors to move it towards a target point."""

        # Calculate direction vector components
        player_x = WINDOW_WIDTH // 2
        player_y = WINDOW_HEIGHT // 2
        dir_x = target_x - player_x
        dir_y = target_y - player_y

        # Calculate direction vector
        distance = hypot(target_x - player_x, target_y - player_y)
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
                if len(self.blobs) > 0 and self.current_player_index > -1:
                    self.move_towards(self.blobs[self.current_player_index], mouseX, mouseY)

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
                # temp = self.game_settings[2]['answer']
                # self.blobs[0].set_name(temp)
                # # color
                # temp = BLOB_COLOR_ARRAY[self.game_settings[1]['answer']]
                # self.blobs[0].set_color(temp)
                # # hair
                # temp = self.game_settings[3]['answer']
                # self.blobs[0].set_hair_count(temp * 14)
                # self.blobs[0].set_hair_size(temp * 2 + 10)
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