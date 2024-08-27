# Initiating Game
import pygame
import sys
import pickle
import os
pygame.init()

# Colour Library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)

# File for Saving Data
save_file = "savegame.pkl"

#Screen
width, height = 800, 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Assignment Rush")
background = black
framerate = 60
font = pygame.font.Font('Lato-Bold.ttf', 30)
timer = pygame.time.Clock()

# Game Variables
money = 0
click_value = 1

# Button Size
button_width, button_height = 200, 50
button_x = (width - button_width) //2
button_y = (height - button_width) //2

# Defining Functions (Save Game)
def save_game():
    with open(save_file, "wb") as f:
        pickle.dump(money,f)
    print("Game Saved!")

# Defining Functions (Load Game)
def load_game():
    global money
    if os.path.exists(save_file):
        with open (save_file, "rb") as f:
            money = pickle.load(f)
        print("Game Loaded!")
    else:
        print("No save file found.")

# Auto Load Game if Save Exists
load_game()

# Game Running Loop
running = True
while running:
    screen.fill(black)

    # Handling Conditions
    for event in pygame.event.get():

        # Quit
        if event.type == pygame.QUIT:
            save_game()
            pygame.quit()
            sys.exit

        # When Click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_width:
                money += click_value
    
    # Draw Button
    pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))

    # Show Money
    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))

    # Update Display
    pygame.display.flip()

    # Cap Framerate
    pygame.time.Clock().tick(framerate)

