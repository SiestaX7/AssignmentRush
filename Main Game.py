import pygame
import sys
import time
import random
import pickle
import os
import textwrap
pygame.init()
pygame.mixer.init()

# Colour Library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)
gray = (169,169,169)
brown =(192, 150, 100)

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
background_image = pygame.image.load("Wooden_Background.png")
background_image = pygame.transform.scale(background_image, (width,height))

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

achievements = {
    "Kindergarten": False,
    "Elementary": False,
    "Middle School": False,
    "High School": False,
    "College": False,
    "Diploma": False,
    "Degree": False,
    "Masters": False,
    "Doctoral": False,
    "Professor": False
}

achievement_conditions = [
    ("Kindergarten", 0),
    ("Elementary", 100),
    ("Middle School", 1000),
    ("High School", 5000),
    ("College", 10000),
    ("Diploma", 25000),
    ("Degree", 50000),
    ("Masters", 100000),
    ("Doctoral", 200000),
    ("Professor", 500000)
]

achievement_popup = []
popup_timer = 0
popup_duration = 180 # 60=1s
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
    pygame.mixer.music.pause()
    call(["python","typing_game.py"])

# Load images for buttons instead
active_upgrade_image = pygame.image.load("Wooden_Button_1.png")
passive_upgrade_image = pygame.image.load("Wooden_Button_1.png")
rebirth_upgrade_image = pygame.image.load("Wooden_Button_2.png")

# Rescaling image to button size
active_upgrade_image = pygame.transform.scale(active_upgrade_image, (500,50))
passive_upgrade_image = pygame.transform.scale(passive_upgrade_image, (500,50))
rebirth_upgrade_image = pygame.transform.scale(rebirth_upgrade_image, (500,50))

# Click Audio and possibly other audios
click_sound = pygame.mixer.Sound("click_sound.mp3")
click_channel = pygame.mixer.Channel(0)

# BGM
pygame.mixer.music.load("Fun_Piano_BGM_by_Sekuora.mp3")
pygame.mixer.music.play(-1)

# Upgrade Button Positions
active_upgrade_x, active_upgrade_y = 250, 400
passive_upgrade_x, passive_upgrade_y = 250, 500
rebirth_upgrade_x, rebirth_upgrade_y = 250, 700

#find pair game variables
matches = 0
upgrade_match = 10
Game_over = False

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

original_rules_image = pygame.image.load("mini game find pair//picture//rules.png")
rules_button_width, rules_button_height = 60, 50  # Adjust these values to your preferred size
rules_button_image = pygame.transform.scale(original_rules_image, (rules_button_width, rules_button_height))
rules_button_rect = rules_button_image.get_rect()
rules_button_rect.topleft = (450, 10)  # Adjust position as needed
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
            screen.blit(rule_surface, (150, 110 + i * line_height))

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

# Defining Functions (Unlock Achievements)
def check_achievements():
    global achievement_popup
    for achievement, threshold in achievement_conditions:
        if not achievements[achievement] and money >= threshold:
            achievements[achievement] = True
            achievement_popup.append(f"Achievement Unlocked: {achievement}")
            print(f"Unlocked {achievement}")

# Defining Functions (Show Achievement Popup)
def show_achievement_popups():
    global popup_timer, achievement_popup
    if achievement_popup:
        popup_timer += 1
        if popup_timer <= popup_duration:
            achievement_text = achievement_popup[0]
            achievement__surface = achievement_font.render(achievement_text, True, green)
            screen.blit(achievement__surface, (20, 100))
        else:
            achievement_popup.pop(0)
            popup_timer = 0
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

            pygame.mixer.music.unpause()

# Auto Load Game if Save Exists
load_game()

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
            pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))

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
    screen.blit(background_image, (0,0))
    current_time = time.time() #track current time
    matches_text = font.render(f'Match: {matches}', True,white)
    screen.blit(matches_text, (800, 25))

    # Draw Rule Button
    screen.blit(rules_button_image, rules_button_rect)
    # Show Rule Button
    rules_text = rules_button_font.render("Rules", True, white)
    text_rect = rules_text.get_rect(center=rules_button_rect.center)
    screen.blit(rules_text, text_rect)

    #Show image as button
    screen.blit(active_upgrade_image, (active_upgrade_x, active_upgrade_y))
    screen.blit(passive_upgrade_image, (passive_upgrade_x, passive_upgrade_y))
    screen.blit(rebirth_upgrade_image, (rebirth_upgrade_x, rebirth_upgrade_y))

    # Show Cost of Button
    active_upgrade_text = font.render(f"Study: {active_upgrade_cost} marks", True, black)
    screen.blit(active_upgrade_text, (active_upgrade_x + 50, active_upgrade_y + 20))

    passive_upgrade_text = font.render(f"Do Quiz: {passive_upgrade_cost} marks", True, black)
    screen.blit(passive_upgrade_text, (passive_upgrade_x + 50, passive_upgrade_y + 20))

    rebirth_upgrade_text= font.render(f"Graduate: {rebirth_cost} marks", True, black)
    screen.blit(rebirth_upgrade_text,(rebirth_upgrade_x + 100, rebirth_upgrade_y + 20))

    # Show Money
    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))
    rebirth_text = font.render(f"Rebirths:{rebirth_count}", True, white)
    screen.blit(rebirth_text, (20, 60)) 

    #check if its time to trigger typing game
    if current_time - last_typing_game_time >= typing_game_interval:
        open_py_file()
        check_typing_game_completion()
        last_typing_game_time = time.time()

    #show time until the next typing game 
    time_until_next_game = int(typing_game_interval - (current_time - last_typing_game_time))
    next_game_text = font.render(f"Test your typing reflexes in: {time_until_next_game} seconds", True, white)
    screen.blit(next_game_text, (width//2 -150, height - 50))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
            handle_rules_button(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            money += click_value * rebrith_multiplier

            # Click Sound
            if not click_channel.get_busy():
                click_channel.play(click_sound)
                
            # Upgrade buttons
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
            
            # If Mouse was on rebirth
            elif rebirth_upgrade_x <= pos[0] < rebirth_upgrade_x + button_width and rebirth_upgrade_y <= pos[1] <= rebirth_upgrade_y + button_height:
                if money >= rebirth_cost:
                    rebirth()

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
           
    # Applying Passive Income
    passive_timer += 1
    if passive_timer >= 60:
        money += passive_income * rebrith_multiplier
        passive_timer = 0

    # In the main game loop, add this after the event handling:
    if upgrade_message_timer > 0:
        pygame.draw.rect(screen, black, [300, height - 490,  450, 60], 0, 5)
        message_text = font.render(upgrade_message, True, white)
        screen.blit(message_text, (380, height - 470))
        upgrade_message_timer -= 1

    # Show Money
    money_text = font.render(f"Marks: {money}", True, white)
    screen.blit(money_text, (20, 20))

    for row_boxes in boxes:
        for box in row_boxes:
            box.move()
            box.draw(screen)
    
    # Check and Unlock Achievements
    check_achievements()

    # Show achievement popups
    show_achievement_popups()

    # Draw rules board if visible
    if rules_visible:
        draw_rules_board(screen)

    # Update Display
    pygame.display.flip()

    # Cap Framerate
    pygame.time.Clock().tick(framerate)

save_game()
pygame.quit()
sys.exit()