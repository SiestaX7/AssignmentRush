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
width, height = 1000, 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Assignment Rush")
background = black
framerate = 60
font = pygame.font.Font('Lato-Bold.ttf', 30)
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
button_width, button_height = 500, 50
button_x = (width - button_width) //2
button_y = (height - button_width) //2

# Upgrade Button Positions
active_upgrade_x, active_upgrade_y = 250, 400
passive_upgrade_x, passive_upgrade_y = 250, 500

# Defining Functions (Save Game)
def save_game():
    with open(save_file, "wb") as f:
        pickle.dump((money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost),f)
    print("Game Saved!")

# Defining Functions (Load Game)
def load_game():
    global money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost
    if os.path.exists(save_file):
        with open (save_file, "rb") as f:
            money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost = pickle.load(f)
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
            
            # If Mouse was on main button
            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_width:
                money += click_value
            
            # If Mouse was on active income upgrade
            if active_upgrade_x <= mouse_x <= active_upgrade_x + button_width and active_upgrade_y <= mouse_y <= active_upgrade_y + button_height:
                if money >= active_upgrade_cost:
                    money -= active_upgrade_cost
                    click_value += 1
                    active_upgrade_cost = int(active_upgrade_cost *1.5)

            # If Mouse was on passive income upgrade
            if passive_upgrade_x <= mouse_x <= passive_upgrade_x + button_width and passive_upgrade_y <= mouse_y <= passive_upgrade_y + button_height:
                if money >= passive_upgrade_cost:
                    money -= passive_upgrade_cost
                    passive_income += 1
                    passive_upgrade_cost = int(passive_upgrade_cost *1.5)

    # Applying Passive Income
    passive_timer +=1
    if passive_timer >= 60:
        money += passive_income
        passive_timer = 0
    
    # Draw Button
    pygame.draw.rect(screen, green, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, red, (passive_upgrade_x, passive_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, purple, (active_upgrade_x, active_upgrade_y, button_width, button_height))

    # Show Cost of Button
    active_upgrade_text = font.render(f"Upgrade Click (+1): {active_upgrade_cost} marks", True, white)
    screen.blit(active_upgrade_text, (active_upgrade_x + 10, active_upgrade_y + 10))
    passive_upgrade_text = font.render(f"Upgrade Passive (+1/s): {passive_upgrade_cost} marks", True, white)
    screen.blit(passive_upgrade_text, (passive_upgrade_x + 10, passive_upgrade_y + 10))


    # Show Money
    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))

    # Update Display
    pygame.display.flip()

    # Cap Framerate
    pygame.time.Clock().tick(framerate)

