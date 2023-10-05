# Common.py
# Common functions used throughout


def clamp(num, min_value, max_value):
   '''Clap a float value between min and max'''
   return max(min(num, max_value), min_value)