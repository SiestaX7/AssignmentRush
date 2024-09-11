import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Colour Library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)

# Screen
width, height = 800, 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Assignment Rush")
background = black
framerate = 60
font = pygame.font.Font(None, 30)
timer = pygame.time.Clock()

# Game Variables
money = 0
click_value = 1
passive_income = 0
passive_timer = 0

# Upgrade Cost
active_upgrade_cost = 10
passive_upgrade_cost = 20

# Button Size
button_width, button_height = 200, 50
button_x = (width - button_width) // 2
button_y = (height - button_height) // 2

# Coordinates for upgrades
active_upgrade_x = (width - button_width) // 2
active_upgrade_y = (height - button_height) // 2 + 60
passive_upgrade_x = (width - button_width) // 2
passive_upgrade_y = (height - button_height) // 2 + 120

# Timer for Typing Game
typing_game_interval = 120  # 2 minutes in seconds
last_typing_game_time = time.time()

# Typing Game Variables
typing_game_active = False
typing_game_stages = [
    {"word_list": ["assignment", "deadline", "programming"], "time_limit": 5},
    {"word_list": ["assignment rush game", "deadline is tomorrow", "python programming subject"], "time_limit": 9},
    {"word_list": ["Assignment rush game is fun", "The deadline is tomorrow", "I like python programming subject"], "time_limit": 12},
]
current_stage = 0
target_word = ""
user_text = ""
feedback_message = ""
typing_game_start_time = 0

def reset_typing_game():
    global current_stage, target_word, user_text, feedback_message, typing_game_start_time
    if current_stage < len(typing_game_stages):
        target_word = random.choice(typing_game_stages[current_stage]["word_list"])
        user_text = ""
        feedback_message = ""
        typing_game_start_time = pygame.time.get_ticks()

def draw_typing_game():
    global typing_game_active, current_stage, money
    
    if not typing_game_active:
        return

    time_limit = typing_game_stages[current_stage]["time_limit"]
    elapsed_time = (pygame.time.get_ticks() - typing_game_start_time) // 1000
    time_left = time_limit - elapsed_time

    if time_left <= 0:
        end_typing_game("Time's up!")
        return

    # Draw typing game elements
    pygame.draw.rect(screen, green, (100, 50, 600, 300))
    typing_font = pygame.font.Font(None, 24)
    
    stage_text = typing_font.render(f"Stage {current_stage + 1}", True, black)
    screen.blit(stage_text, (110, 60))
    
    target_text = typing_font.render(f"Type: {target_word}", True, black)
    screen.blit(target_text, (110, 100))
    
    input_text = typing_font.render(user_text, True, black)
    screen.blit(input_text, (110, 140))
    
    feedback_text = typing_font.render(feedback_message, True, red)
    screen.blit(feedback_text, (110, 180))
    
    time_text = typing_font.render(f"Time left: {time_left} seconds", True, black)
    screen.blit(time_text, (110, 220))

def handle_typing_game_input(event):
    global typing_game_active, current_stage, user_text, feedback_message, money

    if not typing_game_active:
        return

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            if user_text == target_word:
                money += 10
                current_stage += 1
                if current_stage < len(typing_game_stages):
                    reset_typing_game()
                else:
                    end_typing_game("All stages completed! +10 marks")
            else:
                end_typing_game("Incorrect. Game Over!")
        elif event.key == pygame.K_BACKSPACE:
            user_text = user_text[:-1]
        else:
            user_text += event.unicode

def end_typing_game(message):
    global typing_game_active, feedback_message
    typing_game_active = False
    feedback_message = message
    display_feedback_message()

def display_feedback_message():
    pygame.draw.rect(screen, white, (200, 300, 400, 100))
    feedback_font = pygame.font.Font(None, 30)
    feedback_text = feedback_font.render(feedback_message, True, black)
    text_rect = feedback_text.get_rect(center=(width // 2, 350))
    screen.blit(feedback_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Display the message for 2 seconds

# Game Running Loop
running = True
while running:
    screen.fill(black)

    # Handling Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not typing_game_active:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                money += click_value

            if active_upgrade_x <= mouse_x <= active_upgrade_x + button_width and active_upgrade_y <= mouse_y <= active_upgrade_y + button_height:
                if money >= active_upgrade_cost:
                    money -= active_upgrade_cost
                    click_value += 1
                    active_upgrade_cost = int(active_upgrade_cost * 1.5)

            if passive_upgrade_x <= mouse_x <= passive_upgrade_x + button_width and passive_upgrade_y <= mouse_y <= passive_upgrade_y + button_height:
                if money >= passive_upgrade_cost:
                    money -= passive_upgrade_cost
                    passive_income += 1
                    passive_upgrade_cost = int(passive_upgrade_cost * 1.5)

        if typing_game_active:
            handle_typing_game_input(event)

    # Applying Passive Income
    passive_timer += 1
    if passive_timer >= 60:
        money += passive_income
        passive_timer = 0

    # Check if it's time to start typing game
    current_time = time.time()
    if not typing_game_active and current_time - last_typing_game_time >= typing_game_interval:
        typing_game_active = True
        current_stage = 0
        reset_typing_game()
        last_typing_game_time = current_time

    if not typing_game_active:
        # Draw main game buttons
        pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))
        pygame.draw.rect(screen, red, (passive_upgrade_x, passive_upgrade_y, button_width, button_height))
        pygame.draw.rect(screen, purple, (active_upgrade_x, active_upgrade_y, button_width, button_height))

        # Show Cost of Button
        active_upgrade_text = font.render(f"Upgrade Click (+1): {active_upgrade_cost} marks", True, white)
        screen.blit(active_upgrade_text, (active_upgrade_x + 10, active_upgrade_y + 10))
        passive_upgrade_text = font.render(f"Upgrade Passive (+1/s): {passive_upgrade_cost} marks", True, white)
        screen.blit(passive_upgrade_text, (passive_upgrade_x + 10, passive_upgrade_y + 10))

        # Show time until next typing game
        time_until_next_game = int(typing_game_interval - (current_time - last_typing_game_time))
        next_game_text = font.render(f"Next typing game in: {time_until_next_game} seconds", True, white)
        screen.blit(next_game_text, (width // 2 - 150, height - 50))

    else:
        draw_typing_game()

    # Show Money
    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))

    # Update Display
    pygame.display.flip()

    # Cap Framerate
    pygame.time.Clock().tick(framerate)

pygame.quit()
sys.exit()