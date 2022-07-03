import pygame
import sys
import matplotlib.pyplot as plt
from reconnaissance_morpion import prediction
from pygame.locals import *
from creation_train_images import diminution_resolution
from jeu_ia import gagne
from time import sleep
import numpy as np
from jeu_ia import libre

plateau = np.array([[-3 for _ in range(3)] for _ in range(3)])

# Fonctionnement :
# 1. Un joueur dessine une forme dans une case. Quand il a fini de dessiner dans une case, il appuie sur "Entrée"
# 2. Si la forme qui s'affiche est la bonne, appuyer sur "Maj". Le prochain joueur peut dessiner dans une nouvelle case
# 3. Sinon, sur la touche "Retour" et revenir à l'étape 1.


def load_image(img, position, scale=(164, 164)):  # img = "pic.png", position = (75,525)
    img = pygame.image.load(img)
    img = pygame.transform.scale(img, scale)
    img_rect = img.get_rect(topleft=position)
    return(img, img_rect)


def main2():
    pygame.init()
    black = 0, 0, 0
    white = 255, 255, 255
    size = width, height = 513, 513
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    l_formes = []
    num_image = 0
    joueur = -3  # Croix = 1 et Cercle = 0
    retour = False
    while 1:
        # lignes du morpion
        for i in range(2):
            pygame.draw.rect(
                screen, black, (171*i+168, 10, 3, 493))
            pygame.draw.rect(
                screen, black, (10, 171*i+168, 493, 3))
        # formes en place
        for forme in l_formes:
            screen.blit(forme[0], forme[1])

        # fin
        bol, j = gagne(plateau)
        if bol:
            pygame.display.flip()
            sleep(2)
            font = pygame.font.Font(None, 40)
            if j:
                screen.fill((13, 186, 177))
                text = font.render(
                    'Bravo, la croix a gagné', True, white)
            else:
                screen.fill((70, 130, 180))
                text = font.render(
                    'Bravo, le cercle a gagné', True, white)
            screen.blit(text, (100, 255))
            pygame.display.flip()
            sleep(3)
            sys.exit()

        if libre(plateau) == []:
            pygame.display.flip()
            sleep(2)
            print('Egalité')
            screen.fill(black)
            font = pygame.font.Font(None, 40)
            text = font.render("Egalité !", True, white)
            screen.blit(text, (200, 255))
            pygame.display.flip()
            sleep(3)
            sys.exit()

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
                if event.key == 13:  # Touche entrée
                    x_case, y_case = x//171, y//171
                    rect = pygame.Rect(171*x_case, 171*y_case, 168, 168)
                    sub = screen.subsurface(rect)
                    path = "images_jeu/inconnue" + str(num_image)+".jpeg"
                    pygame.image.save(sub, path)
                    diminution_resolution(path)
                    num_image += 1
                    predict = prediction(path)
                    if predict:
                        print('Dans la case '+str(x_case)+','+str(y_case) +
                              ' il y a une croix')
                        l_formes.append(load_image(
                            'croix.png', (171*x_case+2, 171*y_case+2)))
                    else:
                        print('Dans la case '+str(x_case)+','+str(y_case) +
                              ' il y a un cercle')
                        l_formes.append(load_image(
                            'cercle.png', (171*x_case+2, 171*y_case+2)))

                if event.key == 8:  # Touche retour
                    print('Pas la bonne forme')
                    l_formes.pop()
                    x_case, y_case = x//171, y//171
                    rect = pygame.Rect(171*x_case+2, 171*y_case+2, 168, 168)
                    pygame.draw.rect(screen, white, rect)
                    predict = 1-predict
                    retour = True

                if joueur == -3:
                    joueur = predict
                    x_case, y_case = x//171, y//171
                    plateau[x_case, y_case] = joueur
                elif joueur == predict:
                    print('Pas le bon joueur')
                    l_formes.pop()
                    x_case, y_case = x//171, y//171
                    rect = pygame.Rect(171*x_case+2, 171*y_case+2, 168, 168)
                    pygame.draw.rect(screen, white, rect)
                else:
                    joueur = predict
                    x_case, y_case = x//171, y//171
                    plateau[x_case, y_case] = joueur

                if retour:
                    plateau[x_case, y_case] = -3
                    retour = False

        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main2()
