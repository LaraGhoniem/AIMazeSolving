#! /usr/bin/env python

import os
import sys
import random
import pygame
from pygame import gfxdraw

class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.collision(dx, dy)

    def collision(self, dx, dy):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Panel(object):
    def __init__(self):
        self.rect = pygame.Rect(487, 1, 260, 450)
        
    def button(self, screen, x,y, text):
        font = pygame.font.SysFont("Italic", 50)
        text_render = font.render(text, 1, (239, 139, 72))
        x, y, w , h = text_render.get_rect()
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))
        return screen.blit(text_render, (x, y))

    def explored(self,screen,x,y,text):
        font1 = pygame.font.SysFont("Italic", 50)
        text_render1 = font1.render(text, 1, (239, 139, 72))
        x, y, w , h = text_render1.get_rect()
        pygame.draw.rect(screen, (100, 100, 100), (x+160, y, 30 , 30))
        return screen.blit(text_render1, (x, y))
    
    def path(self,screen,x,y,text):
        font2 = pygame.font.SysFont("Italic", 50)
        text_render2 = font2.render(text, 1, (239, 139, 72))
        x, y, w , h = text_render2.get_rect()
        pygame.draw.rect(screen, (255, 255, 51), (x+90, y, 30 , 30))
        return screen.blit(text_render2, (x, y))


os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Search Maze Game")
screen = pygame.display.set_mode((750, 450))
clock = pygame.time.Clock()
walls = []
player = Player()
panel = Panel()

# Holds the level layout in a list of strings. 25R 27C
level = """
WWWWWWWWWWWWWWWWWWWWWWWWWWW
W                         W
W   WWWWWWWWWWWWWWWWW   W W
WWW W       W  WW   W   W W
W W W  WW   W   W   W  WWWW
W W W   W       W     WWW W
W   WWWWW  WWWW   W     W W
WW            W  WW   W   W
WWWWWWWWWWWWWWW   W   W   W
W                 WWWWWWWWW
W  WWWWWW  W   WW         W
W   W     WWW  W  W  W W  W
W W WWWWW     WWWWW  WWW  W
WWW   WW    W         W   W
W   W    WWWWWWWWW  WWWWWWW
W  WW       W   W         W
WWWWWWWWWWWWW   WWWWWWW   W
W             W W       WWW
W   WWWWWWW   W    WWWW   W
W   W    W       W  W    WW
W WWW  WWW  WW  WWWWW     W
W   W    WWWW      W  WWWWW
WWWWWWW    W  WW   WWWW   W
W              W W      E W
WWWWWWWWWWWWWWWWWWWWWWWWWWW
""".splitlines()[1:]

# Parse the level string above. W = wall, E = exit
x = y = 1
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 10, 10)
        x += 18
    y += 18
    x = 1

running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        # if e.type == pygame.MOUSEBUTTONDOWN:
        #     if b1.collidepoint(pygame.mouse.get_pos()):
        #         #call function

    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()

    # Draw the scene
    screen.fill((1,8,52))
    for wall in walls:
        pygame.draw.rect(screen, (32, 105, 201), wall.rect)
    pygame.draw.ellipse(screen, (255, 0, 0), end_rect)
    pygame.draw.ellipse(screen, (255, 200, 0), player.rect)
    pygame.draw.rect(screen, (255, 200, 0), panel.rect)
    b1 = panel.button(screen, 500,5, "BFS")
    # b2 = panel.button(screen, 510, 5, "DFS")
    # b3 = panel.button(screen, 490, 10, "UCS")
    # b4 = panel.button(screen, 510, 10, "GBFS")
    # b5 = panel.button(screen, 490, 15, "A*")
    # b6 = panel.explored(screen,490,25,"Explored:")
    # b7 = panel.path(screen,490, 30,"Path:")

    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,128))
    pygame.display.flip()
    clock.tick(360)

pygame.quit()