import pygame
from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.zoom = 1

    def apply(self, entity):
        # Return adjusted x and y positions for the blob
        x, y = entity.x - self.camera.x, entity.y - self.camera.y
        # Scale the coordinates and size by the zoom factor
        x, y, size = x * self.zoom, y * self.zoom, entity.size * self.zoom
        return x, y, size
    
    def update(self, target):
        # Adjust the camera position based on the player's movement vectors
        self.camera.x += target.dx
        self.camera.y += target.dy

    def world_to_screen(self, x, y):
        # Use your camera's properties to transform the world x, y into screen coordinates.
        screen_x = (x - self.camera.x) * self.zoom  # Assuming self.camera.x is the camera's world x position
        screen_y = (y - self.camera.y) * self.zoom  # Assuming self.camera.y is the camera's world y position

        return screen_x, screen_y
