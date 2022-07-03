import pygame
import sys
import matplotlib.pyplot as plt
from reconnaissance_morpion import prediction
from pygame.locals import *
from creation_train_images import diminution_resolution
from jeu_ia import gagne, minimax, libre
from time import sleep
import numpy as np

plateau = np.array([[-3 for _ in range(3)] for _ in range(3)])

# Fonctionnement :
# 1. Un joueur dessine une forme dans une case. Quand il a fini de dessiner dans une case, il appuie sur "Entrée"
# 2. Pour laisser jouer l'ordi, appuyer à nouveau sur "Entrée"
# 3. Revenir à l'étape 1.


def load_image(img, position, scale=(164, 164)):  # img = "pic.png", position = (75,525)
    img = pygame.image.load(img)
    img = pygame.transform.scale(img, scale)
    img_rect = img.get_rect(topleft=position)
    return(img, img_rect)


def main1():
    black = 0, 0, 0
    white = 255, 255, 255
    size = width, height = 513, 513
    screen = pygame.display.set_mode(size)
    screen.fill(white)
    l_formes = []
    num_image = 0
    joueur = -3  # Croix = 1 et Cercle = 0
    ordi = -3
    retour = False
    validation = True
    ordi_a_joue = False
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

        # Fin de la partie
        bol, j = gagne(plateau)
        if bol:
            pygame.display.flip()
            sleep(2)
            #rgb(13, 186, 177)
            screen.fill(black)
            font = pygame.font.Font(None, 40)

            if ordi == j:
                text = font.render(
                    "Aie, peut être pour la prochaine fois ?", True, white)
                screen.blit(text, (15, 255))
            else:
                text = font.render("Bravo !", True, white)
                screen.blit(text, (200, 255))
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

        # l'ordi joue
        if joueur != ordi and validation:
            sc, [i_mm, j_mm] = minimax(plateau, ordi, 2)
            plateau[i_mm, j_mm] = ordi
            print("L'ordi joue dans la case"+str(i_mm)+','+str(j_mm))
            if ordi:
                l_formes.append(load_image(
                    'croix.png', (171*i_mm+2, 171*j_mm+2)))
            else:
                l_formes.append(load_image(
                    'cercle.png', (171*i_mm+2, 171*j_mm+2)))
            joueur = ordi
            ordi_a_joue = False

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
                if event.key == 13 and not validation:
                    validation = True
                    ordi_a_joue = True

                if event.key == 13 and validation and not ordi_a_joue:  # Touche entrée
                    x_case, y_case = x//171, y//171
                    rect = pygame.Rect(171*x_case, 171*y_case, 168, 168)
                    sub = screen.subsurface(rect)
                    path = "images_jeu/inconnue" + str(num_image)+".jpeg"
                    pygame.image.save(sub, path)
                    diminution_resolution(path)
                    num_image += 1
                    predict = prediction(path)
                    validation = False
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

                if joueur == -3:
                    joueur = predict
                    x_case, y_case = x//171, y//171
                    plateau[x_case, y_case] = joueur
                    ordi = 1 - joueur
                elif joueur == predict and not validation:
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
    main1()
