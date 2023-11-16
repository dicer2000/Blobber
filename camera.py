import pygame as pg
from settings import *

class Camera:
    def __init__(self, width, height):
        self.bounds = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def set_center(self, x, y):
        start_x = x - self.bounds.width // 2
        start_y = y - self.bounds.height // 2
        self.bounds = pg.Rect(start_x, start_y, self.bounds.width, self.bounds.height)

    def apply(self, entity):
        # Return adjusted x and y positions for the blob
        x, y = entity.x - self.bounds.x, entity.y - self.bounds.y
        return x, y
    
    def update(self, target):
        # Adjust the camera position based on the player's movement vectors
        self.bounds.x += target.dx
        self.bounds.y += target.dy

    def world_to_screen(self, x, y):
        # Use your camera's properties to transform the world x, y into screen coordinates.
        screen_x = (x - self.bounds.x) # Assuming self.camera.x is the camera's world x position
        screen_y = (y - self.bounds.y) # Assuming self.camera.y is the camera's world y position

        return screen_x, screen_y
