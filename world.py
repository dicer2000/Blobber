# World Class
#

import pygame

class world:
    def __init__(self, world_width, world_height, color=(0, 255, 0), line_width=2):
        self.world_width = world_width
        self.world_height = world_height
        self.color = color
        self.line_width = line_width
        self.grid_color = (200, 200, 200)  # Light gray color for the grid
        self.grid_spacing = 50  # Distance between grid lines, adjust as needed

    def draw(self, screen, camera):
        # Get the transformed coordinates of the world bounds
        top_left = camera.world_to_screen(0, 0)
        top_right = camera.world_to_screen(self.world_width, 0)
        bottom_left = camera.world_to_screen(0, self.world_height)
        bottom_right = camera.world_to_screen(self.world_width, self.world_height)

        self.draw_grid(screen, camera)

        # Draw the rectangle using the transformed coordinates
        points = [top_left, top_right, bottom_right, bottom_left, top_left]  # List of transformed vertices
        pygame.draw.lines(screen, self.color, True, points, self.line_width)



    def draw_grid(self, screen, camera):
        # Horizontal lines
        for y in range(0, self.world_height + self.grid_spacing, self.grid_spacing):
            start = camera.world_to_screen(0, y)
            end = camera.world_to_screen(self.world_width, y)
            pygame.draw.line(screen, self.grid_color, start, end, 1)  # 1 is line width

        # Vertical lines
        for x in range(0, self.world_width + self.grid_spacing, self.grid_spacing):
            start = camera.world_to_screen(x, 0)
            end = camera.world_to_screen(x, self.world_height)
            pygame.draw.line(screen, self.grid_color, start, end, 1)  # 1 is line width
