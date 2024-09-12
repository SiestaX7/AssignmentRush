import pygame
import sys
import time
import random
# Initialize Pygame
import pickle
import os
import random
pygame.init()

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
#find pair game variables
matches = 0
upgrade_match = 10
Game_over = False
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

# Auto Load Game if Save Exists
load_game()
#find pair
# Row heights and speeds
row_height = [100, 165, 235]  # y-coordinates for the three rows
row_speed = [1, 2, 1]  # Medium speed for the first and third rows, fast for the second row
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
UPGRADE_MESSAGE_DURATION = 2 * 60  # 3 seconds at 60 FPS

def random_upgrade():
    global click_value, passive_income, rebirth_multiplier, upgrade_message, upgrade_message_timer
    upgrade_type = random.choice(['click', 'passive'])
    if upgrade_type == 'click':
        click_value += 1
        upgrade_message = "You get upgrade power click"
    elif upgrade_type == 'passive':
        passive_income += 1
        upgrade_message = "You get upgrade power passive"
    
    upgrade_message_timer = UPGRADE_MESSAGE_DURATION
# Game Running Loop
running = True
while running:
    screen.fill(black)
    matches_text = font.render(f'Match: {matches}', True,white)
    screen.blit(matches_text, (800, 25))
    # Draw Button
    pygame.draw.rect(screen, red, (passive_upgrade_x, passive_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, purple, (active_upgrade_x, active_upgrade_y, button_width, button_height))
    pygame.draw.rect(screen, green, (rebirth_upgrade_x, rebirth_upgrade_y, button_width, button_height))

    # Handling Events

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
    # Handling Conditions

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

       ## elif event.type == pygame.MOUSEBUTTONDOWN and not typing_game_active:
           # mouse_x, mouse_y = pygame.mouse.get_pos()

            #if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                #money += click_value

            #if active_upgrade_x <= mouse_x <= active_upgrade_x + button_width and active_upgrade_y <= mouse_y <= active_upgrade_y + button_height:

                #break
            #save_game()
            #pygame.quit()
            #sys.exit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Everytime click, gain currency
            money += click_value * rebrith_multiplier
            for row_boxes in boxes:
                for box in row_boxes:
                    if not box.matched and box.x < pos[0] < box.x + box.width and box.y < pos[1] < box.y + box.height and not Game_over:
                        if len(selected_boxes) < 2 and box not in selected_boxes:
                            #money += 1
                            selected_boxes.append(box)
                            box.selected = True                           
                            if len(selected_boxes) == 2:
                                for row_boxes in boxes:
                                    for box in row_boxes:
                                        box.move()
                                        box.draw(screen)
                                pygame.display.flip()
                                  # Delay before checking the match
                                check_guess()
                                pygame.time.delay(200)
        # When Click
        #elif event.type == pygame.MOUSEBUTTONDOWN:
            #mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Everytime click, gain currency
            #money += click_value * rebrith_multiplier

            ## (Temp) Click Sound
            #click_sound.play()
            
            # If Mouse was on active income upgrade
            if active_upgrade_x <= pos[0] <= active_upgrade_x + button_width and active_upgrade_y <= pos[1] <= active_upgrade_y + button_height:

                if money >= active_upgrade_cost:
                    money -= active_upgrade_cost
                    click_value += 1
                    active_upgrade_cost = int(active_upgrade_cost * 1.5)

            # If Mouse was on passive income upgrade
            if passive_upgrade_x <= pos[0] <= passive_upgrade_x + button_width and passive_upgrade_y <= pos[1] <= passive_upgrade_y + button_height:
                if money >= passive_upgrade_cost:
                    money -= passive_upgrade_cost
                    passive_income += 1
                    passive_upgrade_cost = int(passive_upgrade_cost *1.5)
            
            # If Mouse was on rebirth
            if rebirth_upgrade_x <= pos[0] < rebirth_upgrade_x + button_width and rebirth_upgrade_y <= pos[1] <= rebirth_upgrade_y + button_height:
                if money >= rebirth_cost:
                    rebirth()

    # Applying Passive Income
    passive_timer += 1
    if passive_timer >= 60:
        money += passive_income * rebrith_multiplier
        passive_timer = 0

    # In the main game loop, add this after the event handling:
    if upgrade_message_timer > 0:
        pygame.draw.rect(screen, gray, [300, height - 490,  450, 60], 0, 5)
        message_text = font.render(upgrade_message, True, white)
        screen.blit(message_text, (380, height - 470))
        upgrade_message_timer -= 1

        if typing_game_active:
            handle_typing_game_input(event)
    # Check if it's time to start typing game
    current_time = time.time()
    if not typing_game_active and current_time - last_typing_game_time >= typing_game_interval:
        typing_game_active = True
        current_stage = 0
        reset_typing_game()
        last_typing_game_time = current_time

    if not typing_game_active:
        # Draw main game buttons
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

    
    for row_boxes in boxes:
        for box in row_boxes:
            box.move()
            box.draw(screen)
    



    # Update Display
    pygame.display.flip()

    # Cap Framerate
    pygame.time.Clock().tick(framerate)

save_game()
pygame.quit()
sys.exit

