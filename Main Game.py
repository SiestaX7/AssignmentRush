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
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Assignment Rush")
background = black
framerate = 60
font = pygame.font.Font('Lato-Bold.ttf', 16)
timer = pygame.time.Clock()

# Game Running Loop
running = True
while running:
    timer.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background)

    pygame.display.flip()

pygame.quit()

