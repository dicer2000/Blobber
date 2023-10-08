# Blob Class
#

import pygame
import noise
import random
from settings import WORLD_HEIGHT, WORLD_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, VERBOSITY
import math

class Blob:
    def __init__(self, name, x, y, size, color, speed=5, wander=0):
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
        self.wander_multiplier = wander
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


    def update(self, player_dx=0, player_dy=0):
        ''' Apply movement vectors to the blob's position '''

        # Adjust based on blob's own movement
        self.world_x += self.dx
        self.world_y += self.dy

        # Boundary checks
        self.world_x = max(min(self.world_x, WORLD_WIDTH - self.size), self.size)
        self.world_y = max(min(self.world_y, WORLD_HEIGHT - self.size), self.size)

        self.x += (self.dx - player_dx)
        self.y += (self.dy - player_dy)

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

'''
    def draw(self, screen, camera, player=False):
        # Translated position based on camera
        tx, ty = self.x, self.y #camera.apply(self)
        size = self.size
        if player:
            tx, ty = self.x, self.y
        
        # If Out of frame, don't draw.  Return immediately
        if not player and ( self.x < 0 or self.y < 0 or self.x > WINDOW_WIDTH or self.y > WINDOW_HEIGHT):
            return

        # Draw everything else
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(size))

        if VERBOSITY > 2:
            # Font rendering for displaying x, y, dx, and dy
            font = pygame.font.SysFont(None, 24)  # Use default font, size 24
            position_text = font.render(f" X: {int(tx)},  Y: {int(ty)}", True, (255, 255, 0))
            change_text = font.render(f"dx: {round(self.dx, 2)}, dy: {round(self.dy,2)}", True, (255, 255, 0))
            velocity_text = font.render(f"wx: {int(self.world_x)}, wy: {int(self.world_y)}", True, (255, 255, 0))

            # Draw the text on the screen
            screen.blit(position_text, (self.x + self.size, self.y))  # Display next to the blob
            screen.blit(change_text, (self.x + self.size, self.y + 20))  # Display next to the blob
            screen.blit(velocity_text, (self.x + self.size, self.y + 40))  # Below the position_text

    def wander(self, step_size=0.05, noise_scale=5.0):
        """
        Update the blob's position using Perlin noise.
        
        Parameters:
        - step_size: how fast the noise offset changes; larger values create more erratic movement
        - noise_scale: scales the noise value; larger values spread the movement over a larger area
        
        Noise scale and Step size are actually factors of the blob 'wander' value
        """
        if self.wander_multiplier == 0:
            return
        
        dx=dy=0
        step_size *= self.wander_multiplier
        noise_scale *= self.wander_multiplier
        # Get Perlin noise values for both x and y directions
        dx = noise.pnoise1(self.noise_offset_x, octaves=3, persistence=0.5, lacunarity=2.0)
        dy = noise.pnoise1(self.noise_offset_y, octaves=3, persistence=0.5, lacunarity=2.0)
        # Update the blob's position
        self.x += dx * noise_scale
        self.y += dy * noise_scale
        self.world_x += dx * noise_scale
        self.world_y += dy * noise_scale
        
        # Increment the noise offset for the next step
        self.noise_offset_x += step_size
        self.noise_offset_y += step_size

