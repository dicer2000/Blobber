import pygame as pg

# Window settings
RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 800
FPS = 60

# World Size
WORLD = WORLD_WIDTH, WORLD_HEIGHT = WINDOW_WIDTH * 2, WINDOW_HEIGHT * 2

# Blob Settings
MAX_BLOB_VELOCITY = 2.0


# Food Settings
FOOD_COLOR_ARRAY = [
    (173, 216, 230),  # Light Blue (Sky Blue)
    (255, 223, 0),    # Gold
    (144, 238, 144),  # Light Green (LightSeaGreen)
    (255, 165, 0),    # Orange
    (255, 0, 0),      # Red
    (128, 0, 128)     # Purple
]



# Camera Settings
MAX_ZOOM = 5
CAMERA_STEADY  = 0
CAMERA_ZOOMIN  = 1
CAMERA_ZOOMOUT = 2
