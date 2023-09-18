import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Return adjusted x and y positions for the blob
        return entity.x - self.camera.x, entity.y - self.camera.y

    def update(self, target):
        # Adjust the camera position based on the player's movement vectors
        self.camera.x += target.dx
        self.camera.y += target.dy
'''
    def apply(self, entity):
        # Return the translated position
        return entity.x - self.camera.left, entity.y - self.camera.top

    def update(self, target):
        # Center the camera on the target (for example, player)
        x = -target.x + int(self.width / 2)
        y = -target.y + int(self.height / 2)
        
        # Clamp the camera position to prevent showing areas outside the world boundaries
        x = max(0, x)  # left
        y = max(0, y)  # top
        x = min(WORLD_WIDTH - self.width, x)  # right
        y = min(WORLD_HEIGHT - self.height, y)  # bottom
        
        self.camera.topleft = (x, y)
'''