'''
Blobber Game
by Brett Huffman
and (add your name)
Comp Sci 333 - Computer Networking
(c)2023.  All Rights Reserved
-----------------------------------
'''

# Debug settings - Verbosity 0-5
VERBOSITY = 5

# Window settings
RES = WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 800
FPS = 60

# World Settings
WORLD = WORLD_WIDTH, WORLD_HEIGHT = WINDOW_WIDTH * 4, WINDOW_HEIGHT * 4
COLLISION_CELL_SIZE = 50
COLLISION_BOUNDING_BOX_SIZE = 250 # 250 pixels around the center player are checked
IS_CLIENT = 0
IS_SERVER = 1

# Blob Settings
MAX_BLOB_VELOCITY = 2.0
START_BLOB = [
    {'question': 'Client/Server', 'options': ['Client', 'Server'], 'answer': IS_CLIENT},
    {'question': 'Color', 'options': ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple'], 'answer': 0},
    {'question': 'Blob Name', 'options': None, 'answer': ''},
    {'question': 'Hairiness', 'options': ['Dwayne J', 'Baby Fuzz', 'Just Right', 'Hairy Biker', 'Beast Mode'], 'answer': 0},
    {'question': 'Server IP', 'options': None, 'answer': ''},
]
BLOB_COLOR_ARRAY = [
    (249, 50, 107),  # Lighter Red
    (255, 255, 80),  # Lighter Orange
    (255, 255, 50),  # Lighter Yellow
    (89, 196, 93),   # Lighter Green
    (89, 118, 196),  # Lighter Blue
    (167, 89, 196)   # Lighter Purple
]

# Food Settings
FOOD_COLOR_ARRAY = [
    (173, 216, 230),  # Light Blue (Sky Blue)
    (255, 223, 0),    # Gold
    (144, 238, 144),  # Light Green (LightSeaGreen)
    (255, 165, 0),    # Orange
    (191, 54, 12),     # Red
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

