import pygame
import random
import sys

pygame.init()

# Window display
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)
RED = (255, 69, 0)
DARK_BLUE = (0, 51, 102)

# Constants
FPS = 60
TEXTBOX_WIDTH = 800
TEXTBOX_HEIGHT = 150
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)

# load background image
background_image = pygame.image.load("Assets//picture//typing game ui.jpg")
background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
# Stages
stages = [
    {"word_list": ["assignment", "deadline", "programming"], "time_limit": 5},
    {"word_list": ["assignment rush game", "deadline is tomorrow", "python programming subject"], "time_limit": 9},
    {"word_list": ["Assignment rush game is fun", "The deadline is tomorrow", "I like python programming subject"], "time_limit": 12},
]

current_stage = 0
target_word = random.choice(stages[current_stage]["word_list"])
user_text = ""
feedback_message = ""
time_limit = stages[current_stage]["time_limit"]
start_ticking = pygame.time.get_ticks()

completion_file = "Typing_game_completion.txt"

#bgm 
pygame.mixer.music.load("Assets//audio//typinggamebgm.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) #-1 mkaes loop indefinitely



# Function to draw a rounded rectangle
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

def draw_window(time_left):
    WIN.blit(background_image, (0, 0))  # Blit the background image

    # Draw the textbox with rounded corners
    textbox_rect = pygame.Rect(100, 50, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)
    draw_rounded_rect(WIN, DARK_BLUE, textbox_rect, 20)
    
    # Display stage number (you can adjust as needed)
    draw_text(f"Stage {current_stage + 1}", 110, 20, WHITE, FONT_SMALL)
    
    # Calculate position to center the target word in the textbox
    target_word_surface = FONT_LARGE.render(f"Type the word: {target_word}", True, WHITE)
    target_word_width, target_word_height = target_word_surface.get_size()
    
    # Calculate centered position within the textbox
    centered_x = textbox_rect.x + (TEXTBOX_WIDTH - target_word_width) // 2
    centered_y = textbox_rect.y + (TEXTBOX_HEIGHT - target_word_height) // 2

    # Draw the target word inside the textbox
    WIN.blit(target_word_surface, (centered_x, centered_y))
    
    # Display user input text (inside the textbox)
    user_input_surface = FONT_LARGE.render(user_text, True, WHITE)
    user_text_width, _ = user_input_surface.get_size()
    user_text_x = textbox_rect.x + (TEXTBOX_WIDTH - user_text_width) // 2
    WIN.blit(user_input_surface, (user_text_x, centered_y + 40))  # Adjust y-offset for user input

    # Display feedback message
    draw_text(feedback_message, 110, 180, RED, FONT_MEDIUM)
    
    # Display remaining time (in white)
    draw_text(f"Time left: {time_left} seconds", 110, 220, WHITE, FONT_SMALL)
    
    # Display progress bar
    draw_progress_bar(WIN, 110, 250, 300, 20, time_left / time_limit)
    
    pygame.display.update()


# Function to draw text with a chosen font and color
def draw_text(text, x, y, color, font):
    text_surface = font.render(text, True, color)
    WIN.blit(text_surface, (x, y))

# Function to draw a progress bar
def draw_progress_bar(surface, x, y, width, height, progress):
    border_color = WHITE
    fill_color = GREEN
    border_rect = pygame.Rect(x, y, width, height)
    fill_rect = pygame.Rect(x, y, width * progress, height)
    pygame.draw.rect(surface, border_color, border_rect, 2)
    pygame.draw.rect(surface, fill_color, fill_rect)

# Function to reset the game for the next stage
def reset_game():
    global target_word, user_text, feedback_message, start_ticking, time_limit
    if current_stage < len(stages):
        target_word = random.choice(stages[current_stage]["word_list"])
        user_text = ""
        feedback_message = ""
        time_limit = stages[current_stage]["time_limit"]
        start_ticking = pygame.time.get_ticks()

# Function to proceed to the next stage
def next_stage():
    global current_stage
    current_stage += 1
    if current_stage < len(stages):
        reset_game()
    else:
        global feedback_message
        feedback_message = "Congratulations! You have completed all stages!"
        draw_window(0)
        pygame.display.update()
        pygame.time.delay(3000)
        with open(completion_file, "w") as f:
            f.write("completed")
        pygame.quit()
        sys.exit()

# Main game loop
def main():
    global target_word, user_text, feedback_message, start_ticking
    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)
        seconds = (pygame.time.get_ticks() - start_ticking) // 1000
        time_left = time_limit - seconds  # Calculate remaining time

        if time_left <= 0:
            feedback_message = "Time's up! Game Over!"
            draw_window(0)
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

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
    sys.exit()

main()
