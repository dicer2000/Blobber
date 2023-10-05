
import pygame as pg
import sys
import random
from settings import *
from blob import *
from camera import *
from spacial_hash import *
from math import hypot
from common import clamp
from tweener import *
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
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.spatial_hash = None
        self.zoom_factor = 0
        self.camera_op = CAMERA_STEADY
        self.world_bounds = world(WORLD_WIDTH, WORLD_HEIGHT)
        self.new_game()

    def new_game(self):
        # Create a new game
        
        # Create blobs - me first
        pb = PlayerBlob("XOR", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 20, (255,255,0), 0.5)
        self.blobs.append(pb)

        # Randomly add food blobs
        for i in range(200):
            b = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, FOOD_COLOR_ARRAY[i%len(FOOD_COLOR_ARRAY)], 0)
            self.blobs.append(b)


    def update(self):
        
        pg.display.set_caption(f'{self.clock.get_fps():.1f} fps')

        # Don't let blob go out of the World

        # Boundary checks for x-coordinate
        if self.blobs[0].world_x - self.blobs[0].size < 0:  # left boundary
            self.blobs[0].world_x = self.blobs[0].size
            self.blobs[0].dx = 0
        elif self.blobs[0].world_x + self.blobs[0].size > WORLD_WIDTH:  # right boundary
            self.blobs[0].world_x = WORLD_WIDTH - self.blobs[0].size
            self.blobs[0].dx = 0

        # Boundary checks for y-coordinate
        if self.blobs[0].world_y - self.blobs[0].size < 0:  # top boundary
            self.blobs[0].world_y = self.blobs[0].size
            self.blobs[0].dy = 0
        elif self.blobs[0].world_y + self.blobs[0].size > WORLD_HEIGHT:  # bottom boundary
            self.blobs[0].world_y = WORLD_HEIGHT - self.blobs[0].size
            self.blobs[0].dy = 0


        # Update the zoom level using lerp
        if tween.animating:
            tween.update()
            if self.camera_op == CAMERA_ZOOMIN:
                self.camera.zoom = tween.value
            elif self.camera_op == CAMERA_ZOOMOUT:
                self.camera.zoom = 1 - (tween.value - 1)



        # Update the main player
        self.blobs[0].update()

        # Update the spacial hash since things moved
        # only after everything is done moving
#        self.spatial_hash = spacial_hash(cell_size=100)

        # Update all other blobs
        player_dx = self.blobs[0].dx
        player_dy = self.blobs[0].dy
        for blob in self.blobs[1:]:
            blob.update(player_dx, player_dy)
#            self.spatial_hash.insert(blob)

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


    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')
        
        # Draw the world boundary
        self.world_bounds.draw(self.screen, self.camera)
        
        # Draw all the blobs
        for blob in self.blobs[::-1]:
            blob.draw(self.screen, self.camera)

        # Drawn screen to forefront
        pygame.display.flip()

    def check_events(self):
        # Check for keyboard events
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYUP:
                if event.key == pg.K_MINUS and not tween.animating:  # set target zoom factor to zoom out
                    self.camera_op = CAMERA_ZOOMOUT
                    tween.start()  # start the tween
                elif event.key == pg.K_EQUALS and not tween.animating:  # set target zoom factor to zoom in
                    self.camera_op = CAMERA_ZOOMIN
                    tween.start()  # start the tween

            # Check if the mouse has moved
            elif event.type == pygame.MOUSEMOTION:
                mouseX, mouseY = event.pos
                if len(self.blobs) > 0:
                    self.move_towards(self.blobs[0], mouseX, mouseY)

    def run(self):
        # Called once to manage whole game
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.delta_time = self.clock.tick(FPS)

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()