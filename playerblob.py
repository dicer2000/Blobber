from blob import Blob
from settings import WORLD_HEIGHT, WORLD_WIDTH, WINDOW_HEIGHT, WINDOW_WIDTH, VERBOSITY

class PlayerBlob(Blob):
    def __init__(self, name, x, y, size, color, speed=5, hair_length = 20, hair_count = 20):
        super().__init__(name, x, y, size, color, speed, hair_length, hair_count)
        self.world_x = x
        self.world_y = y
        
    def draw(self, screen, camera):
        super().draw(screen, camera, True)

    def update(self, camera):

        # Proposed movement
        new_world_x = self.world_x + self.dx
        new_world_y = self.world_y + self.dy

        # Check boundaries for x-coordinate
        if new_world_x - self.size < 1:
            self.dx = max(0, self.dx)
        elif new_world_x + self.size > WORLD_WIDTH - 1:
            self.dx = min(0, self.dx)
        self.x += self.dx

        # Check boundaries for y-coordinate
        if new_world_y - self.size < 1:
            self.dy = max(0, self.dy)
        elif new_world_y + self.size > WORLD_HEIGHT - 1:
            self.dy = min(0, self.dy)
        self.y += self.dy

        # Adjust the camera
        camera.update(self)

        # Don't call the super's update here!