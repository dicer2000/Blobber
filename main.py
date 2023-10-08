from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame as pg
import sys
import random
from settings import *
from blob import Blob
from playerblob import PlayerBlob
from spacial_hash import *
from math import hypot
from common import clamp
from tweener import *
from camera import Camera
from world import world

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
        self.delta_time = 1
        self.blobs = []
        self.spatial_hash = None
        self.zoom_factor = 0
        self.world = world(WORLD_WIDTH, WORLD_HEIGHT)
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.new_game()

    def new_game(self):
        ''' Create a new game '''
        
        # Create blobs - Main Player first (so always in index=0 position)
        pb = PlayerBlob("main_player", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 20, (255,255,0), 0.5)
        self.blobs.append(pb)

        # Randomly add food blobs
        for i in range(200):
            b = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, FOOD_COLOR_ARRAY[i%len(FOOD_COLOR_ARRAY)], 0, 1)
            self.blobs.append(b)

    def update(self):
        ''' Update executed once per frame '''
        # Caption for now        
        pg.display.set_caption(f'{self.clock.get_fps():.1f} fps')

        # Update the main player
        self.blobs[0].update(self.camera)

        # Update the spacial hash since things moved
        # only after everything is done moving
#        self.spatial_hash = spacial_hash(cell_size=100)

        # Update all other blobs
        player_dx = self.blobs[0].dx
        player_dy = self.blobs[0].dy
        for blob in self.blobs[1:]:
            blob.wander()
            blob.update(player_dx, player_dy)
#            self.spatial_hash.insert(blob)


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



    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            # Check if the mouse has moved
            elif event.type == pg.MOUSEMOTION:
                mouseX, mouseY = event.pos
                if len(self.blobs) > 0:
                    self.move_towards(self.blobs[0], mouseX, mouseY)

    def run(self):
        # Called once to manage whole game
        while True:
            # Order is very important here
            self.check_events()
            self.update()
            self.draw()
            self.delta_time = self.clock.tick(FPS)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()