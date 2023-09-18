# Blob Class
#

import pygame

class Blob:
    def __init__(self, name, x, y, size, color, speed=5):
        self.name = name
        self.x = x
        self.y = y
        self.dx = self.dy = 0.0 # Not moving
        self.speed = 0
        self.size = size
        self.squared_size = size * size
        self.color = color
        self.speed = speed

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
        if player:
            tx, ty = self.x, self.y
        else:
            tx, ty = camera.apply(self)

        pygame.draw.circle(screen, self.color, (tx, ty), self.size)

        # Font rendering for displaying x, y, dx, and dy
        font = pygame.font.SysFont(None, 24)  # Use default font, size 24
        position_text = font.render(f"X: {self.x}, Y: {self.y}", True, (255, 255, 0))  # Black color
        velocity_text = font.render(f"DX: {self.dx:.2f}, DY: {self.dy:.2f}", True, (255, 255, 0))

        # Draw the text on the screen
        screen.blit(position_text, (tx + self.size + 5, ty))  # Display next to the blob
        screen.blit(velocity_text, (tx + self.size + 5, ty + 25))  # Below the position_text


    def update(self, player_dx=0, player_dy=0):
        # Apply movement vectors to the blob's position
        # Adjust blob's position based on PlayerBlob's movement vectors
        self.x -= player_dx
        self.y -= player_dy
        self.x += self.dx
        self.y += self.dy

class PlayerBlob(Blob):
    def __init__(self, name, x, y, size, color, speed=5):
        super().__init__(name, x, y, size, color, speed)
        self.dx = 0  # change in x direction
        self.dy = 0  # change in y direction

    def draw(self, screen, camera):
        camera.update(self)
        super().draw(screen, camera, True)


    def update(self):
        return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.dx = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.dx = self.speed
        else:
            self.dx = 0
        
        if keys[pygame.K_UP]:
            self.dy = -self.speed
        elif keys[pygame.K_DOWN]:
            self.dy = self.speed
        else:
            self.dy = 0

#        self.x += self.dx
#        self.y += self.dy
