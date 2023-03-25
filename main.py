import urllib.request
import threading
import pygame
import time
import sys
from PyQt5 import QtWidgets, QtGui
from random import randint, choice
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
import ctypes
import inspect
import os

# 0 -> Yol
# 1 -> 1x1 Engel
# 2 -> Gezilmiş Doğru Yol -> Yeşil
# 3 -> Gezilmiş Yanlış Yol -> Kırmızı

class robot1():
    kareSayısı = 0
    enKısaYol = 0
    pygame.time.set_timer = 0
    refreshTime = pygame.time.get_ticks()
    FONT_SIZE = 25
    waitTime = 0.1
    def __init__(self):
        pygame.init()
        self.ızgara = ızgara1()
        self.cellSize = 40
        self.HEADER = 40
        self.cellPadding = 5
        self.mazeNumber = 2
        
        self.TITLE = "Problem1"
        pygame.display.set_caption(self.TITLE)
        self.CLOCK = pygame.time.Clock()
        
        
        # Colors
        self.WhiteColor = (255, 255, 255)
        self.BlackColor = (0, 0, 0)
        self.RedColor = (175, 0, 0)
        self.GreenColor = (0, 175, 0)
        self.BlueColor = (0, 0, 255)
        self.GrayColor = (45, 45, 45)
        self.YellowColor = (255, 255, 0)
        self.OrangeColor = (255, 100, 0)
        self.BrownColor = (75, 35, 15)
        self.AquaColor = (0, 255, 255)
        
        self.buttonList = []
        self.SOLVE_THREAD = None
        
    def main(self):
        self.Maze1, self.Entrance1, self.Exit1 = self.ızgara.generate_maze1()
        
        print("Entrance1: ",self.Entrance1)
        print("Exit1: ",self.Exit1)
        self.currMaze = self.Maze1
        self.currEntrance = self.Entrance1
        self.currExit = self.Exit1
        
        self.Maze2, self.Entrance2, self.Exit2 = self.ızgara.generate_maze2()
        
        print("Entrance2: ", self.Entrance2)
        print("Exit2:", self.Exit2)
        
        self.WIDTH = (self.cellSize * len(self.Maze1[0])) + (2 * self.cellPadding)
        self.HEIGHT = self.WIDTH + self.HEADER
        self.WINDOW = (self.WIDTH, self.HEIGHT)
        self.SCREEN = pygame.display.set_mode(self.WINDOW)
        self.drawMazeEnd(self.currMaze)
        
        run = True
        while run:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            #self.dispatcher_click(mouse_pos)
                            if self.buttonList[0].collidepoint(mouse_pos):
                                run = False
                                robot1.refreshTime = pygame.time.get_ticks()
                                
                            elif self.buttonList[1].collidepoint(mouse_pos):
                                self.MAZE, self.ENTRANCE, self.EXIT = self.ızgara.generate_maze2()
                                self.WIDTH = (self.cellSize * len(self.MAZE[0])) + (2 * self.cellPadding)
                                self.HEIGHT = self.WIDTH + self.HEADER
                                self.WINDOW = (self.WIDTH, self.HEIGHT)
                                self.SCREEN = pygame.display.set_mode(self.WINDOW)
                                self.drawMazeEnd(self.MAZE)
                                
        self.SCREEN.fill(self.BlackColor)
        self.SOLVE_THREAD = threading.Thread(target= self.solve_maze, args=(self.currMaze, self.currEntrance, self.currExit, self.drawMazeStart))
        self.SOLVE_THREAD.start()
        self.infoVisible = False

        run2 = True
        while True:
            self.CLOCK.tick(60)
            if not self.SOLVE_THREAD.is_alive() and not self.infoVisible and run2:
                self.drawMazeEnd(self.currMaze)
                self.infoWindow = uygulama()
                self.infoWindow.show()
                self.infoVisible = True
                with open("problem1.txt","w") as file:
                    for maze in self.currMaze:
                        for i in range(len(maze)):
                            if maze[i] == 2:
                                file.write("-")
                                
                            elif maze[i] == 3:
                                file.write("x")
                                
                            else:
                                file.write(" ")
                        file.write("\n")
                file.close()
                
                    
                for maze in self.currMaze:
                    for i in range(len(maze)):
                        if maze[i] == 2:
                            maze[i] = 0
                            
                        elif maze[i] == 3:
                            maze[i] = 4
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.SOLVE_THREAD is not None and self.SOLVE_THREAD.is_alive():
                        stop_thread(self.SOLVE_THREAD)
                        self.SOLVE_THREAD = None
                    exit(0)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        #self.dispatcher_click(mouse_pos)
                        
                        if self.buttonList[0].collidepoint(mouse_pos):
                            robot1.refreshTime = pygame.time.get_ticks()
                            robot1.kareSayısı = 0
                            robot1.enKısaYol = 0
                            robot1.waitTime = 0.1
                            self.SCREEN.fill(self.BlackColor)
                            self.SOLVE_THREAD = threading.Thread(target= self.solve_maze, args=(self.currMaze, self.currEntrance, self.currExit, self.drawMazeStart))
                            self.SOLVE_THREAD.start()
                            self.infoVisible = False
                        
                        elif self.buttonList[1].collidepoint(mouse_pos):
                            self.changeMaze()
                        
                        elif self.buttonList[2].collidepoint(mouse_pos):
                            robot1.waitTime = 0
    
                
    def draw_rect(self, x, y, len, color):
        pygame.draw.rect(self.SCREEN, color, [x, y, len, len], 0)

    
    def drawButton(self, x, y, len, height, text):
        
        FONT = pygame.font.SysFont("MS Shell Dlg2", robot1.FONT_SIZE)
        button = pygame.draw.rect(self.SCREEN, self.WhiteColor, [x, y, len, height], 1)
        self.buttonList.append(button)
        text_surface = FONT.render(text, True, self.WhiteColor)
        text_len = text.__len__() * 7
        print(text_len)
        self.SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 6))
    
    
    
    def changeMaze(self):
        robot1.refreshTime = pygame.time.get_ticks()
        self.buttonList.clear()
        robot1.waitTime = 0.1
        robot1.kareSayısı = 0
        robot1.enKısaYol = 0
        self.infoVisible = False
        pygame.time.set_timer = 0
        global Maze, Entrance, Exit, SOLVE_THREAD
        if self.SOLVE_THREAD is not None and self.SOLVE_THREAD.is_alive():
            stop_thread(self.SOLVE_THREAD)
            self.SOLVE_THREAD = None
            
        if self.mazeNumber == 1:
            self.mazeNumber = 2
            self.WIDTH = (self.cellSize * len(self.Maze1[0])) + (2 * self.cellPadding)
            self.HEIGHT = self.WIDTH + self.HEADER
            self.WINDOW = (self.WIDTH, self.HEIGHT)
            self.SCREEN = pygame.display.set_mode(self.WINDOW)
            for maze in self.currMaze:
                for i in range(len(maze)):
                    if maze[i] == 2 or maze[i] == 3:
                        maze[i] = 0
                        
            self.currMaze = self.Maze1
            self.currEntrance = self.Entrance1
            self.currExit = self.Exit1
            
        else: 
            self.mazeNumber = 1
            self.WIDTH = (self.cellSize * len(self.Maze2[0])) + (2 * self.cellPadding)
            self.HEIGHT = self.WIDTH + self.HEADER
            self.WINDOW = (self.WIDTH, self.HEIGHT)
            self.SCREEN = pygame.display.set_mode(self.WINDOW)
            for maze in self.currMaze:
                for i in range(len(maze)):
                    if maze[i] == 2 or maze[i] == 3:
                        maze[i] = 0
                        
            self.currMaze = self.Maze2
            self.currEntrance = self.Entrance2
            self.currExit = self.Exit2
            
        if len(self.currMaze[0]) < 15:
                robot1.FONT_SIZE = 20
                
        else:
                robot1.FONT_SIZE = 25
             
        self.drawMazeEnd(self.currMaze)   
        run = True
        while run:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)
                        
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            #self.dispatcher_click(mouse_pos)
                            
                            if self.buttonList[0].collidepoint(mouse_pos):
                                run = False
                                robot1.refreshTime = pygame.time.get_ticks()
                            
                            elif self.buttonList[1].collidepoint(mouse_pos):
                                self.changeMaze()
                                
        self.SCREEN.fill(self.BlackColor)          
        self.SOLVE_THREAD = threading.Thread(target = self.solve_maze, args = (self.currMaze, self.currEntrance, self.currExit, self.drawMazeStart))
        self.SOLVE_THREAD.start()
    
    
    
    def drawMazeStart(self, maze, curPos):
        self.drawButton(2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Çalıştır')
            
        self.drawButton(2 + (self.WIDTH - 4)/3, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Değiştir')
        
        self.drawButton(2 + ((self.WIDTH - 4)/3) * 2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Son')
            
        #self.drawButton(2 + ((self.WIDTH - 4)/4) * 3, 2, (self.WIDTH - 4)/4, self.HEADER - 4, 'Son')
        
        for y in range(len(maze)): 
            for x in range(len(maze)):
                cell = maze[y][x]
                print("currPos[1]: ", curPos[1])
                print("currPos[2]: ", curPos[2])
                    
                if maze[y][x] == 2:
                    color = self.GreenColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                elif maze[y][x] == 3:
                    color = self.RedColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                #1
                elif y == curPos[2] + 1 and  x == curPos[1] and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                elif y == curPos[2] + 1 and  x == curPos[1] and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] + 1 and  x == curPos[1] and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] + 1 and  x == curPos[1] and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                #2    
                elif y == curPos[2] and  x == curPos[1] + 1 and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                elif y == curPos[2] and  x == curPos[1] + 1 and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] and  x == curPos[1] + 1 and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] and  x == curPos[1] + 1 and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                #3    
                elif y == curPos[2] and  x == curPos[1] - 1 and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                elif y == curPos[2] and  x == curPos[1] - 1 and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                
                elif y == curPos[2] and  x == curPos[1] - 1 and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] and  x == curPos[1] - 1 and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                #4
                elif y == curPos[2] - 1 and  x == curPos[1] and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                elif y == curPos[2] - 1 and  x == curPos[1] and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] - 1 and  x == curPos[1] and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif y == curPos[2] - 1 and  x == curPos[1] and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                
                else:
                    color = self.GrayColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                
                if x == curPos[1] and y == curPos[2]:
                    color = self.BlueColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                    
                if x == self.currEntrance[0] and y == self.currEntrance[1]:
                    color = self.YellowColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
                
            pygame.display.flip()
  
            
                 
    def drawMazeEnd(self, maze):
        print(maze)
        #self.SCREEN.fill(self.GrayColor) 
        self.drawButton(2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Çalıştır')
        
        self.drawButton(2 + (self.WIDTH - 4)/3, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Değiştir')
        
        self.drawButton(2 + ((self.WIDTH - 4)/3) * 2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Son')
            
        #self.drawButton(2 + ((self.WIDTH - 4)/4) * 3, 2, (self.WIDTH - 4)/4, self.HEADER - 4, 'Son')
        
        size = len(maze)
        for y in range(size):
            for x in range(size):
                cell = maze[y][x]
                if maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    
                elif maze[y][x] == 5:
                    color = self.OrangeColor
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    
                elif maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    
                elif maze[y][x] == 2:
                    robot1.kareSayısı += 1
                    robot1.enKısaYol += 1
                    color = self.GreenColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize - 1, color)
                    
                elif maze[y][x] == 3:
                    robot1.kareSayısı += 1
                    color = self.RedColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize - 1, color)
                    
                else:
                    color = self.WhiteColor
                    self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize - 1, color)
                    
        pygame.display.flip()        
    
    
    def solve_maze(self, maze, pos, end, callback):
        time.sleep(robot1.waitTime)
        
        # Çıkışa ulaşmak
        if pos[0] == end[0] and pos[1] == end[1]:
            maze[pos[1]][pos[0]] = 2
            return True
        # 4 bitişik pozisyon al
        x, y = pos
        t = self.ızgara.valid(maze, x, y-1)
        r = self.ızgara.valid(maze, x+1, y)
        d = self.ızgara.valid(maze, x, y+1)
        l = self.ızgara.valid(maze, x-1, y)
    
        nextPos = self.ızgara.suggestPos((t, r, d, l))

        if nextPos:
            print("nextPos: ",nextPos)
            if nextPos[0] == 2:
                maze[pos[1]][pos[0]] = 3
            
            else:
                maze[pos[1]][pos[0]] = 2
            
            callback(maze, nextPos)
            return self.solve_maze(maze, (nextPos[1], nextPos[2]), end, callback)
        else:
            print("nextPos: ", nextPos)
            maze[pos[1]][pos[0]] = 3
            callback(maze, nextPos)
            return False
         
      
class ızgara1():
    
    def generate_maze1(self):
        url = "http://bilgisayar.kocaeli.edu.tr/prolab2/url1.txt"
        response = urllib.request.urlopen(url)
        data = response.read()
        maze = []
        
        for line in data.splitlines():
            row = [int(num) for num in line.decode('utf-8').strip()]
            maze.append(row)
            
        Entrance = []
        Exit = []
        
        for i in range (len(maze[0])):
            #sütun
            if len(Entrance) == 0:
                for j in range(len(maze)):
                #satır
                    if maze[j][i] == 0 and len(Entrance) == 0:
                        Entrance.append(i)
                        Entrance.append(j)
                        break
                    
        for i in range(len(maze[0])-1, -1, -1):
            if len(Exit) == 0:
                for j in range(len(maze)-1, -1, -1):
                    if maze[j][i] == 0 and len(Exit) == 0:
                        Exit.append(j)
                        Exit.append(i)
                        break
                    
        for Maze in maze:
            for i in range (len(Maze)):
                if Maze[i] == 2 :
                    Maze[i] = 5
                elif Maze[i] == 3:
                    Maze[i] = 6
            print(Maze)
            
        return maze, Entrance, Exit
           
           
    def generate_maze2(self):
        url = "http://bilgisayar.kocaeli.edu.tr/prolab2/url2.txt"

        response = urllib.request.urlopen(url)

        data = response.read()

        maze = []

        for line in data.splitlines():
            row = [int(num) for num in line.decode('utf-8').strip()]
            maze.append(row)
            
        Entrance = []
        Exit = []
        
        for i in range (len(maze[0])):
            #sütun
            if len(Entrance) == 0:
                for j in range(len(maze)):
                #satır
                    if maze[j][i] == 0 and len(Entrance) == 0:
                        Entrance.append(i)
                        Entrance.append(j)
                        break
                    
        for i in range(len(maze[0])-1, -1, -1):
            if len(Exit) == 0:
                for j in range(len(maze)-1, -1, -1):
                    if maze[j][i] == 0 and len(Exit) == 0:
                        Exit.append(j)
                        Exit.append(i)
                        break
        
        for Maze in maze:
            for i in range(len(Maze)):
                if Maze[i] == 2 :
                    Maze[i] = 5
                elif Maze[i] == 3:
                    Maze[i] = 6    
        
        return maze, Entrance, Exit
    
    
    
    def valid(self, maze, x, y):
        if x < 0 or y < 0:
            return False
        
        if x >= len(maze) or y >= len(maze):
            return False
        
        val = maze[y][x]
        
        if val == 1 or val == 3:
            return False
        
        return val, x, y
    
    
    
    def suggestPos(self, cells):
        
        cellArr = []
        
        for i in range (len(cells)):
                if cells[i]:
                    cellArr.append(cells[i][0])
                
                else:
                    cellArr.append(3)
        return cells[cellArr.index(min(cellArr))]



class robot2():
    kareSayısı = 0
    enKısaYol = 0
    refreshTime = pygame.time.get_ticks()
    waitTime = 0.1
    def __init__(self):
        pygame.init()
        self.cell_size = 40
        self.HEADER = 40
        self.cell_padding = 5
        self.WIDTH = (self.cell_size * menu.sutun) + (2 * self.cell_padding)
        self.HEIGHT = self.WIDTH + self.HEADER
        self.WINDOW = (self.WIDTH, self.HEIGHT)
        self.TITLE = "Problem2"
        self.SCREEN = pygame.display.set_mode(self.WINDOW)
        pygame.display.set_caption(self.TITLE)
        self.CLOCK = pygame.time.Clock()
        self.startTime = pygame.time.get_ticks()
        self.buttonList = []
        #Colors
        self.WhiteColor = (255, 255, 255)
        self.BlackColor = (0, 0, 0)
        self.RedColor = (175, 0, 0)
        self.GreenColor = (0, 175, 0)
        self.BlueColor = (0, 0, 255)
        self.GrayColor = (45, 45, 45)
        self.BUTTONS = []
        self.SOLVE_THREAD = None
        self.ızgara = ızgara2(self.WIDTH, self.HEIGHT)
        
    def main(self):
        
        self.MAZE, self.ENTRANCE, self.EXIT = self.ızgara.generate_maze(menu.satır, menu.sutun)        
        self.draw_mazeEnd(self.MAZE)
        
        run = True
        while run:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)
                        
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            #self.dispatcher_click(mouse_pos)
                            if self.buttonList[0].collidepoint(mouse_pos):
                                run = False
                                robot2.refreshTime = pygame.time.get_ticks()
                            
                            elif self.buttonList[1].collidepoint(mouse_pos):
                                self.MAZE, self.ENTRANCE, self.EXIT = self.ızgara.generate_maze(menu.satır, menu.sutun)
                                self.draw_mazeEnd(self.MAZE)
        self.SCREEN.fill(self.BlackColor)
        self.SOLVE_THREAD = threading.Thread(target= self.solve_maze, args=(self.MAZE, self.ENTRANCE, self.EXIT, self.draw_mazeStart))
        self.SOLVE_THREAD.start()
        self.infoVisible = False
        
        run2 = True
        while True:
            self.CLOCK.tick(60)
            if not self.SOLVE_THREAD.is_alive() and not self.infoVisible and run2:
                self.draw_mazeEnd(self.MAZE)
                self.infoWindow = uygulama()
                self.infoWindow.show()
                self.infoVisible = True
                
                with open("problem2.txt","w") as file:
                    for maze in self.MAZE:
                        for i in range(len(maze)):
                            if maze[i] == 2:
                                file.write("-")
                                
                            elif maze[i] == 3:
                                file.write("*")
                                
                            else:
                                file.write(" ")
                                
                        file.write("\n")
                file.close()
                
                for maze in self.MAZE:
                    for i in range(len(maze)):
                        if maze[i] == 2:
                            maze[i] = 0
                            
                        elif maze[i] == 3:
                            maze[i] = 4
                
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.SOLVE_THREAD is not None and self.SOLVE_THREAD.is_alive():
                        stop_thread(self.SOLVE_THREAD)
                        self.SOLVE_THREAD = None
                        
                    exit(0)        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    #self.dispatcher_click(mouse_pos)
                    
                    if self.buttonList[0].collidepoint(mouse_pos):
                            robot2.refreshTime = pygame.time.get_ticks()
                            robot2.kareSayısı = 0
                            robot2.enKısaYol = 0
                            robot2.waitTime = 0.1
                            self.SOLVE_THREAD = threading.Thread(target= self.solve_maze, args=(self.MAZE, self.ENTRANCE, self.EXIT, self.draw_mazeStart))
                            self.SOLVE_THREAD.start()
                            self.infoVisible = False
                        
                    elif self.buttonList[1].collidepoint(mouse_pos):
                        self.refresh()
                        
                        
                    elif self.buttonList[2].collidepoint(mouse_pos):
                        robot2.waitTime = 0
            
        
    def draw_rect(self, x, y, len, color):
        pygame.draw.rect(self.SCREEN, color, [x, y, len, len], 0)


    def draw_button(self, x, y, len, height, text):
        self.FONT_SIZE = 25
        FONT = pygame.font.SysFont("MS Shell Dlg2", self.FONT_SIZE)
        button = pygame.draw.rect(self.SCREEN, self.WhiteColor, [x, y, len, height], 1)
        self.buttonList.append(button)
        text_surface = FONT.render(text, True, self.WhiteColor)
        text_len = text.__len__() * 7
        self.SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


    def refresh(self):
        self.SCREEN.fill(self.BlackColor)
        robot2.refreshTime = pygame.time.get_ticks()
        pygame.time.set_timer = 0
        robot2.waitTime = 0.1
        robot2.kareSayısı = 0
        robot2.enKısaYol = 0
        self.infoVisible = False
        pygame.time.set_timer = 0
        if self.SOLVE_THREAD is not None and self.SOLVE_THREAD.is_alive():
            stop_thread(self.SOLVE_THREAD)
            self.SOLVE_THREAD = None
        self.MAZE, self.ENTRANCE, self.EXIT = self.ızgara.generate_maze(menu.satır, menu.sutun)
        
        self.draw_mazeEnd(self.MAZE)
        run = True
        while run:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit(0)
                        
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            #self.dispatcher_click(mouse_pos)
                            
                            if self.buttonList[0].collidepoint(mouse_pos):
                                run = False
                                robot2.refreshTime = pygame.time.get_ticks()
                                
                            elif self.buttonList[1].collidepoint(mouse_pos):
                                self.refresh()
                                        
        self.SOLVE_THREAD = threading.Thread(target= self.solve_maze, args=(self.MAZE, self.ENTRANCE, self.EXIT, self.draw_mazeStart))
        self.SOLVE_THREAD.start()


    def draw_mazeStart(self, maze, cur_pos):
        #self.SCREEN.fill(self.GrayColor)
        self.draw_button(2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Çalıştır')
        self.draw_button(2 + (self.WIDTH - 4)/3, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Değiştir')
        self.draw_button(2 + ((self.WIDTH - 4)/3) * 2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Son')
        #self.draw_button(2 + ((self.WIDTH - 4)/4) * 3, 2, (self.WIDTH - 4)/4, self.HEADER - 4, 'Son')


        size = len(maze)
        for y in range(size):
            for x in range(size):
                cell = maze[y][x]
                print("curr_pos[1]: ",cur_pos[1])
                print("curr_pos[2]: ",cur_pos[2])
                if cell == 2:
                    color = self.GreenColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                elif cell == 3:
                    color = self.RedColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                
                #1
                elif y == cur_pos[2] + 1 and  x == cur_pos[1] and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                elif y == cur_pos[2] + 1 and  x == cur_pos[1] and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                elif y == cur_pos[2] + 1 and  x == cur_pos[1] and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                    
                elif y == cur_pos[2] + 1 and  x == cur_pos[1] and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                #2    
                elif y == cur_pos[2] and  x == cur_pos[1] + 1 and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                elif y == cur_pos[2] and  x == cur_pos[1] + 1 and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                elif y == cur_pos[2] and  x == cur_pos[1] + 1 and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                    
                elif y == cur_pos[2] and  x == cur_pos[1] + 1 and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                #3    
                elif y == cur_pos[2] and  x == cur_pos[1] - 1 and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                elif y == cur_pos[2] and  x == cur_pos[1] - 1 and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                elif y == cur_pos[2] and  x == cur_pos[1] - 1 and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                    
                elif y == cur_pos[2] and  x == cur_pos[1] - 1 and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                #4
                elif y == cur_pos[2] - 1 and  x == cur_pos[1] and maze[y][x] == 0:
                    color = self.WhiteColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                elif y == cur_pos[2] - 1 and  x == cur_pos[1] and maze[y][x] == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                elif y == cur_pos[2] - 1 and  x == cur_pos[1] and maze[y][x] == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                    
                elif y == cur_pos[2] - 1 and  x == cur_pos[1] and maze[y][x] == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                    
                else:
                    color = self.GrayColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                if x == cur_pos[1] and y == cur_pos[2]:
                    color = self.BlueColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
        pygame.display.flip()

    def draw_mazeEnd(self, maze):
        #self.SCREEN.fill(self.GrayColor)
        self.draw_button(2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Çalıştır')
        
        self.draw_button(2 + (self.WIDTH - 4)/3, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Değiştir')
        
        self.draw_button(2 + ((self.WIDTH - 4)/3) * 2, 2, (self.WIDTH - 4)/3, self.HEADER - 4, 'Son')
            
        #self.draw_button(2 + ((self.WIDTH - 4)/4) * 3, 2, (self.WIDTH - 4)/4, self.HEADER - 4, 'Son')

        size = len(maze)
        self.cell_padding = (self.WIDTH - (self.cell_size * size)) / 2
        for y in range(size):
            for x in range(size):
                cell = maze[y][x]
                
                if cell == 1:
                    image = pygame.image.load("Engel1.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                
                elif cell == 5:
                    image = pygame.image.load("Engel2.jpg")
                    image = pygame.transform.scale(image, (self.cell_size - (self.cell_padding*2), self.cell_size - (self.cell_padding*2)))
                    self.SCREEN.blit(image, ((self.cell_padding*2) + x * self.cell_size, self.HEADER + (self.cell_padding*2) + y * self.cell_size))
                    pygame.display.flip()
                    
                elif cell == 6:
                    image = pygame.image.load("Engel3.jpg")
                    image = pygame.transform.scale(image, (self.cellSize - (self.cellPadding*2), self.cellSize - (self.cellPadding*2)))
                    self.SCREEN.blit(image, ((self.cellPadding*2) + x * self.cellSize, self.HEADER + (self.cellPadding*2) + y * self.cellSize))
                    pygame.display.flip()
                    
                elif cell == 2:
                    robot2.kareSayısı += 1
                    robot2.enKısaYol += 1
                    color = self.GreenColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                    
                elif cell == 3:
                    robot2.kareSayısı += 1
                    color = self.RedColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
                else:
                    color = self.WhiteColor
                    self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
        
        pygame.display.flip()
    
    
    def valid(self, maze, x, y):
        if x < 0 or y < 0:
            return False
        
        if x >= len(maze) or y >= len(maze):
            return False
        
        val = maze[y][x]
        
        if val == 1 or val == 3:
            return False
        
        return val, x, y


    def neighbors(self, maze, pos):
        x, y = pos
        t, r, d, l = self.valid(maze, x, y - 1), self.valid(maze, x + 1, y), self.valid(maze, x, y + 1), self.valid(maze, x - 1, y)
        
        return t, r, d, l


    def suggest_pos(self, cells):
        arr = []
        for cell in cells:
            print("cell: ",cell)
            if cell:
                arr.append(cell[0])
                
            else:
                arr.append(3)
                
        return cells[arr.index(min(arr))]


    def solve_maze(self, maze, pos, end, callback):
        time.sleep(robot2.waitTime)
        
        # Çıkışa Ulaşmak
        if pos[0] == end[0] and pos[1] == end[1]:
            maze[pos[1]][pos[0]] = 2
            return True
        
        # 4 bitişik pozisyon al
        t, r, d, l = self.neighbors(maze, pos)
        
        print("t: ",t)
        print("r: ",r)
        print("d: ",d)
        print("l: ",l)
        
        next_pos = self.suggest_pos((t, r, d, l))
        
        if next_pos:
            print("nextPos: ",next_pos)
            if next_pos[0] == 2:
                maze[pos[1]][pos[0]] = 3
                
            else:
                maze[pos[1]][pos[0]] = 2
            callback(maze, next_pos)
            
            return self.solve_maze(maze, (next_pos[1], next_pos[2]), end, callback)
        
        else:
            print("next_pos: ",next_pos)
            maze[pos[1]][pos[0]] = 3
            callback(maze, next_pos)
            
            return False


def check_neighbors(maze, x, y, width, height, checklist):
    directions = []
    if x > 0:
        if not maze.visited(2 * (x - 1) + 1, 2 * y + 1):
            directions.append("LEFT")
            
    if y > 0:
        if not maze.visited(2 * x + 1, 2 * (y - 1) + 1):
            directions.append("UP")
            
    if x < width - 1:
        if not maze.visited(2 * (x + 1) + 1, 2 * y + 1):
            directions.append("RIGHT")
            
    if y < height - 1:
        if not maze.visited(2 * x + 1, 2 * (y + 1) + 1):
            directions.append("DOWN")
            
    print("Directions: ",directions)        
    if len(directions) != 0:
        direction = choice(directions)
        print(direction)
        
        if direction == "LEFT":
            maze.set_maze(2 * (x - 1) + 1, 2 * y + 1, 0)
            maze.set_maze(2 * x, 2 * y + 1, 0)
            checklist.append((x - 1, y))
            
        elif direction == "UP":
            maze.set_maze(2 * x + 1, 2 * (y - 1) + 1, 0)
            maze.set_maze(2 * x + 1, 2 * y, 0)
            checklist.append((x, y - 1))
            
        elif direction == "RIGHT":
            maze.set_maze(2 * (x + 1) + 1, 2 * y + 1, 0)
            maze.set_maze(2 * x + 2, 2 * y + 1, 0)
            checklist.append((x + 1, y))
            
        elif direction == "DOWN":
            maze.set_maze(2 * x + 1, 2 * (y + 1) + 1, 0)
            maze.set_maze(2 * x + 1, 2 * y + 2, 0)
            checklist.append((x, y + 1))
            
        return True
    
    return False



class ızgara2():
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = []
        for i in range (height):
            self.maze.append([])
            for j in range(width):
                self.maze[i].append(0)
        print("Maze: ",self.maze)
        
    
    def reset_maze(self, cellType):
        for y in range(self.height):
            for x in range(self.width):
                self.set_maze(x, y, cellType)


    def set_maze(self, x, y, value):
        if value == 0:
            self.maze[y][x] = 0
            
        else:
            self.maze[y][x] = 1


    def visited(self, x, y):
        return self.maze[y][x] != 1
        
    
    
    def do_random_prime(self, maze):
        maze.reset_maze(1)
        width = (maze.width - 1) // 2
        height = (maze.height - 1) // 2
        start_x, start_y = (randint(0, width - 1), randint(0, height - 1))
        print("Start X: ",start_x)
        print("Start Y: ",start_y)
        maze.set_maze(2 * start_x + 1, 2 * start_y + 1, 1)
        checklist = [(start_x, start_y)]
        print("Checklist: ",checklist)
        
        while len(checklist):
            entry = choice(checklist)
            print(entry)
            
            if not check_neighbors(maze, entry[0], entry[1], width, height, checklist):
                checklist.remove(entry)


    def girişÇıkışAyarla(self, maze):
        başlangıç = []
        for i in range(maze.height):
            if maze.maze[i][1] == 0:
                maze.set_maze(0, i, 0)
                başlangıç = [0, i]
                print("Giriş: ",başlangıç)
                break
        çıkış = []
        
        for i in range(maze.height - 1, 0, -1):
            if maze.maze[i][maze.width - 2] == 0:
                maze.set_maze(maze.width - 1, i, 0)
                çıkış = [maze.width - 1, i]
                break
            
        return başlangıç, çıkış


    def generate_maze(self, height, width):
        # labirenti başlat
        maze = ızgara2(width, height)
        print("maze: ",maze)
        
        # Harita oluştur
        self.do_random_prime(maze)
        
        # Başlangıç ve bitişi seçin
        başlangıç, çıkış = self.girişÇıkışAyarla(maze)
        
        # Haritaya Dön
        return maze.maze, başlangıç, çıkış




      
class Engel():
    def __init__(self, type):
        self.BlackColor = (0, 0, 0)
        self.OrangeColor = (255, 100, 0)
        self.AquaColor = (0, 255, 255)
        
        if self.type == 1:
            self.Color = self.BlackColor

        elif self.type == 2:
            self.Color = self.OrangeColor
            
        elif self.type == 3:
            self.Color = self.AquaColor
      
      
        
class uygulama(QMainWindow):
    def __init__(self):
        super(uygulama, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle("Bitti")
        myFont = QtGui.QFont('MS Shell Dlg2',14)
        myFont.setBold(True)
        myFont.setPointSize(12)
        
        #Girişte
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Labirent Çözüldü")
        self.label1.setFixedSize(200, 50)
        self.label1.move(125, 30)
        self.label1.setFont(myFont)
        
        myFont.setPointSize(8)
        self.label2 = QtWidgets.QLabel(self)
        
        self.label2.setFixedSize(150 ,40)
        self.label2.move(125, 80)
        self.label2.setFont(myFont)
        
        self.label3 = QtWidgets.QLabel(self)
        self.label3.setFixedSize(160 ,40)
        self.label3.move(80, 120)
        self.label3.setFont(myFont)
        
        self.label4 = QtWidgets.QLabel(self)
        self.label4.setFixedSize(125, 40)
        self.label4.move(125, 160)
        self.label4.setFont(myFont)
        
        if robot1.kareSayısı == 0:
            self.label3.setText("Gezilen Kare Sayısı: " +  str(robot2.kareSayısı))
            self.label2.setText("Toplam Süre: " + str(round(((pygame.time.get_ticks() - robot2.refreshTime)/1000.0),2)) + " sn")
            self.label4.setText("En Kısa Yol: " + str(robot2.enKısaYol))
            robot2.refreshTime = pygame.time.get_ticks()
        else:
            self.label3.setText("Gezilen Kare Sayısı: " +  str(robot1.kareSayısı))
            self.label2.setText("Toplam Süre: " + str(round(((pygame.time.get_ticks() - robot1.refreshTime)/1000.0),2)) + " sn")
            self.label4.setText("En Kısa Yol: "+ str(robot1.enKısaYol))
            robot1.refreshTime = pygame.time.get_ticks()
        
        
        myFont.setPointSize(10)
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Kapat")
        self.button1.setFont(myFont)
        self.button1.clicked.connect(self.button_clicked_button1)
        self.button1.setFixedSize(100, 40)
        self.button1.move(150,220)
        
    def button_clicked_button1(self):
        self.setVisible(False)


class menu(QMainWindow, robot1):
    def __init__(self):
        super(menu,self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(600, 400)
        self.move(600, 300)
        #self.setStyleSheet("background-color: darkGray;")
        self.setWindowTitle("Prolab2.1")
        myFont = QtGui.QFont('MS Shell Dlg2', 14)
        myFont.setBold(True)
        
        #Girişte Yazacak Olanlar
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("ProLab2")
        self.label1.setFixedSize(140, 50)
        self.label1.move(240, 50)
        self.label1.setFont(myFont)
        
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Gezgin Robot Projesi")
        self.label2.setFixedSize(250, 40)
        self.label2.move(160, 110)
        self.label2.setFont(myFont)
        
        myFont.setPointSize(8)
        self.bp1 = QtWidgets.QPushButton(self)
        self.bp1.setText("Problem1")
        self.bp1.setFont(myFont)
        self.bp1.clicked.connect(self.button_clicked_bg1)
        self.bp1.setFixedSize(100,50)
        self.bp1.move(240,170)
        
        self.bp2 = QtWidgets.QPushButton(self)
        self.bp2.setText("Problem2")
        self.bp2.setFont(myFont)
        self.bp2.clicked.connect(self.button_clicked_bp2)
        self.bp2.setFixedSize(100,50)
        self.bp2.move(240,230)
        
        #Problem 2 ye basılırsa açılacak olanlar
        self.textbox1 = QLineEdit(self)
        self.textbox1.move(270, 210)
        self.textbox1.resize(50, 30)
        self.textbox1.setVisible(False)
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(270, 250)
        self.textbox2.resize(50,30)
        self.textbox2.setVisible(False)
        
        self.label3 = QtWidgets.QLabel(self)
        myFont.setPointSize(10)
        self.label3.setText("Labirent Boyutlarını Girin")
        self.label3.setVisible(False)
        self.label3.setFixedSize(221,41)
        self.label3.move(210,160)
        self.label3.setFont(myFont)
        
        self.label4 = QtWidgets.QLabel(self)
        self.label4.setText("Satır")
        self.label4.setVisible(False)
        self.label4.setFixedSize(55, 16)
        self.label4.move(200, 220)
        self.label4.setFont(myFont)
        
        self.label5 = QtWidgets.QLabel(self)
        self.label5.setText("Sütun")
        self.label5.setVisible(False)
        self.label5.setFixedSize(55, 16)
        self.label5.move(200, 260)
        self.label5.setFont(myFont)
        
        self.bg2 = QtWidgets.QPushButton(self)
        self.bg2.setText("Labirenti Oluştur")
        self.bg2.setFont(myFont)
        self.bg2.clicked.connect(self.button_clicked_bg2)
        self.bg2.setFixedSize(155, 40)
        self.bg2.move(230, 300)
        self.bg2.setVisible(False)
    
    
    def button_clicked_bp2(self):
        self.bp1.setVisible(False)
        self.bp2.setVisible(False)
        self.textbox1.setVisible(True)
        self.textbox2.setVisible(True)
        self.label3.setVisible(True)
        self.label4.setVisible(True)
        self.label5.setVisible(True)
        self.bg2.setVisible(True)
    
        
    def button_clicked_bg1(self):
        self.setVisible(False)
        maze = robot1()
        maze.main()
        
    def button_clicked_bg2(self):
        menu.satır = int(self.textbox1.text())
        menu.sutun = int(self.textbox2.text())
        maze = robot2()
        self.close()
        maze.main()

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)




app = QApplication(sys.argv)
win = menu()
win.show()
sys.exit(app.exec_())
   
