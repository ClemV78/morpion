import pygame
import sys

pygame.init()
black = 0, 0, 0
white = 255, 255, 255
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
screen.fill(white)

while 1:
    # lignes du morpion
    for i in range(2):
        pygame.draw.rect(
            screen, black, (200*i+200, 50, 3, 500))
        pygame.draw.rect(
            screen, black, (50, 200*i+200, 500, 3))
    # gestion du dessin
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                x, y = pygame.mouse.get_pos()
                pygame.draw.rect(
                    screen, black, (x, y, 5, 5))
    pygame.display.flip()
