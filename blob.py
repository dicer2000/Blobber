# Blob Class
#

import pygame
from opensimplex import OpenSimplex
import random
from settings import WORLD_HEIGHT, WORLD_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, VERBOSITY
import math
import time

class Blob:
    def __init__(self, name, x, y, size, color, speed=5, wander=0, hair_length = 20, hair_count = 20):
        self.name = name

        # World coordinates removed as everything is world
        # the camera class converts them to camera-ready
        self.x = x # Camera-relative X coordinate
        self.y = y # Camera-relative Y coordinate

        self.dx = self.dy = 0.0 # Not moving
        self.size = size
        self.squared_size = size * size
        self.color = color
        self.speed = speed
        self.wander_multiplier = wander
        self.hair_size = hair_length
        self.hair_count = hair_count
        self.noise_offset_x = random.random() * 1000  # Random starting point for noise
        self.noise_offset_y = random.random() * 1000
        self.simplex_noise = OpenSimplex(seed=int(time.time()))
        # self.font = pygame.font.SysFont(None, 24)

    # Set a new size and also it's square
    def set_size(self, new_size):
        self.size = new_size
        self.squared_size = new_size * new_size

    def squared_distance(self, blob1, blob2):
        dx = blob1.x - blob2.x
        dy = blob1.y - blob2.y
        return dx * dx + dy * dy

    def has_touched(self, blob2):
        squared_sum_sizes = self.squared_size + blob2.squared_size + 2 * self.size * blob2.size  # This accounts for the total squared distance for two circles to touch (size1 + size2)^2
        return self.squared_distance(self, blob2) <= squared_sum_sizes


    def update(self, player_dx=0, player_dy=0):
        ''' Apply movement vectors to the blob's position '''
        self.x += self.dx
        self.y += self.dy

        # Boundary checks
        self.x = max(min(self.x, WORLD_WIDTH - self.size), self.size)
        self.y = max(min(self.y, WORLD_HEIGHT - self.size), self.size)

    def draw(self, screen, camera, player=False):
        # Translated position based on camera
        tx, ty = camera.apply(self) #self.x, self.y
        
        # If Out of frame, don't draw.  Return immediately
        if not player and ( tx < 0 or ty < 0 or tx > WINDOW_WIDTH or ty > WINDOW_HEIGHT):
            return

        # Draw everything
        pygame.draw.circle(screen, self.color, (int(tx), int(ty)), self.size)
        self.draw_hairs(int(tx), int(ty), screen)

        # Commented out because fonts don't work with pickle
#         if VERBOSITY > 2:
#             # Font rendering for displaying x, y, dx, and dy
#             position_text = self.font.render(f"x: {int(self.x)}, y: {int(self.y)}", True, (255, 255, 0))
#             trans_position_text = self.font.render(f" tx: {int(tx)},  ty: {int(ty)}", True, (255, 255, 0))
#             velocity_text = self.font.render(f"dx: {round(self.dx, 2)}, dy: {round(self.dy,2)}", True, (255, 255, 0))

# #            Draw the text on the screen
#             screen.blit(position_text, (tx + self.size, ty + 20))  # Display next to the blob
#             screen.blit(trans_position_text, (tx + self.size, ty + 40))  # Display next to the blob
#             screen.blit(velocity_text, (tx + self.size, ty + 60))  # Below the position_text
    
    def draw_hairs(self, tx, ty, screen):
        '''Draw hairs around a player at a certain translated position'''
        noise_scale = 1.5  # Scale of the noise, adjust for more/less variation

        for i in range(self.hair_count):
            angle = 2 * math.pi * i / self.hair_count

            current_time = int(time.time() * 10 * random.random()) 

            # Use sine functions for more dynamic, wavy hair
            # Adjust 0.1 and 3 for varying frequency and amplitude
            hair_length = self.hair_size + 5 * math.sin(0.3 * current_time + angle)

            start_x = tx + self.size * math.cos(angle)
            start_y = ty + self.size * math.sin(angle)
            end_x = tx + (self.size + hair_length) * math.cos(angle)
            end_y = ty + (self.size + hair_length) * math.sin(angle)

            pygame.draw.line(screen, self.color, (start_x, start_y), (end_x, end_y ), 1)


    def wander(self, step_size=0.05, noise_scale=5.0):
        """
        Update the blob's position using noise.

        Parameters:
        - step_size: how fast the noise offset changes; larger values create more erratic movement
        - noise_scale: scales the noise value; larger values spread the movement over a larger area

        Noise scale and Step size are actually factors of the blob 'wander' value
        """
        if self.wander_multiplier == 0:
            return
        
        dx = dy = 0
        step_size *= self.wander_multiplier
        noise_scale *= self.wander_multiplier

        # Get noise values for both x and y directions using noise2 function
        dx = self.simplex_noise.noise2(x=self.noise_offset_x, y=self.noise_offset_x)
        dy = self.simplex_noise.noise2(x=self.noise_offset_y, y=self.noise_offset_y)
        
        # Update the blob's position
        self.x += dx * noise_scale
        self.y += dy * noise_scale
#        self.world_x += dx * noise_scale
#        self.world_y += dy * noise_scale
        
        # Increment the noise offset for the next step
        self.noise_offset_x += step_size
        self.noise_offset_y += step_size

    # Setter for speed
    def set_speed(self, new_speed):
        self.speed = new_speed

    # Setter for color
    def set_color(self, new_color):
        self.color = new_color

    # Setter for hair_size
    def set_hair_size(self, new_hair_size):
        self.hair_size = new_hair_size

    # Setter for hair_count
    def set_hair_count(self, new_hair_count):
        self.hair_count = new_hair_count

    # Setter for name
    def set_name(self, new_name):
        self.name = new_name