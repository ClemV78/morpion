import pygame
import sys
import matplotlib.pyplot as plt
"""
pygame.init()
black = 0, 0, 0
white = 255, 255, 255
size = width, height = 513, 513
screen = pygame.display.set_mode(size)
screen.fill(white)
num_image = 0

while 1:
    # lignes du morpion
    for i in range(2):
        pygame.draw.rect(
            screen, black, (171*i+168, 10, 3, 493))
        pygame.draw.rect(
            screen, black, (10, 171*i+168, 493, 3))
    # gestion du dessin
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                x, y = pygame.mouse.get_pos()
                pygame.draw.rect(
                    screen, black, (x-3, y-3, 12, 12))
        if event.type == pygame.KEYDOWN:
            for i in range(3):
                for j in range(3):
                    rect = pygame.Rect(171*i, 171*j, 168, 168)
                    sub = screen.subsurface(rect)
                    pygame.image.save(sub, "images_test/cross" +
                                      str(num_image)+".jpeg")
                    num_image += 1
            screen.fill(white)

    pygame.display.flip()

"""


def diminution_resolution(path):
    img = plt.imread(path)
    img = img[::6, ::6, 0]
    # print(img)
    # print(img.shape)
    # plt.imshow(img)
    # plt.show()
    plt.imsave(path, img)
    # print('done', path)


def diminution_globale(n_max):
    for i in range(n_max):
        diminution_resolution("images_test/cross" +
                              str(i)+".jpeg")


# diminution_globale(9)
