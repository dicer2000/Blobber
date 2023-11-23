'''
Blobber Game
by Brett Huffman
and (add your name)
Comp Sci 333 - Computer Networking
(c)2023.  All Rights Reserved
-----------------------------------
'''
import pygame as pg
import sys
import random
from settings import *
from common import clamp, get_private_ip
from tweener import Tween, Easing, EasingMode
from socket import getaddrinfo, AF_INET, SOCK_STREAM, SOCK_DGRAM, socket

class main_menu:
    def __init__(self, screen, sounds, start_settings):
        self.screen = screen
        self.sounds = sounds
        self.background_image = pg.transform.scale(pg.image.load('images/bg/blob2.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.input_font = pg.font.Font(None, 32)
        # Initialize Tween for "breathing" effect
        self.breathing_tween = Tween(begin=1.0, 
                                     end=1.04,
                                     duration=1000,
                                     easing=Easing.CIRC,
                                     easing_mode=EasingMode.IN_OUT,
                                     boomerang=True,
                                     loop=True,
                                     reps=0)  # Infinite Reps
        self.breathing_image = pg.image.load('images/blobbie.png')
 
        self.current_question_idx = 0

        # Get the IP Address to show
        start_settings[4]['answer'] = self.get_local_ips()
        self.questions = start_settings # Ask these questions


    def show(self):
        title_font = pg.font.SysFont("Comic Sans", 80)
        info_font = pg.font.SysFont("Comic Sans", 30)
        delta_time = 0
        clock = pg.time.Clock()
        self.breathing_tween.start()

        if BACKGROUND_MUSIC:
            self.sounds['main_menu'].play(-1)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.current_question_idx -= 1


                elif event.type == pg.KEYDOWN:
                    current_question = self.questions[self.current_question_idx]
                    if current_question['options']:  # This is a dropdown
                        if event.key == pg.K_LEFT:
                            selected = current_question['answer'] or 0
                            current_question['answer'] = (selected - 1) % len(current_question['options'])
                        elif event.key == pg.K_RIGHT:
                            selected = current_question['answer'] or 0
                            current_question['answer'] = (selected + 1) % len(current_question['options'])
                        elif event.key == pg.K_RETURN:
                            self.current_question_idx += 1
                    else:  # This is a text input
                        if event.key == pg.K_RETURN:
                            self.current_question_idx += 1
                        elif event.key == pg.K_BACKSPACE:
                            current_question['answer'] = (current_question['answer'] or '')[:-1]
                        else:
                            # 15 Char Max
                            if len(current_question['answer']) < 15:
                                current_question['answer'] = (current_question['answer'] or '') + event.unicode


            # Place background, then title    
            self.screen.blit(self.background_image, (0, 0))

            # Apply the "breathing" effect to the image
            self.breathing_tween.update()
            scale_factor = self.breathing_tween.value
            width, height = self.breathing_image.get_size()
            scaled_image = pg.transform.scale(self.breathing_image, (int(width * scale_factor), int(height * scale_factor)))
            self.screen.blit(scaled_image, (WINDOW_WIDTH // 2 - int(width * scale_factor) // 2+25, WINDOW_HEIGHT // 2 - int(height * scale_factor) // 2+20))

            title_text = title_font.render('Blobber', True, (216, 191, 216))
            self.screen.blit(title_text, [600, 20])
            
            # Show server mode or client mode
            if self.questions[0]['answer'] == IS_SERVER:
                sys_text = info_font.render('Server Mode', True, (216, 191, 216))
                self.screen.blit(sys_text, [40, WINDOW_HEIGHT-80])
            elif self.questions[0]['answer'] == IS_CLIENT:
                sys_text = info_font.render('Client Mode', True, (216, 191, 216))
                self.screen.blit(sys_text, [40, WINDOW_HEIGHT-80])


            # We are done getting info, hook us up to the game
            if self.current_question_idx > len(self.questions)-1:
                if BACKGROUND_MUSIC:
                    self.sounds['main_menu'].stop()
                    self.sounds['gamemusic1'].play(-1)
                return self.questions # Everything we need
            elif self.current_question_idx < 0: # Exit program
                pg.quit()
                sys.exit()

            # Handle Questions
            current_question = self.questions[self.current_question_idx]
            if current_question['options']:
                self.draw_dropdown(current_question['question'],current_question['options'], current_question['answer'], 100, 100)
            else:
                self.draw_text_input(current_question['question'], current_question['answer'], 100, 100)

            pg.display.update()

    def draw_text_input(self, prompt, input_str, x, y):
        prompt_surface = self.input_font.render(prompt, True, (255, 255, 255))
        input_surface = self.input_font.render(input_str, True, (255, 255, 255))
        self.screen.blit(prompt_surface, (x, y))
        self.screen.blit(input_surface, (x + 10, y + 40))
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(x, y + 35, 200, 32), 2)

    def draw_dropdown(self, prompt, options, selected_idx, x, y):
        prompt_surface = self.input_font.render(prompt, True, (255, 255, 255))
        self.screen.blit(prompt_surface, (x, y))
        y += 35
        # Draw left and right arrows
        pg.draw.polygon(self.screen, (255, 255, 255), [(x-20, y+16), (x-10, y), (x-10, y+32)])
        pg.draw.polygon(self.screen, (255, 255, 255), [(x+160, y+16), (x+150, y), (x+150, y+32)])
        # Draw the box
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(x, y, 140, 32), 2)
        # Draw the selected option
        selected_surface = self.input_font.render(options[selected_idx], True, (255, 255, 255))
        self.screen.blit(selected_surface, (x + 10, y + 5))

    def get_local_ips(self):
        try:
            # Create a temporary socket to determine the local IP address
            # The destination doesn't need to be reachable
            with socket(AF_INET, SOCK_DGRAM) as s:
                # Using Google's public DNS server address and port
                s.connect(("8.8.8.8", 80))
                IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        return IP