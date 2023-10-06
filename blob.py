# Blob Class
#

import pygame
import noise
import random
from settings import WORLD_HEIGHT, WORLD_WIDTH

class Blob:
    def __init__(self, name, x, y, size, color, speed=5):
        self.name = name
        self.x = x
        self.y = y
        self.world_x = x # X coordinate in world space
        self.world_y = y # Y coordinate in world space
        self.dx = self.dy = 0.0 # Not moving
        self.speed = 0
        self.size = size
        self.squared_size = size * size
        self.color = color
        self.speed = speed
        self.noise_offset_x = random.random() * 1000  # Random starting point for noise
        self.noise_offset_y = random.random() * 1000

    # Set a new size and also it's square
    def set_size(self, new_size):
        self.size = new_size
        self.squared_size = new_size * new_size

    def squared_distance(self, blob1, blob2):
        dx = blob1.x - blob2.x
        dy = blob1.y - blob2.y
        return dx * dx + dy * dy

    def has_touched(self, blob1, blob2):
        squared_sum_sizes = blob1.squared_size + blob2.squared_size + 2 * blob1.size * blob2.size  # This accounts for the total squared distance for two circles to touch (size1 + size2)^2
        return self.squared_distance(blob1, blob2) <= squared_sum_sizes

    def has_touched(self, blob2):
        return self.has_touched(self, blob2)

    def draw(self, screen, camera, player=False):
        # Translated position based on camera
        tx, ty, size = camera.apply(self)
        if player:
            tx, ty = self.x, self.y
#        else:
#            self.x, self.y = tx, ty

        # Do this to make sure collissions work
#        self.set_size(size)
        
        # Only draw me if I'm in the frame
        if not player and ( self.x < camera.camera.left or self.y < camera.camera.top or self.x > camera.camera.right or self.y > camera.camera.bottom):
            return

        # Draw everything else
        pygame.draw.circle(screen, self.color, (int(tx), int(ty)), int(size))  # Modify this line

        # Font rendering for displaying x, y, dx, and dy
        font = pygame.font.SysFont(None, 24)  # Use default font, size 24
        position_text = font.render(f" X: {int(tx)},  Y: {int(ty)}", True, (255, 255, 0))
        velocity_text = font.render(f"WX: {int(self.world_x)}, WY: {int(self.world_y)}", True, (255, 255, 0))

        # Draw the text on the screen
        screen.blit(position_text, (tx + self.size + 5, ty))  # Display next to the blob
        screen.blit(velocity_text, (tx + self.size + 5, ty + 25))  # Below the position_text

    def wander(self, step_size=0.05, noise_scale=5.0):
        """
        Update the blob's position using Perlin noise.
        
        Parameters:
        - step_size: how fast the noise offset changes; larger values create more erratic movement
        - noise_scale: scales the noise value; larger values spread the movement over a larger area
        """
        dx=dy=0
        # Get Perlin noise values for both x and y directions
        # dx = noise.pnoise1(self.noise_offset_x, octaves=3, persistence=0.5, lacunarity=2.0)
        # dy = noise.pnoise1(self.noise_offset_y, octaves=3, persistence=0.5, lacunarity=2.0)
        # Update the blob's position
        self.x += dx * noise_scale
        self.y += dy * noise_scale
        
        # Increment the noise offset for the next step
        self.noise_offset_x += step_size
        self.noise_offset_y += step_size

    def update(self, player_dx=0, player_dy=0):
        ''' Apply movement vectors to the blob's position '''

        # Adjust based on blob's own movement
        self.world_x += self.dx
        self.world_y += self.dy

        # Adjust based on PlayerBlob's movement
        self.world_x -= player_dx
        self.world_y -= player_dy

        # Update screen positions
        self.x += (self.dx - player_dx)
        self.y += (self.dy - player_dy)

        # Boundary checks
        self.world_x = max(min(self.world_x, WORLD_WIDTH - self.size), self.size)
        self.world_y = max(min(self.world_y, WORLD_HEIGHT - self.size), self.size)

        '''
        # Can we actually move in direction we want?
        if self.world_x - self.dx > 0:
            # Only if not going to left of world
            self.x -= player_dx
            self.x += self.dx
            self.world_x += self.dx
            self.world_x -= player_dx

        if self.world_y - self.dy > 0:
            # Only if not going off the top of world
            self.y -= player_dy
            self.y += self.dy
            self.world_y -= self.dy
            self.world_y -= player_dy

        # # Boundary checks for x-coordinate
        # if self.world_x - self.size < 0:  # left boundary
        #     self.world_x = self.size
        # elif self.world_x + self.size > WORLD_WIDTH:  # right boundary
        #     self.world_x = WORLD_WIDTH - self.size

        # # Boundary checks for y-coordinate
        # if self.world_y - self.size < 0:  # top boundary
        #     self.world_y = self.size
        # elif self.world_y + self.size > WORLD_HEIGHT:  # bottom boundary
        #     self.world_y = WORLD_HEIGHT - self.size
'''

class PlayerBlob(Blob):
    def __init__(self, name, x, y, size, color, speed=5):
        super().__init__(name, x, y, size, color, speed)
        self.dx = 0  # change in x direction
        self.dy = 0  # change in y direction

    def draw(self, screen, camera):
        super().draw(screen, camera, True)

    def update(self):

        # Update the world_x and world_y based on movement vectors
        self.world_x += self.dx
        self.world_y += self.dy


        # Don't call the super's update here!