
# Debug settings - Verbosity 0-5
VERBOSITY = 0

# Window settings
RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 800
FPS = 60

# World Settings
WORLD = WORLD_WIDTH, WORLD_HEIGHT = WINDOW_WIDTH * 4, WINDOW_HEIGHT * 4
COLLISION_CELL_SIZE = 50
COLLISION_BOUNDING_BOX_SIZE = 250 # 250 pixels around the center player are checked
GAME_MODE = None

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

# Sound settings
BACKGROUND_MUSIC = False
GAME_SOUNDS = True
SOUNDS = ['collision.wav',
          'bonus1.mp3',
          'bonus2.mp3',
          'gamemusic1.ogg',
          'winner.mp3', 
          'main_menu.ogg' ]

