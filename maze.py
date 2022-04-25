import timeit
import pygame
import time
import collections
import queue

goalx = 24
goaly = 23
fx=2
fy=1

class Player(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Explored(object):
    def __init__(self, pos):
        exp.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        
class Final(object):
    def __init__(self,pos):
        finalpath.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class Panel(object):
    def __init__(self):
        self.rect = pygame.Rect(487, 1, 260, 450)

    def explored(self, screen, position, text):
        font1 = pygame.font.SysFont("Italic", 50)
        text_render1 = font1.render(text, 1, (70, 70, 70))
        x, y, w, h = text_render1.get_rect()
        x, y = position
        pygame.draw.rect(screen, (100, 100, 100), (x + 160, y, 30, 30))
        return screen.blit(text_render1, (x, y))

    def path(self, screen, position, text):
        font2 = pygame.font.SysFont("Italic", 50)
        text_render2 = font2.render(text, 1, (70, 70, 70))
        x, y, w, h = text_render2.get_rect()
        x, y = position
        pygame.draw.rect(screen, (239,139, 72), (x + 90, y, 30, 30))
        return screen.blit(text_render2, (x, y))

class Buttons(object):
    def __init__(self, screen, position, text):
        font = pygame.font.SysFont("Italic", 50)
        self.text_render = font.render(text, 1, (239, 139, 72))
        x, y, self.w, self.h = self.text_render.get_rect()
        self.screen = screen
        self.x, self.y = position
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.clicked = False
        
    def button(self):
        if self.clicked == False:
            pygame.draw.line(self.screen, (150, 150, 150), (self.x, self.y), (self.x + self.w, self.y), 5)
            pygame.draw.line(self.screen, (150, 150, 150), (self.x, self.y - 2), (self.x, self.y + self.h), 5)
            pygame.draw.line(self.screen, (50, 50, 50), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 5)
            pygame.draw.line(self.screen, (50, 50, 50), (self.x + self.w, self.y + self.h), [self.x + self.w, self.y], 5)
            pygame.draw.rect(self.screen, (100, 100, 100), (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.line(self.screen, (100, 100, 100), (self.x, self.y), (self.x + self.w, self.y), 5)
            pygame.draw.line(self.screen, (100, 100, 100), (self.x, self.y - 2), (self.x, self.y + self.h), 5)
            pygame.draw.line(self.screen, (150, 150, 150), (self.x, self.y + self.h), (self.x + self.w, self.y + self.h), 5)
            pygame.draw.line(self.screen, (150, 150, 150), (self.x + self.w, self.y + self.h), [self.x + self.w, self.y], 5)
            pygame.draw.rect(self.screen, (50, 50, 50), (self.x, self.y, self.w, self.h))
        return self.screen.blit(self.text_render, (self.x, self.y))

class Algorithms(object):
    def __init__(self, path):
        self.path = path

    def BFS(self, x, y, level):
        frontier = collections.deque()
        frontier.append((x, y))
        explored = []
        actions = {}
        childNode = (x, y)
        actions[childNode] = x, y
        while len(frontier) > 0:
            x, y = frontier.popleft()
            if(x - 1, y) in path and (x - 1, y) not in explored:
                childNode = (x - 1, y)
                actions[childNode] = x,y
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if(x, y - 1) in path and (x, y - 1) not in explored:
                childNode = (x, y - 1)
                actions[childNode] = x,y
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if(x + 1, y) in path and (x + 1, y) not in explored:
                childNode = (x + 1, y)
                actions[childNode] = x,y
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y + 1) in path and (x, y + 1) not in explored:
                childNode = (x, y + 1)
                actions[childNode] = x,y
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            Maze(level)
            if (x, y) == (goalx, goaly):
                return actions
            
    def DFS(self, x, y, level):
        frontier = collections.deque()
        frontier.appendleft((x, y))
        explored = []
        actions = {}
        childNode = (x, y)
        actions[childNode] = x, y
        while len(frontier) > 0:
            x, y = frontier.popleft()
            if (x - 1, y) in path and (x - 1, y) not in explored:
                childNode = (x - 1, y)
                actions[childNode] = x, y
                frontier.appendleft(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y - 1) in path and (x, y - 1) not in explored:
                childNode = (x, y - 1)
                actions[childNode] = x, y
                frontier.appendleft(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if (x + 1, y) in path and (x + 1, y) not in explored:
                childNode = (x + 1, y)
                actions[childNode] = x, y
                frontier.append(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y + 1) in path and (x, y + 1) not in explored:
                childNode = (x, y + 1)
                actions[childNode] = x, y
                frontier.appendleft(childNode)
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y) == (goalx, goaly):
                return actions
            Maze(level)
            
    def UCS(self, x, y, level):
        frontier = queue.PriorityQueue()
        frontier.put((realcost[y][x], (x, y)))
        explored = []
        actions = {}
        childNode = (x, y)
        actions[childNode] = x, y
        while not frontier.empty():
            cost, (x, y) = frontier.get()
            if(x - 1, y) in path and (x - 1, y) not in explored:
                childNode = (x - 1, y)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y][x - 1], (x - 1, y)))
                explored.append(childNode)
                level[y][x] = "+"
            if(x, y - 1) in path and (x, y - 1) not in explored:
                childNode = (x, y - 1)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y - 1][x], (x, y - 1)))
                explored.append(childNode)
                level[y][x] = "+"
            if(x + 1, y) in path and (x + 1, y) not in explored:
                childNode = (x + 1, y)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y][x + 1], (x + 1, y)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y + 1) in path and (x, y + 1) not in explored:
                childNode = (x, y + 1)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y + 1][x], (x, y + 1)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y) == (goalx, goaly):
                return actions
            Maze(level)
            
    def GBFS(self, x, y, level):
        frontier = queue.PriorityQueue()
        frontier.put((heuristiccost[y][x], (x, y)))
        explored = []
        actions = {}
        childNode = (x, y)
        actions[childNode] = x, y
        while not frontier.empty():
            cost, (x, y) = frontier.get()
            if (x - 1, y) in path and (x - 1, y) not in explored:
                childNode = (x - 1, y)
                actions[childNode] = x, y
                frontier.put((heuristiccost[y][x - 1], (x - 1, y)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y - 1) in path and (x, y - 1) not in explored:
                childNode = (x, y - 1)
                actions[childNode] = x, y
                frontier.put((heuristiccost[y - 1][x], (x, y - 1)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x + 1, y) in path and (x + 1, y) not in explored:
                childNode = (x + 1, y)
                actions[childNode] = x, y
                frontier.put((heuristiccost[y][x + 1], (x + 1, y)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y + 1) in path and (x, y + 1) not in explored:
                childNode = (x, y + 1)
                actions[childNode] = x, y
                frontier.put((heuristiccost[y + 1][x], (x, y + 1)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y) == (goalx, goaly):
                return actions
            Maze(level)
        
    def Astar(self, x, y, level):
        frontier = queue.PriorityQueue()
        frontier.put((realcost[y][x], heuristiccost[y][x], (x, y)))
        explored = []
        actions = {}
        childNode = (x, y)
        actions[childNode] = x, y
        while not frontier.empty():
            tcost, hcost, (x, y) = frontier.get()
            if(x - 1, y) in path and (x - 1, y) not in explored:
                childNode = (x - 1, y)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y][x - 1] + heuristiccost[y][x - 1], heuristiccost[y][x - 1], (x - 1, y)))
                explored.append(childNode)
                level[y][x] = "+"
            if(x, y - 1) in path and (x, y - 1) not in explored:
                childNode = (x, y - 1)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y - 1][x] + heuristiccost[y - 1][x], heuristiccost[y - 1][x], (x, y - 1)))
                explored.append(childNode)
                level[y][x] = "+"
            if(x + 1, y) in path and (x + 1, y) not in explored:
                childNode = (x + 1, y)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y][x + 1] + heuristiccost[y][x + 1], heuristiccost[y][x + 1], (x + 1, y)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y + 1) in path and (x, y + 1) not in explored:
                childNode = (x, y + 1)
                actions[childNode] = x, y
                frontier.put((realcost[y][x] + realcost[y + 1][x] + heuristiccost[y + 1][x], heuristiccost[y + 1][x], (x, y + 1)))
                explored.append(childNode)
                level[y][x] = "+"
            if (x, y) == (goalx, goaly):
                return actions
            Maze(level)
        
    def pathFind(self, x, y, actions):
        while (x, y) != (fx, fy):
            x, y = actions[x, y]
            level[y][x] = "-"
            Maze(level)
        
pygame.init()
icon = pygame.image.load('icon.jpg')
pygame.display.set_icon(icon)
pygame.display.set_caption("Solving a Maze Using AI Algorithms")
screen = pygame.display.set_mode((750, 450))
clock = pygame.time.Clock()
none = True
drawOnce = False
walls = []
path = []
exp = []
finalpath = []
panel = Panel()
buttons = [
    Buttons(screen, (500, 10), "BFS"),
    Buttons(screen, (620, 10), "DFS"),
    Buttons(screen, (500, 80), "UCS"),
    Buttons(screen, (620, 80), "GBFS"),
    Buttons(screen, (500, 150), "A*")
]

def resetLevel():
    global level, exp, finalpath
    exp = []
    finalpath = []
    level = [["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"],
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
            ["W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W","W"]]

resetLevel()

realcost = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 74, 1, 156, 29, 90, 174, 2, 77, 105, 98, 135, 174, 72, 179, 190, 149, 113, 107, 170, 184, 85, 40, 42, 5, 149, -1],
            [-1, 128, 25, 170, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 102, 192, 79, -1, 117, -1],
            [-1, -1, -1, 141, -1, 162, 79, 176, 118, 96, 35, 114, -1, 189, 120, -1, -1, 36, 146, 89, -1, 101, 69, 1, -1, 100, -1], 
            [-1, 111, -1, 89, -1, 118, 148, -1, -1, 173, 183, 59, -1, 154, 19, 100, -1, 31, 152, 147, -1, 54, 101, -1, -1, -1, -1], 
            [-1, 163, -1, 43, -1, 28, 35, 19, -1, 104, 112, 58, 11, 173, 84, 180, -1, 154, 143, 133, 179, 141, -1, -1, -1, 84, -1], 
            [-1, 172, 156, 30, -1, -1, -1, -1, -1, 50, 12, -1, -1, -1, -1, 79, 170, 37, -1, 7, 53, 125, 137, 91, -1, 23, -1], 
            [-1, -1, 38, 172, 186, 192, 8, 126, 166, 88, 119, 50, 189, 113, -1, 19, 117, -1, -1, 145, 137, 132, -1, 114, 51, 200, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 156, 44, 79, -1, 116, 31, 129, -1, 124, 192, 190, -1], 
            [-1, 6, 175, 3, 200, 180, 164, 25, 116, 18, 112, 125, 29, 81, 11, 70, 181, 22, -1, -1, -1, -1, -1, -1, -1, -1, -1], 
            [-1, 58, 139, -1, -1, -1, -1, -1, -1, 98, 74, -1, 40, 129, 22, -1, -1, 135, 170, 156, 140, 129, 121, 21, 120, 126, -1],
            [-1, 40, 7, 51, -1, 65, 156, 176, 33, 171, -1, -1, -1, 169, 82, -1, 158, 3, -1, 8, 33, -1, 65, -1, 195, 27, -1], 
            [-1, 96, -1, 139, -1, -1, -1, -1, -1, 72, 105, 167, 75, 42, -1, -1, -1, -1, -1, 80, 189, -1, -1, -1, 195, 173, -1], 
            [-1, -1, -1, 48, 36, 27, -1, -1, 140, 119, 61, 107, -1, 64, 52, 136, 197, 163, 46, 139, 24, 28, -1, 75, 98, 182, -1], 
            [-1, 133, 109, 14, -1, 143, 143, 139, 181, -1, -1, -1, -1, -1, -1, -1, -1, -1, 118, 62, -1, -1, -1, -1, -1, -1, -1], 
            [-1, 41, 21, -1, -1, 34, 16, 92, 163, 132, 98, 179, -1, 71, 168, 92, -1, 39, 35, 121, 72, 160, 135, 43, 26, 18, -1], 
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 87, 41, 19, -1, -1, -1, -1, -1, -1, -1, 94, 29, 12, -1], 
            [-1, 116, 100, 105, 62, 51, 76, 33, 39, 32, 113, 103, 42, 90, -1, 27, -1, 52, 181, 200, 97, 142, 161, 120, -1, -1, -1], 
            [-1, 182, 52, 99, -1, -1, -1, -1, -1, -1, -1, 90, 194, 64, -1, 190, 5, 71, 156, -1, -1, -1, -1, 198, 194, 181, -1], 
            [-1, 141, 11, 46, -1, 23, 90, 3, 167, -1, 187, 163, 54, 182, 137, 33, 194, -1, 69, 191, -1, 101, 138, 113, 65, -1, -1], 
            [-1, 31, -1, -1, -1, 92, 162, -1, -1, -1, 177, 96, -1, -1, 33, 197, -1, -1, -1, -1, -1, 151, 1, 192, 71, 2, -1], 
            [-1, 57, 183, 198, -1, 92, 9, 174, 183, -1, -1, -1, -1, 35, 99, 56, 136, 111, 9, -1, 26, 50, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, 121, 152, 9, 16, -1, 152, 55, -1, -1, 93, 55, 17, -1, -1, -1, -1, 19, 171, 168, -1],
            [-1, 117, 54, 139, 135, 157, 95, 143, 27, 139, 42, 107, 54, 139, 78, -1, 134, -1, 175, 92, 74, 59, 185, 182, 0, 43, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

heuristiccost = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                 [-1, 137, 163, 159, 78, 141, 131, 45, 182, 21, 130, 27, 88, 189, 81, 165, 4, 147, 76, 37, 6, 124, 147, 137, 183, 49, -1],
                 [-1, 148, 134, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 173, 82, 73, -1, 41, -1],
                 [-1, -1, -1, 20, -1, 5, 137, 124, 24, 8, 41, 9, -1, 31, 166, -1, -1, 68, 194, 61, -1, 18, 39, 184, -1, 29, -1],
                 [-1, 181, -1, 118, -1, 3, 25, -1, -1, 16, 29, 186, -1, 18, 75, 168, -1, 116, 152, 48, -1, 88, 167, -1, -1, -1, -1],
                 [-1, 114, -1, 36, -1, 17, 81, 37, -1, 143, 3, 93, 68, 90, 163, 28, -1, 190, 161, 108, 156, 51, -1, -1, -1, 5, -1],
                 [-1, 112, 73, 56, -1, -1, -1, -1, -1, 97, 189, -1, -1, -1, -1, 86, 128, 143, -1, 83, 54, 10, 121, 148, -1, 7, -1],
                 [-1, -1, 170, 5, 29, 74, 170, 24, 101, 93, 176, 50, 165, 168, -1, 54, 6, -1, -1, 149, 36, 121, -1, 11, 132, 121, -1],
                 [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 16, 106, -1, 87, 158, 78, -1, 178, 195, 7, -1],
                 [-1, 8, 35, 185, 5, 106, 139, 116, 6, 181, 159, 160, 165, 68, 135, 120, 22, 54, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                 [-1, 108, 112, -1, -1, -1, -1, -1, -1, 95, 31, -1, 182, 50, 69, -1, -1, 189, 175, 135, 66, 140, 98, 39, 46, 19, -1],
                 [-1, 116, 58, 2, -1, 102, 199, 68, 13, 62, -1, -1, -1, 9, 15, -1, 71, 59, -1, 49, 58, -1, 17, -1, 143, 193, -1],
                 [-1, 200, -1, 70, -1, -1, -1, -1, -1, 155, 138, 20, 192, 57, -1, -1, -1, -1, -1, 46, 146, -1, -1, -1, 139, 104, -1],
                 [-1, -1, -1, 45, 105, 182, -1, -1, 91, 85, 160, 87, -1, 10, 17, 112, 104, 195, 39, 150, 69, 178, -1, 58, 48, 128, -1],
                 [-1, 150, 181, 189, -1, 170, 86, 92, 160, -1, -1, -1, -1, -1, -1, -1, -1, -1, 66, 30, -1, -1, -1, -1, -1, -1, -1],
                 [-1, 178, 31, -1, -1, 60, 153, 97, 188, 149, 27, 56, -1, 166, 123, 184, -1, 145, 91, 136, 100, 186, 111, 15, 172, 128, -1],
                 [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 86, 15, 56, -1, -1, -1, -1, -1, -1, -1, 136, 82, 37, -1],
                 [-1, 168, 92, 123, 52, 174, 84, 74, 65, 4, 162, 159, 43, 85, -1, 79, -1, 106, 191, 89, 85, 15, 53, 82, -1, -1, -1],
                 [-1, 17, 104, 81, -1, -1, -1, -1, -1, -1, -1, 11, 141, 136, -1, 100, 135, 104, 197, -1, -1, -1, -1, 134, 112, 3, -1],
                 [-1, 143, 107, 59, -1, 58, 179, 115, 153, -1, 101, 2, 56, 184, 176, 58, 199, -1, 130, 132, -1, 125, 131, 82, 57, -1, -1],
                 [-1, 71, -1, -1, -1, 46, 165, -1, -1, -1, 139, 86, -1, -1, 166, 156, -1, -1, -1, -1, -1, 108, 126, 21, 84, 5, -1],
                 [-1, 107, 5, 196, -1, 62, 67, 118, 103, -1, -1, -1, -1, 71, 129, 169, 78, 182, 161, -1, 175, 172, -1, -1, -1, -1, -1],
                 [-1, -1, -1, -1, -1, -1, -1, 104, 168, 47, 198, -1, 138, 180, -1, -1, 64, 8, 17, -1, -1, -1, -1, 33, 169, 132, -1],
                 [-1, 71, 53, 184, 109, 154, 35, 21, 122, 97, 198, 95, 121, 163, 47, -1, 47, -1, 176, 114, 151, 38, 108, 40, 0, 159, -1],
                 [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

def Maze(level):
    global player, end_rect
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
                path.append((j, i))
            if col == " ":
                path.append((j, i))
            if col == "-":
                Final((x,y))
            if col == "+":
                Explored((x, y))
            x += 18
        y += 18
        x = 1
        
Maze(level)
def draw():
    pygame.draw.ellipse(screen, (255, 0, 0), end_rect)
    pygame.draw.ellipse(screen, (255, 0, 0), player.rect)

def buttonsreset():
    buttons[0].button()
    buttons[1].button()
    buttons[2].button()
    buttons[3].button()
    buttons[4].button()

algorithms = Algorithms(path)
running = True
while running:
    screen.fill((1, 8, 52))       
    for wall in walls:
        pygame.draw.rect(screen, (32, 105, 201), wall.rect)
    draw()
    pygame.draw.rect(screen, (255, 200, 0), panel.rect)
    buttonsreset()
    b6 = panel.explored(screen, (500, 250), "Explored:")
    b7 = panel.path(screen, (500, 290), "Path:")
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
        running = False
    if e.type == pygame.MOUSEBUTTONDOWN:
        resetLevel()
        
        Maze(level)
        none=True
        if buttons[0].rect.collidepoint(pygame.mouse.get_pos()):
            none=False
            for b in buttons:
                b.clicked = False
            buttons[0].clicked = True
            starttime = timeit.default_timer()
            algorithms.pathFind(goalx, goaly, (algorithms.BFS(2, 1, level)))
            exetime="The time taken to solve maze using BFS: "+str(timeit.default_timer() - starttime)
            print(exetime)
        if buttons[1].rect.collidepoint(pygame.mouse.get_pos()):
            none=False
            for b in buttons:
                b.clicked = False
            buttons[1].clicked = True
            starttime = timeit.default_timer()
            act=algorithms.DFS(2, 1, level)
            algorithms.pathFind(goalx, goaly, (act))
            print("The time taken to explore using DFS: ", timeit.default_timer() - starttime)
        if buttons[2].rect.collidepoint(pygame.mouse.get_pos()):
            none=False
            for b in buttons:
                b.clicked = False
            buttons[2].clicked = True
            starttime = timeit.default_timer()
            act=algorithms.UCS(2, 1, level)
            algorithms.pathFind(goalx, goaly, (act))
            print("The time taken to explore using UCS: ", timeit.default_timer() - starttime)
        if buttons[3].rect.collidepoint(pygame.mouse.get_pos()):
            none=False
            for b in buttons:
                b.clicked = False
            buttons[3].clicked = True
            starttime = timeit.default_timer()
            act=algorithms.GBFS(2, 1, level)
            algorithms.pathFind(goalx, goaly, (act))
            print("The time taken to explore using GBFS: ", timeit.default_timer() - starttime)
        if buttons[4].rect.collidepoint(pygame.mouse.get_pos()):
            none=False
            for b in buttons:
                b.clicked = False
            buttons[4].clicked = True
            starttime = timeit.default_timer()
            act=algorithms.Astar(2, 1, level)
            algorithms.pathFind(goalx, goaly, (act))
            print("The time taken to explore using A*: ", timeit.default_timer() - starttime)
        if none:
            for b in buttons:
                b.clicked = False
        buttonsreset()
        for x in exp:
            if drawOnce == False:
                draw() 
            pygame.draw.rect(screen, (100, 100, 100), x.rect)
            time.sleep(0)
            pygame.display.update()
            drawOnce == True
    for x in exp:
            pygame.draw.rect(screen, (100, 100, 100), x.rect)
    for p in finalpath:
        pygame.draw.rect(screen, (239,139, 72), p.rect)
    draw()
    pygame.display.flip()
pygame.quit()