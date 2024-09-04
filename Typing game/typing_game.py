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
TEXTBOX_WIDTH = 700
TEXTBOX_HEIGHT = 100
FONT = pygame.font.Font(None,36)

#stages 
stages = [
    {"word_list":["assignment", "deadline", "programming"], "time_limit" : 5},
    {"word_list":["assignment rush game", "deadline is tomorrow", "python programming subject"], "time_limit" :9},
    {"word_list":["Assignment rush game is fun", "The deadline is tomorrow", "I like python programming subject"], "time_limit" :12},
]

current_stage=0
target_word = random.choice(stages[current_stage]["word_list"])
user_text = ""
feedback_message = ""
time_limit = stages[current_stage]["time_limit"]
start_ticking = pygame.time.get_ticks()

def draw_textbox():
    pygame.draw.rect(WIN, GREEN, (100, 50, TEXTBOX_WIDTH, TEXTBOX_HEIGHT))

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    WIN.blit(text_surface,(x, y))

def draw_window(time_left):
    WIN.fill((WHITE))
    draw_textbox()
    draw_text(f"Stage {current_stage + 1}", 110, 20, BLACK)
    draw_text(f"Type the word:{target_word}", 110, 60, BLACK)
    draw_text(user_text, 110, 120, BLACK)
    draw_text(feedback_message,110,180, RED)
    draw_text(f'Time left: {time_left} seconds', 110, 220, BLACK)
    pygame.display.update()

def reset_game():
    global target_word,user_text, feedback_message, start_ticking, time_limit
    if current_stage < len(stages):
        target_word = random.choice(stages[current_stage]["word_list"])
        user_text = ""
        feedback_message = ""
        time_limit = stages[current_stage]["time_limit"]
        start_ticking = pygame.time.get_ticks()

def next_stage():
    global current_stage
    current_stage += 1
    if current_stage < len(stages):
        reset_game()
    else:
        global feedback_message
#if no more stages end the game
        feedback_message = "Congratulations! You have completed all stages!"
        draw_window(0)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        exit()


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
                        next_stage()
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