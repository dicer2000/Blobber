
import pygame as pg
import sys
import random
from settings import *
from blob import *
from camera import *
from spacial_hash import *
from math import hypot

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
        self.new_game()

    def new_game(self):
        # Create a new game
        
        # Create blobs - me first
        pb = PlayerBlob("XOR", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 20, "Yellow", 0.5)
        self.blobs.append(pb)

        # Randomly add 100 other blobs
        for i in range(70):
            b = Blob("food", random.randrange(0, WORLD_WIDTH), random.randrange(0, WORLD_HEIGHT), 10, "white", 0)
            self.blobs.append(b)
        pass

    def update(self):
        
        pg.display.set_caption(f'{self.clock.get_fps():.1f} fps')

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
    
        # Normalize the direction vector
        dir_x /= distance
        dir_y /= distance
        
        # Scale the direction by the blob's speed to get the movement vector
        blob.dx = dir_x * 2.5
        blob.dy = dir_y * 2.5

    def draw(self):
        # Draw to the main Screen
        self.screen.fill('black')
        
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