import pygame
import sys
import time
import random
import pickle
import textwrap
import os
pygame.init()
#pygame.mixer.init()

# Colour Library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)
gray = (169,169,169)

# File for saving data 
save_file = "savegame.pkl"
# Screen
width, height = 1000, 800
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Assignment Rush")
background = black
framerate = 60
font = pygame.font.Font(None, 30)
achievement_font = pygame.font.Font(None, 28)
timer = pygame.time.Clock()

# Game Variables
money = 0
click_value = 1
passive_income = 0
passive_timer = 0
rebrith_multiplier = 1
rebirth_count = 0
rebirth_cost = 100000
typing_game_reward = 2000
completion_file = "Typing_game_completion.txt"


# Upgrade Cost
active_upgrade_cost = 10
passive_upgrade_cost = 20

# Button Size
button_width, button_height = 200, 50

# Coordinates for upgrades
active_upgrade_x = (width - button_width) // 2
active_upgrade_y = (height - button_height) // 2 + 60
passive_upgrade_x = (width - button_width) // 2
passive_upgrade_y = (height - button_height) // 2 + 120

# Timer for Typing Game
typing_game_interval = 60  # 1 minutes in seconds
last_typing_game_time = time.time()

#Typing game lauch function
from subprocess import call

def open_py_file():
    call(["python","typing_game.py"])

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
#find pair game variables
matches = 0
upgrade_match = 1
Game_over = False
button_width, button_height = 200, 50
rules_button_width, rules_button_height = 60, 30
rules_button_rect = pygame.Rect((width - rules_button_width) // 2, 10, rules_button_width, rules_button_height)
rules_visible = False
rules_font = pygame.font.Font(None, 24)
rules_button_font = pygame.font.Font(None, 20)
def create_rules_text():
    rules = [
        "Game Rules:",
        "1. Click to earn marks",
        "2. Upgrade 'Revise' to increase click value",
        "3. Upgrade 'Study' for passive income",
        "4. Match pairs in the mini-game for bonuses",
        "5. Complete typing games for extra marks",
        "6. Rebirth to multiply your earnings",
        "7. Press 'R' to toggle rules visibility"
    ]
    return rules

def draw_rules_board(screen):
    if rules_visible:
        rules = create_rules_text()
        board_width = 500
        line_height = 30
        board_height = len(rules) * line_height + 20
        
        # Draw the board background
        pygame.draw.rect(screen, (50, 50, 50), (150, 100, board_width, board_height))
        pygame.draw.rect(screen, white, (150, 100, board_width, board_height), 2)
        
        # Draw the rules text
        for i, rule in enumerate(rules):
            rule_surface = rules_font.render(rule, True, white)
            screen.blit(rule_surface, (155, 110 + i * line_height))

def handle_rules_button(event):
    global rules_visible
    if event.type == pygame.MOUSEBUTTONDOWN:
        if rules_button_rect.collidepoint(event.pos):
            rules_visible = not rules_visible
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            rules_visible = not rules_visible
# Defining Functions (Save Game)
def save_game():
    with open(save_file, "wb") as f:
        pickle.dump((money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier, matches),f)
    print("Game Saved!")

# Defining Functions (Load Game)
def load_game():
    global money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier, matches
    if os.path.exists(save_file):
        with open (save_file, "rb") as f:
            money, click_value, passive_income, passive_upgrade_cost, active_upgrade_cost, rebirth_cost, rebirth_count, rebrith_multiplier, matches = pickle.load(f)
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

#check if the typing game is completed and reward the player
def check_typing_game_completion():
    if os.path.exists(completion_file):
        print("detected")
        with open(completion_file,"r")as f:
            status = f.read().strip()
        if status == "completed":
            global money
            money += typing_game_reward
            print("Typing game completed. 2000 marks rewarded!")
            os.remove(completion_file)

# Auto Load Game if Save Exists
load_game()

##Find pair
# Row heights and speeds
row_height = [100, 175, 255]  # y-coordinates for the three rows
row_speed = [2, 3, 1]  # Medium speed for the first and third rows, fast for the second row
# Load and scale images
images = [pygame.image.load(f"mini game find pair//picture//image{i}.jpg") for i in range(1, 9)]
scaled_images = [pygame.transform.scale(img, (50, 50)) for img in images]
# Prepare image pairs
num_boxes = 16  # Total number of boxes needed
image_pairs = scaled_images * ((num_boxes // len(scaled_images)) + 1)  # Duplicate images as needed
image_pairs = image_pairs[:num_boxes] * 2  # Ensure pairs for matching
random.shuffle(image_pairs)
# Box class definition
class Box:
    def __init__(self, y_position, speed, initial_x, image, image_id, direction="right"):
        self.width = 50
        self.height = 50
        self.x = initial_x
        self.y = y_position
        self.speed = speed
        self.direction = direction
        self.image = image
        self.image_id = image_id
        self.matched = False
        self.selected = False

    def move(self):
        if self.direction == "right":
            self.x += self.speed
            if self.x > width:
                self.x = -self.width
        elif self.direction == "left":
            self.x -= self.speed
            if self.x < -self.width:
                self.x = width

    def draw(self, screen):
        if self.matched:
            return
        if self.selected:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, gray, (self.x, self.y, self.width, self.height))
# Create boxes and assign them to rows
boxes = []
num_boxes_per_row = 6
box_index = 0  

for row_index, row in enumerate(row_height):
    row_boxes = []
    min_gap = width // (num_boxes_per_row + 1)
    initial_positions = [(i * (min_gap + 24.5)) % width for i in range(num_boxes_per_row)]
    
    for i in range(num_boxes_per_row):
        direction = "left" if row_index == 1 else "right"
        image = image_pairs[box_index]
        image_id = box_index // 2
        box = Box(row, row_speed[row_index], initial_positions[i], image, image_id, direction)
        row_boxes.append(box)
        box_index += 1

    boxes.append(row_boxes)
# Track selected boxes for matching
selected_boxes = []

# Function to check guesses
def check_guess():        
    global Turn, matches, Wrong, selected_boxes, image_pairs
    first_box, second_box = selected_boxes
    if first_box.image == second_box.image:  # Check if images match
        first_box.matched = True
        second_box.matched = True
        matches += 1
        
        if matches == upgrade_match:
            random_upgrade()            
            matches = 0
        if len(image_pairs) >= 2: 
            first_box.image = image_pairs.pop()
            second_box.image = image_pairs.pop()
            first_box.matched = False
            second_box.matched = False
    # Reset selected status for all boxes
    for box in selected_boxes:
        box.selected = False
    selected_boxes = []
upgrade_message = ""
upgrade_message_timer = 0
UPGRADE_MESSAGE_DURATION = 1 * 60  # 3 seconds at 60 FPS

def random_upgrade():
    global click_value, passive_income, rebirth_multiplier, upgrade_message, upgrade_message_timer
    upgrade_type = random.choice(['click', 'passive'])
    if upgrade_type == 'click':
        click_value += 1
        upgrade_message = "You Get Upgrade Power Click"
    elif upgrade_type == 'passive':
        passive_income += 1
        upgrade_message = "You Get Upgrade Power Passive"
    
    upgrade_message_timer = UPGRADE_MESSAGE_DURATION
# Game Running Loop
running = True
while running:
    screen.fill(black)
    current_time = time.time()

    # Draw buttons
    pygame.draw.rect(screen, red, (passive_upgrade_x, passive_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, purple, (active_upgrade_x, active_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, green, (rebirth_upgrade_x, rebirth_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, (100, 100, 100), rules_button_rect)

    # Draw button texts
    active_upgrade_text = font.render(f"Revise: {active_upgrade_cost} marks", True, white)
    screen.blit(active_upgrade_text, (active_upgrade_x + 10, active_upgrade_y + 10))

    passive_upgrade_text = font.render(f"Study: {passive_upgrade_cost} marks", True, white)
    screen.blit(passive_upgrade_text, (passive_upgrade_x + 10, passive_upgrade_y + 10))

    rebirth_upgrade_text = font.render(f"Rebirth: {rebirth_cost} marks", True, black)
    screen.blit(rebirth_upgrade_text, (rebirth_upgrade_x + 10, rebirth_upgrade_y + 10))

    rules_text = rules_button_font.render("Rules", True, white)
    text_rect = rules_text.get_rect(center=rules_button_rect.center)
    screen.blit(rules_text, text_rect)

    # Draw other game elements
    matches_text = font.render(f'Match: {matches}', True, white)
    screen.blit(matches_text, (800, 25))

    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))
    
    rebirth_text = font.render(f"Rebirths: {rebirth_count}", True, white)
    screen.blit(rebirth_text, (20, 60))

    # Check for typing game trigger
    if current_time - last_typing_game_time >= typing_game_interval:
        open_py_file()
        check_typing_game_completion()
        last_typing_game_time = time.time()

    time_until_next_game = int(typing_game_interval - (current_time - last_typing_game_time))
    next_game_text = font.render(f"Next typing game in: {time_until_next_game} seconds", True, white)
    screen.blit(next_game_text, (width//2 - 150, height - 50))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            money += click_value * rebrith_multiplier

            # Check button clicks
            if active_upgrade_x <= pos[0] <= active_upgrade_x + button_width and active_upgrade_y <= pos[1] <= active_upgrade_y + button_height:
                if money >= active_upgrade_cost:
                    money -= active_upgrade_cost
                    click_value += 1
                    active_upgrade_cost = int(active_upgrade_cost * 1.5)
            
            elif passive_upgrade_x <= pos[0] <= passive_upgrade_x + button_width and passive_upgrade_y <= pos[1] <= passive_upgrade_y + button_height:
                if money >= passive_upgrade_cost:
                    money -= passive_upgrade_cost
                    passive_income += 1
                    passive_upgrade_cost = int(passive_upgrade_cost * 1.5)
            
            elif rebirth_upgrade_x <= pos[0] < rebirth_upgrade_x + button_width and rebirth_upgrade_y <= pos[1] <= rebirth_upgrade_y + button_height:
                if money >= rebirth_cost:
                    rebirth()
            
            elif rules_button_rect.collidepoint(pos):
                rules_visible = not rules_visible

            # Mini-game box handling
            for row_boxes in boxes:
                for box in row_boxes:
                    if not box.matched and box.x < pos[0] < box.x + box.width and box.y < pos[1] < box.y + box.height and not Game_over:
                        if len(selected_boxes) < 2 and box not in selected_boxes:
                            selected_boxes.append(box)
                            box.selected = True
                            if len(selected_boxes) == 2:
                                for row_boxes in boxes:
                                    for box in row_boxes:
                                        box.move()
                                        box.draw(screen)
                                pygame.display.flip()
                                check_guess()
                                pygame.time.delay(200)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                rules_visible = not rules_visible

    # Apply passive income
    passive_timer += 1
    if passive_timer >= 60:
        money += passive_income * rebrith_multiplier
        passive_timer = 0

    # Draw upgrade message if timer is active
    if upgrade_message_timer > 0:
        pygame.draw.rect(screen, gray, [300, height - 490, 450, 60], 0, 5)
        message_text = font.render(upgrade_message, True, white)
        screen.blit(message_text, (380, height - 470))
        upgrade_message_timer -= 1

    # Draw mini-game boxes
    for row_boxes in boxes:
        for box in row_boxes:
            box.move()
            box.draw(screen)
    
    # Draw rules board if visible
    if rules_visible:
        draw_rules_board(screen)

    # Update display
    pygame.display.flip()

    # Cap framerate
    pygame.time.Clock().tick(framerate)

# End of game loop
save_game()
pygame.quit()
sys.exit()
