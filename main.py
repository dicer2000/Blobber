'''
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
from common import clamp, get_private_ip
from tweener import *
from camera import Camera
from world import world
from spatial_hash import spatial_hash
from pygame.locals import *

# Tween motions
tween = Tween(begin=1.0, 
               end=1.05,
               duration=100,
               easing=Easing.LINEAR,
               easing_mode=EasingMode.IN,
               boomerang=True,
               loop=False,
               reps=1)


# Main game object
class Game:
    def __init__(self) -> None:
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.ip_address = get_private_ip()
        self.game_mode = None
        self.delta_time = 1
        self.blobs = []
        self.spatial_hash = None
        self.zoom_factor = 0
        self.world = world(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.spatial_hash = spatial_hash(COLLISION_CELL_SIZE)
        self.collision_sound = None
        self.sounds = dict()
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
            fb = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, FOOD_COLOR_ARRAY[i%len(FOOD_COLOR_ARRAY)], 0, 1)
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

        # Define a radius for the query
        box = (self.blobs[0].x - COLLISION_BOUNDING_BOX_SIZE, self.blobs[0].y - COLLISION_BOUNDING_BOX_SIZE, self.blobs[0].x + COLLISION_BOUNDING_BOX_SIZE, self.blobs[0].y + COLLISION_BOUNDING_BOX_SIZE)

        # Retrieve the blobs using spatial hash
        nearby_blobs = self.spatial_hash.potential_collisions(self.blobs[0])

        # Handle collisions
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

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')
        
        # Draw the world boundary
        self.world.draw(self.screen, self.camera)
        
        # Draw all the blobs
        for blob in self.blobs[::-1]:
            blob.draw(self.screen, self.camera)

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

    def show_main_menu(self, screen):
        title_font = pg.font.SysFont("Comic Sans", 80)
        menu_font = pg.font.Font(None, 48)
        background_image = pg.image.load('images/bg/blob2.png')
        self.background_image = pg.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Play the game music loop
        if BACKGROUND_MUSIC:
            self.sounds['gamemusic1'].stop()
            self.sounds['main_menu'].play(-1)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()

            keys = pg.key.get_pressed()
            if keys[pg.K_s]:
                self.game_mode = "Server"
                # Play the game music loop
                if BACKGROUND_MUSIC:
                    self.sounds['main_menu'].stop()
                    self.sounds['gamemusic1'].play(-1)

                return
            elif keys[pg.K_c]:
                self.game_mode = "Client"
                # Play the game music loop
                if BACKGROUND_MUSIC:
                    self.sounds['main_menu'].stop()
                    self.sounds['gamemusic1'].play(-1)
                return

            self.screen.blit(self.background_image, (0, 0))
            title_text = title_font.render('Blobber', True, (216, 191, 216))
            server_text = menu_font.render(f'Press "S" for Server Mode: {self.ip_address}', True, (255, 255, 255))
            client_text = menu_font.render('Press "C" for Client Mode', True, (255, 255, 255))

            screen.blit(title_text, [600, 20])
            screen.blit(server_text, [200, WINDOW_HEIGHT - 100])
            screen.blit(client_text, [200, WINDOW_HEIGHT - 50])

            pg.display.update()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                self.game_mode = None
            # Check if the mouse has moved
            elif event.type == pg.MOUSEMOTION:
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
            if self.game_mode == None:
                self.show_main_menu(self.screen)
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