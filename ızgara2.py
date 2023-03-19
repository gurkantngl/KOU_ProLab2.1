import urllib.request
import threading
import pygame
import time
from utils import stop_thread
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit

# 0 -> Yol
# 1 -> 1x1 Engel
# 2 -> Gezilmiş Doğru Yol -> Yeşil
# 3 -> Gezilmiş Yanlış Yol -> Kırmızı

class problem1():
    kareSayısı = 0
    refreshTime = pygame.time.get_ticks()
    def init(self):
        pygame.init()
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
        
        self.BUTTONS = []
        self.SOLVE_THREAD = None
        
    def main(self):
        self.Maze1, self.Entrance1, self.Exit1 = self.generate_maze1()
        
        print("Entrance1: ",self.Entrance1)
        print("Exit1: ",self.Exit1)
        self.currMaze = self.Maze1
        self.currEntrance = self.Entrance1
        self.currExit = self.Exit1
        
        self.Maze2, self.Entrance2, self.Exit2 = self.generate_maze2()
        for maze in self.Maze2:
            for i in range(len(maze)):
                if maze[i] == 2 or maze[i] == 3:
                    maze[i] = 1
            print(maze)
        print("Entrance2: ", self.Entrance2)
        print("Exit2:", self.Exit2)
        
        self.WIDTH = (self.cellSize * len(self.Maze1[0])) + (2 * self.cellPadding)
        self.HEIGHT = self.WIDTH + self.HEADER
        self.WINDOW = (self.WIDTH, self.HEIGHT)
        self.SCREEN = pygame.display.set_mode(self.WINDOW)
        
        self.SOLVE_THREAD = threading.Thread(target= self.solve_maze, args=(self.currMaze, self.currEntrance, self.currExit, self.drawMazeStart))
        self.SOLVE_THREAD.start()
        self.infoVisible = False
     
        while True:
            self.CLOCK.tick(60)
            if not self.SOLVE_THREAD.is_alive() and not self.infoVisible:
                self.drawMazeEnd(self.currMaze)
                self.infoWindow = uygulama()
                self.infoWindow.show()
                self.infoVisible = True
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
                        print((pygame.time.get_ticks() - problem1.refreshTime)/1000.0)
                    exit(0)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in self.BUTTONS:
                        x, y, length, height = button['x'], button['y'], button['length'], button['height']
                        pos_x, pos_y = pos
                        if x <= pos_x <= x + length and y <= pos_y <= y + height:
                            if self.mazeNumber == 1:
                                self.mazeNumber == 2
                            else:
                                self.mazeNumber == 1
                            button['click']()
                
    def draw_rect(self, x, y, len, color):
        pygame.draw.rect(self.SCREEN, color, [x, y, len, len], 0)           
    
    def drawButton(self, x, y, len, height, text):
        self.FONT_SIZE = 25
        FONT = pygame.font.SysFont("MS Shell Dlg2", self.FONT_SIZE)
        pygame.draw.rect(self.SCREEN, self.WhiteColor, [x, y, len, height], 1)
        text_surface = FONT.render(text, True, self.WhiteColor)
        text_len = text.__len__() * self.FONT_SIZE
        self.SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))
    
    
    
    def changeMaze(self):
        problem1.kareSayısı = 0
        self.infoVisible = False
        problem1.refreshTime = pygame.time.get_ticks()
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
        self.SOLVE_THREAD = threading.Thread(target = self.solve_maze, args = (self.currMaze, self.currEntrance, self.currExit, self.drawMazeStart))
        self.SOLVE_THREAD.start()
        
    
    
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
                if Maze[i] == 2 or Maze[i] == 3:
                    Maze[i] = 1
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
            for i in range (len(Maze)):
                if Maze[i] == 2 or Maze[i] == 3:
                    Maze[i] = 1
            print(Maze)
        return maze, Entrance, Exit
    
    
    
    def drawMazeStart(self, maze, curPos):
        self.SCREEN.fill(self.GrayColor)
        self.drawButton(2, 2, self.WIDTH - 4, self.HEADER - 4, 'Değiştir')
        if len(self.BUTTONS) == 0:
            self.BUTTONS.append({
                'x' : 2,
                'y' : 2,
                'length' : self.WIDTH - 4,
                'height' : self.HEADER  - 4,
                'click' : self.changeMaze
            })
        
        for y in range(len(maze)):
            for x in range(len(maze)):
                
                cell = maze[y][x]
                print("currPos[1]: ", curPos[1])
                print("currPos[2]: ", curPos[2])
                
                """
                if x == curPos[1] + 1:
                    cellNeighbor = maze[y][x+1]
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    self.draw_rect(cellPadding + (x+1) * cellSize, self.HEADER + cellPadding + y * cellSize, cellSize - 1, color)
                    #pygame.display.flip()
                
                elif x == curPos[1] - 1 and y == curPos[2]:
                    cellNeighbor = maze[y][x-1]
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                        
                    self.draw_rect(cellPadding + (x-1) * cellSize, self.HEADER + cellPadding + y * cellSize, cellSize-1, color)
                    #pygame.display.flip()
                
                elif y == curPos[2] + 1 and x == curPos[1]:
                    cellNeighbor = maze[y+1][x]
                    
                    if cellNeighBor == 1:
                        color self.BlackColor
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    self.draw_rect(cellPadding + x * cellSize, self.HEADER + cellPadding + (y+1) * cellSize, cellSize - 1, color)
                    #pygame.display.flip()
                    
                elif y == curPos[2] - 1 and x == curPos[1]:
                    cellNeighbor = maze[y-1][x]
                    
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    
                    self.draw_rect(cellPadding + x * cellSize, self.HEADER + cellPadding + (y-1) * cellSize, cellSize - 1, color)
                    #pygame.display.flip()
                    """
                
                
                if cell == 2:
                    color = self.GreenColor
                    
                elif cell == 3:
                    color = self.RedColor
                
                else:
                    color = self.GrayColor
                    
                if x == curPos[1] and y == curPos[2]:
                    color = self.BlueColor
                    
                if x == self.currEntrance[0] and y == self.currEntrance[1]:
                    color = self.YellowColor
                    
                    
                self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize -1, color)
            pygame.display.flip()
  
            
                 
    def drawMazeEnd(self, maze):
        print(maze)
        self.SCREEN.fill(self.GrayColor) 
        self.drawButton(2, 2, self.WIDTH - 4, self.HEADER - 4, 'Değiştir')
        if len(self.BUTTONS) == 0:
            self.BUTTONS.append({
                'x' : 2,
                'y' : 2,
                'length' : self.WIDTH - 4,
                'height' : self.HEADER - 4,
                'click' : self.changeMaze
            })
        
        size = len(maze)
        for y in range(size):
            for x in range(size):
                cell = maze[y][x]
                if cell == 1:
                    color = self.BlackColor
                    
                elif cell == 2:
                    problem1.kareSayısı += 1
                    color = self.GreenColor
                    
                elif cell == 3:
                    problem1.kareSayısı += 1
                    color = self.RedColor
                else:
                    color = self.WhiteColor
                self.draw_rect(self.cellPadding + x * self.cellSize, self.HEADER + self.cellPadding + y * self.cellSize, self.cellSize - 1, color)
        pygame.display.flip()        
    
    
    def solve_maze(self, maze, pos, end, callback):
        wait_time = 0.1
        time.sleep(wait_time)
        
        # Çıkışa ulaşmak
        if pos[0] == end[0] and pos[1] == end[1]:
            maze[pos[1]][pos[0]] = 2
            return True
        # 4 bitişik pozisyon al
        x, y = pos
        t = self.valid(maze, x, y-1)
        r = self.valid(maze, x+1, y)
        d = self.valid(maze, x, y+1)
        l = self.valid(maze, x-1, y)
    
        nextPos = self.suggestPos((t, r, d, l))

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
        
class uygulama(QMainWindow):
    def __init__(self):
        super(uygulama, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(400, 300)
        self.setWindowTitle("Bitti")
        myFont = QtGui.QFont('MS Shell Dlg2',14)
        myFont.setBold(True)
        myFont.setPointSize(10)
        
        #Girişte
        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("Labirent Çözüldü")
        self.label1.setFixedSize(150, 50)
        self.label1.move(125, 50)
        self.label1.setFont(myFont)
        
        myFont.setPointSize(8)
        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Toplam Süre: " + str(round(((pygame.time.get_ticks() - problem1.refreshTime)/1000.0),2)) + " sn")
        self.label2.setFixedSize(150 ,40)
        self.label2.move(125, 120)
        self.label2.setFont(myFont)
        
        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("Gezilen Kare Sayısı: " +  str(problem1.kareSayısı))
        self.label3.setFixedSize(160 ,40)
        self.label3.move(80, 160)
        self.label3.setFont(myFont)
        
        myFont.setPointSize(10)
        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Kapat")
        self.button1.setFont(myFont)
        self.button1.clicked.connect(self.button_clicked_button1)
        self.button1.setFixedSize(100, 40)
        self.button1.move(150,220)
        
    def button_clicked_button1(self):
        self.setVisible(False)


class menu(QMainWindow, problem1):
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
        self.bp1.setFixedSize(100,30)
        self.bp1.move(240,170)
        
        self.bp2 = QtWidgets.QPushButton(self)
        self.bp2.setText("Problem2")
        self.bp2.setFont(myFont)
        self.bp2.clicked.connect(self.button_clicked_bp2)
        self.bp2.setFixedSize(100,30)
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
        maze = problem1()
        maze.init()
        maze.main()
    def button_clicked_bg2(self):
        """grid.satır = int(self.textbox1.text())
        grid.sutun = int(self.textbox2.text())
        maze = problem2()
        self.setVisible(False)
        maze.init()
        maze.main()   """
        pass
    
def window():
    app = QApplication(sys.argv)
    win = menu()
    win.show()
    sys.exit(app.exec_())
window()   
