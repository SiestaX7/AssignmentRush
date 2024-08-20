# Initiating Game
import pygame
pygame.init()

# Colour Library
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (127, 0, 255)
orange = (255, 165, 0)

#Screen
screen = pygame.display.set_mode([800, 800])
pygame.display.set_caption("Assignment Rush")
background = black
framerate = 60
font = pygame.font.Font('Lato-Bold.ttf', 30)
timer = pygame.time.Clock()

# Defining "Draw"
def draw(colour, y_coord, value):
    pygame.draw.circle(screen, colour, (100, y_coord), 50, 5)
    value_text = (font.render(str(value), True, white))
    screen.blit(value_text, (90, y_coord - 10))

# Game Running Loop
running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)
    draw(green, 100, 1)

    pygame.display.flip()

pygame.quit()

