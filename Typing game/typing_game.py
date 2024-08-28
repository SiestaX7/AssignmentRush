import pygame
from pygame.locals import *
import random

pygame.init()

#window display
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

#constant and variables
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
TEXTBOX_WIDTH = 400
TEXTBOX_HEIGHT = 100
word_list = ["assignment", "deadline", "programming"]
FONT = pygame.font.Font(None,36)

target_word = random.choice(word_list)
user_text = ""
feedback_message = ""
time_limit = 5
start_ticking = pygame.time.get_ticks()

def draw_textbox():
    pygame.draw.rect(WIN, GREEN, (100, 50, TEXTBOX_WIDTH, TEXTBOX_HEIGHT))

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    WIN.blit(text_surface,(x, y))

def draw_window(time_left):
    WIN.fill((WHITE))
    draw_textbox()
    draw_text(f"Type the word:{target_word}", 110, 60, BLACK)
    draw_text(user_text, 110, 120, BLACK)
    draw_text(feedback_message,110,180, RED)
    draw_text(f'Time left: {time_left} seconds', 110, 220, BLACK)
    pygame.display.update()

#game function
def main():
    global target_word, user_text, feedback_message, start_ticking
    clock = pygame.time.Clock()
    running=True

    while running:
        clock.tick(FPS)
        seconds = (pygame.time.get_ticks() - start_ticking) // 1000
        time_left = time_limit - seconds #calculate remaining time

        if time_left<=0:
            feedback_message = "Time's up! Game Over!"
            draw_window(0)
            pygame.time.delay(2000) #wait a bit before quitting
            running = False
            continue 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text == target_word:
                        feedback_message = "NICE!"
                        target_word= random.choice(word_list)
                        user_text =""
                        start_ticking = pygame.time.get_ticks() #reset timer
                    else:
                        feedback_message = "INCORRECT"
                        user_text = ""       
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        draw_window(time_left)

    pygame.quit()

if __name__== "__main__":
    main()