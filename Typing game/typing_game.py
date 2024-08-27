import pygame
from pygame.locals import *
import random

pygame.init()

#window display
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60
TEXTBOX_WIDTH = 300
TEXTBOX_HEIGHT = 100
word_list = ["assignment", "deadline", "programming"]
FONT = pygame.font.Font(None,36)

target_word = random.choice(word_list)
user_text = ""
feedback_message = ""


def draw_textbox():
    pygame.draw.rect(WIN, GREEN, (100, 50, TEXTBOX_WIDTH, TEXTBOX_HEIGHT))

def draw_text(text, x, y, color):
    text_surface = FONT.render(text, True, color)
    WIN.blit(text_surface,(x, y))

def draw_window():
    WIN.fill((WHITE))
    draw_textbox()
    draw_text(f"Type the word:{target_word}", 110, 60, BLACK)
    draw_text(user_text, 110, 120, BLACK)
    draw_text(feedback_message,110,180, RED)
    pygame.display.update()

#game function
def main():
    global target_word, user_text, feedback_message
    clock = pygame.time.Clock()
    running=True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text == target_word:
                        feedback_message = "NICE!"
                        target_word= random.choice(word_list)
                        user_text =""
                    else:
                        feedback_message = "INCORRECT"
                        user_text = ""
                        
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        draw_window()

    pygame.quit()

if __name__== "__main__":
    main()