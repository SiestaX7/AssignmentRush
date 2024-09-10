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
rebrith_multiplier = 1
rebirth_count = 0
rebirth_cost = 100000

# Upgrade Cost
active_upgrade_cost = 10
passive_upgrade_cost = 20

# Button Size
button_width, button_height = 500, 50

## (Temp) Load images for buttons instead
#active_upgrade_image = pygame.image.load("active_button.png")
#passive_upgrade_image = pygame.image.load("passive_button.png")

## (Temp) Rescaling image to button size
#active_upgrade_image = pygame.transform.scale(500,50)
#passive_upgrade_image = pygame.transform.scale(500,50)

## (Temp) Click Audio and possibly other audios
#click_sound = pygame.mixer.sound("click_sound.wav")

# Upgrade Button Positions
active_upgrade_x, active_upgrade_y = 250, 400
passive_upgrade_x, passive_upgrade_y = 250, 500
rebirth_upgrade_x, rebirth_upgrade_y = 250, 700

# Defining Functions (Save Game)
def save_game():
    with open(save_file, "wb") as f:
        pickle.dump((money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier),f)
    print("Game Saved!")

# Defining Functions (Load Game)
def load_game():
    global money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier
    if os.path.exists(save_file):
        with open (save_file, "rb") as f:
            money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier = pickle.load(f)
        print("Game Loaded!")
    else:
        print("No save file found.")

# Defining Functions (Rebirth)
def rebirth():
    global money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier
    if money >= rebirth_cost:
        money = 0
        click_value = 1
        passive_income = 0
        passive_upgrade_cost = 20
        active_upgrade_cost = 10
        rebirth_count += 1
        rebrith_multiplier += 1
        rebirth_cost *= 2

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
            
            # Everytime click, gain currency
            money += click_value * rebrith_multiplier

            ## (Temp) Click Sound
            #click_sound.play()
            
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
            
            # If Mouse was on rebirth
            if rebirth_upgrade_x <= mouse_x < rebirth_upgrade_x + button_width and rebirth_upgrade_y <= mouse_y <= rebirth_upgrade_y + button_height:
                if money >= rebirth_cost:
                    rebirth()

    # Applying Passive Income
    passive_timer +=1
    if passive_timer >= 60:
        money += passive_income * rebrith_multiplier
        passive_timer = 0
    
    # Draw Button
    pygame.draw.rect(screen, red, (passive_upgrade_x, passive_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, purple, (active_upgrade_x, active_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, green, (rebirth_upgrade_x, rebirth_upgrade_y, button_width, button_height))

    ## (Temp) Show image as button
    #screen.blit(active_upgrade_image, (active_upgrade_x, active_upgrade_y))
    #screen.blit(passive_upgrade_image, (passive_upgrade_x, passive_upgrade_y))

    # Show Cost of Button
    active_upgrade_text = font.render(f"Upgrade Click (+1): {active_upgrade_cost} marks", True, white)
    screen.blit(active_upgrade_text, (active_upgrade_x + 10, active_upgrade_y + 10))

    passive_upgrade_text = font.render(f"Upgrade Passive (+1/s): {passive_upgrade_cost} marks", True, white)
    screen.blit(passive_upgrade_text, (passive_upgrade_x + 10, passive_upgrade_y + 10))

    rebirth_upgrade_text= font.render(f"Rebirth: {rebirth_cost} marks", True, black)
    screen.blit(rebirth_upgrade_text,(rebirth_upgrade_x + 10, rebirth_upgrade_y +10))

    # Show Money
    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))
    rebirth_text = font.render(f"Rebirths:{rebirth_count}", True, white)
    screen.blit(rebirth_text, (20, 60))

    # Update Display
    pygame.display.flip()

    # Cap Framerate
    pygame.time.Clock().tick(framerate)

