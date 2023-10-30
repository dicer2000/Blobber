# Common.py
# Common functions used throughout
import socket
from enum import Enum, auto

def clamp(num, min_value, max_value):
   '''Clap a float value between min and max'''
   return max(min(num, max_value), min_value)

def get_private_ip():
    hostname = socket.gethostname()
    ip_list = socket.gethostbyname_ex(hostname)
    for ip in ip_list[2]:
        if not ip.startswith('127.'):
            return ip
    return "127.0.0.1"  # Fallback

class GameModes(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    DEAD = auto()
    WATCHER = auto()
