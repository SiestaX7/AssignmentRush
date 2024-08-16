# Initiating Game
import pygame
pygame.init()

# Game Running Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()

