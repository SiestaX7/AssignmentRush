import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Text fonts
title_font = pygame.font.Font('freesansbold.ttf', 56)
small_font = pygame.font.Font('freesansbold.ttf', 26)

# Game variables
Turn = 0
matches = 0
Wrong = 0
Game_over = False

# Colors
white = (255, 255, 255)
gray = (169, 169, 169)
black = (0, 0, 0)

# Row heights and speeds
row_height = [50, 150, 250]  # y-coordinates for the three rows
row_speed = [1, 2, 1]  # Medium speed for the first and third rows, fast for the second row

# Load and scale images
images = [pygame.image.load(f"mini game find pair//picture//image{i}.jpg") for i in range(1, 9)]
scaled_images = [pygame.transform.scale(img, (50, 50)) for img in images]

# Prepare image pairs
num_boxes = 45  # Total number of boxes needed
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
            if self.x > screen_width:
                self.x = -self.width
        elif self.direction == "left":
            self.x -= self.speed
            if self.x < -self.width:
                self.x = screen_width

    def draw(self, screen):
        if self.matched:
            return
        if self.selected:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, gray, (self.x, self.y, self.width, self.height))

# Create boxes and assign them to rows
boxes = []
num_boxes_per_row = 15
box_index = 0  

for row_index, row in enumerate(row_height):
    row_boxes = []
    min_gap = screen_width // (num_boxes_per_row + 10)
    initial_positions = [(i * (min_gap + 24.5)) % screen_width for i in range(num_boxes_per_row)]
    
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
        if len(image_pairs) >= 2: 
            first_box.image = image_pairs.pop()
            second_box.image = image_pairs.pop()
            first_box.matched = False
            second_box.matched = False
    else:
        Wrong += 1
    Turn += 1
    # Reset selected status for all boxes
    for box in selected_boxes:
        box.selected = False
    selected_boxes = []
# Function to reset the game
def reset_game():
    global Turn, matches, Wrong, Game_over, selected_boxes
    Turn = 0
    matches = 0
    Wrong = 0
    Game_over = False
    selected_boxes = []
    random.shuffle(image_pairs)
    # Reinitialize the boxes with shuffled images
    box_index = 0
    for row_boxes in boxes:
        for box in row_boxes:
            box.image = image_pairs[box_index]
            box.matched = False
            box.selected = False
            box_index += 1
# Main game loop
running = True
clock = pygame.time.Clock()
while running:    
    screen.fill(white)
    Turn_text = small_font.render(f'Turn: {Turn}', True, black)
    screen.blit(Turn_text, (705, 500))
    matches_text = small_font.render(f'Match: {matches}', True, black)
    screen.blit(matches_text, (680, 530))    
    Wrong_text = small_font.render(f'Wrong: {Wrong}', True, black)
    screen.blit(Wrong_text, (680, 560))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
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
                                pygame.time.delay(500)  # Delay before checking the match
                                check_guess()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
    for row_boxes in boxes:
        for box in row_boxes:
            box.move()
            box.draw(screen)
    if Wrong == 7:
        Game_over = True
        pygame.draw.rect(screen, black, [10, screen_height - 360, screen_width - 20, 80], 0, 5)
        lose_text = title_font.render("You lose", True, white)
        screen.blit(lose_text, (300, screen_height - 350))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
