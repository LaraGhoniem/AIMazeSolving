#! /usr/bin/env python
import os
import sys
import random
import pygame
import time
import collections
from pygame import gfxdraw

goalx = 24
goaly = 23

class Player(object):
    def __init__(self,pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

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

class Explored(object):
    def __init__(self, pos):
        exp.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


class Panel(object):
    def __init__(self):
        self.rect = pygame.Rect(487, 1, 260, 450)

    def button(self, screen, position, text):
        font = pygame.font.SysFont("Italic", 50)
        text_render = font.render(text, 1, (239, 139, 72))
        x, y, w, h = text_render.get_rect()
        x,y =position
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w, h))
        return screen.blit(text_render, (x, y))

    def explored(self, screen, position, text):
        font1 = pygame.font.SysFont("Italic", 50)
        text_render1 = font1.render(text, 1, (239, 139, 72))
        x, y, w, h = text_render1.get_rect()
        x,y= position
        pygame.draw.rect(screen, (100, 100, 100), (x + 160, y, 30, 30))
        return screen.blit(text_render1, (x, y))

    def path(self, screen, position, text):
        font2 = pygame.font.SysFont("Italic", 50)
        text_render2 = font2.render(text, 1, (239, 139, 72))
        x, y, w, h = text_render2.get_rect()
        x, y = position
        pygame.draw.rect(screen, (255, 255, 51), (x + 90, y, 30, 30))
        return screen.blit(text_render2, (x, y))

class Algorithms(object):
    def __init__(self, path):
        self.path = path

    def BFS(self, x, y, level):
        frontier = collections.deque()
        frontier.append((x, y))
        explored = []
        actions = {}
        childNode = 0
        while len(frontier) > 0:
            time.sleep(0)
            x,y = frontier.popleft()
            if(x-1, y) in path and (x-1, y) not in explored:
                childNode = (x-1, y)
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if(x, y-1) in path and (x, y-1) not in explored:
                childNode = (x, y-1)
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if(x+1, y) in path and (x+1, y) not in explored:
                childNode = (x+1, y)
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y+1) in path and (x, y+1) not in explored:
                childNode = (x, y+1)
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            actions[childNode] = x, y
            if (x, y) == (goalx, goaly):
                return actions
            Maze(level)

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

pygame.display.set_caption("Search Maze Game")
screen = pygame.display.set_mode((750, 450))
clock = pygame.time.Clock()
font=pygame.freetype.SysFont(None, 34)
font.origin=True
walls = []
path=[]
exp = []
panel = Panel()

# Holds the level layout in a list of strings. 25R 27C
level = [
["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],
["W"," ","P"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"],
["W"," "," "," ","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"," "," "," ","W"," ","W"],
["W","W","W"," ","W"," "," "," "," "," "," "," ","W"," "," ","W","W"," "," "," ","W"," "," "," ","W"," ","W"],
["W"," ","W"," ","W"," "," ","W","W"," "," "," ","W"," "," "," ","W"," "," "," ","W"," "," ","W","W","W","W"],
["W"," ","W"," ","W"," "," "," ","W"," "," "," "," "," "," "," ","W"," "," "," "," "," ","W","W","W"," ","W"],
["W"," "," "," ","W","W","W","W","W"," "," ","W","W","W","W"," "," "," ","W"," "," "," "," "," ","W"," ","W"],
["W","W"," "," "," "," "," "," "," "," "," "," "," "," ","W"," "," ","W","W"," "," "," ","W"," "," "," ","W"],
["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"," "," "," ","W"," "," "," ","W"," "," "," ","W"],
["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W","W","W","W","W","W","W","W","W"],
["W"," "," ","W","W","W","W","W","W"," "," ","W"," "," "," ","W","W"," "," "," "," "," "," "," "," "," ","W"],
["W"," "," "," ","W"," "," "," "," "," ","W","W","W"," "," ","W"," "," ","W"," "," ","W"," ","W"," "," ","W"],
["W"," ","W"," ","W","W","W","W","W"," "," "," "," "," ","W","W","W","W","W"," "," ","W","W","W"," "," ","W"],
["W","W","W"," "," "," ","W","W"," "," "," "," ","W"," "," "," "," "," "," "," "," "," ","W"," "," "," ","W"],
["W"," "," "," ","W"," "," "," "," ","W","W","W","W","W","W","W","W","W"," "," ","W","W","W","W","W","W","W"],
["W"," "," ","W","W"," "," "," "," "," "," "," ","W"," "," "," ","W"," "," "," "," "," "," "," "," "," ","W"],
["W","W","W","W","W","W","W","W","W","W","W","W","W"," "," "," ","W","W","W","W","W","W","W"," "," "," ","W"],
["W"," "," "," "," "," "," "," "," "," "," "," "," "," ","W"," ","W"," "," "," "," "," "," "," ","W","W","W"],
["W"," "," "," ","W","W","W","W","W","W","W"," "," "," ","W"," "," "," "," ","W","W","W","W"," "," "," ","W"],
["W"," "," "," ","W"," "," "," "," ","W"," "," "," "," "," "," "," ","W"," "," ","W"," "," "," "," ","W","W"],
["W"," ","W","W","W"," "," ","W","W","W"," "," ","W","W"," "," ","W","W","W","W","W"," "," "," "," "," ","W"],
["W"," "," "," ","W"," "," "," "," ","W","W","W","W"," "," "," "," "," "," ","W"," "," ","W","W","W","W","W"],
["W","W","W","W","W","W","W"," "," "," "," ","W"," "," ","W","W"," "," "," ","W","W","W","W"," "," "," ","W"],
["W"," "," "," "," "," "," "," "," "," "," "," "," "," "," ","W"," ","W"," "," "," "," "," "," ","E"," ","W"],
["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"]
]

# Parse the level string above. "W" = wall, E = exit
def Maze(level):
    global player, end_rect, exp
    x = y = 1
    for i in range(len(level)):
        for j in range(len(level[0])):
            col = level[i][j]
            if col == "W": 
                Wall((x, y))
            if col == "P":
                player = Player((x, y))
            if col == "E":
                end_rect = pygame.Rect(x, y, 10, 10)
                path.append((j,i))
            if col == " ":
                path.append((j,i))
            if col == "+":
                Explored((x, y))
                # exp_rect= pygame.Rect(x, y, 16, 16)
                # pygame.draw.rect(screen, (100,100,100), exp_rect)
            x += 18
        y += 18
        x = 1
# print(path)
Maze(level)
algorithms = Algorithms(path)

running = True

print(algorithms.BFS(2,1,level))

while running:
    # clock.tick(60)
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
    screen.fill((1, 8, 52))
    for wall in walls:
        pygame.draw.rect(screen, (32, 105, 201), wall.rect)
    pygame.draw.ellipse(screen, (255, 0, 0), end_rect)
    pygame.draw.ellipse(screen, (255, 200, 0), player.rect)
    pygame.draw.rect(screen, (255, 200, 0), panel.rect)
    for x in exp:
        time.sleep(0)
        pygame.draw.rect(screen, (100,100,100), x.rect)
    b1 = panel.button(screen, (500, 10), "BFS")
    b2 = panel.button(screen, (620, 10), "DFS")
    b3 = panel.button(screen,(500, 80), "UCS")
    b4 = panel.button(screen,(620, 80), "GBFS")
    b5 = panel.button(screen, (500, 150), "A*")
    b6 = panel.explored(screen,(500,250),"Explored:")
    b7 = panel.path(screen,(500, 290),"Path:")
    
    # ticks=pygame.time.get_ticks()
    # millis=ticks%1000
    # seconds=int(ticks/1000 % 60)
    # minutes=int(ticks/60000 % 24)
    # out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
    # font.render_to(screen, (540, 350), out, pygame.Color('dodgerblue'))
    
    pygame.display.flip()
    # clock.tick(360)

# 
pygame.quit()