import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
screen.fill('turquoise')
def button(screen, position, text):
    font = pygame.font.SysFont("Italic", 50)
    text_render = font.render(text, 1, (239, 139, 72))
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))

    return screen.blit(text_render, (x, y))


def start():
    print("Ok, let's go")
def explored(screen,position,text):
    font1 = pygame.font.SysFont("Italic", 50)
    text_render1 = font1.render(text, 1, (239, 139, 72))
    x, y, w , h = text_render1.get_rect()
    x, y = position

    pygame.draw.rect(screen, (100, 100, 100), (x+160, y, 30 , 30))
    return screen.blit(text_render1, (x, y))
def path(screen,position,text):
    font2 = pygame.font.SysFont("Italic", 50)
    text_render2 = font2.render(text, 1, (239, 139, 72))
    x, y, w , h = text_render2.get_rect()
    x, y = position

    pygame.draw.rect(screen, (255, 255, 51), (x+90, y, 30 , 30))
    return screen.blit(text_render2, (x, y))
# def timer():
#     i = 0
#
#     # creating a clock object
#     clock = pygame.time.Clock()
#
#     # creating a loop for 5 iterations
#     while i < 5:
#         # setting fps of program to max 1 per second
#         clock.tick(1)
#
#         # printing time used in the previous tick
#         print(clock.get_time())
#
#         # printing compute the clock framerate
#         print(clock.get_fps())
#         i = i + 1
def menu():
    """ This is the menu that waits you to click the s key to start """
    b1 = button(screen, (50, 50), "bfs")
    b2 = button(screen, (150, 50), "dfs")
    b3 = button(screen, (250, 50), "ucs")
    b4 = button(screen, (350, 50), "gbfs")
    b5 = button(screen, (450, 50), "A*")
    b6=explored(screen,(100,250),"explored:")
    b7 =path(screen,(300, 250),"path:")
    #timer()
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                key_to_start = event.key == pygame.K_s or event.key == pygame.K_RIGHT or event.key == pygame.K_UP
                if key_to_start:
                    start()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b1.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    start()
        pygame.display.update()
    pygame.quit()

menu()