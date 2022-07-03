import pygame
from un_joueur import main1
from deux_joueurs import main2

pygame.init()
black = 0, 0, 0
white = 255, 255, 255
size = width, height = 513, 513
screen = pygame.display.set_mode(size)
page = 'startscreen'

while 1:
    if page == 'startscreen':
        screen.fill(white)
        pygame.draw.rect(
            screen, black, (50, 200, 200, 100))
        pygame.draw.rect(
            screen, black, (263, 200, 200, 100))
        font = pygame.font.Font(None, 40)
        text = font.render("1 joueur", True, white)
        screen.blit(text, (95, 240))
        text = font.render("2 joueurs", True, white)
        screen.blit(text, (305, 240))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x < 251:
                    print('1 joueur')
                    page = '1 joueur'
                else:
                    print('2 joueurs')
                    page = '2 joueurs'

    if page == '1 joueur':
        main1()
        page = 'endscreen'

    if page == '2 joueurs':
        main2()
        page = 'endscreen'
