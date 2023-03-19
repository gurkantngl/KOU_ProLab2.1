# Bu sınıfta problem1 için ızgara tasarımı verilen url adresindeki text dosyasına göre oluşturulurken
# problem2 için ızgara kullanıcıdan alınacak boyut bilgisine göre oluşturulmalıdır.
# coding = utf-8
import threading
import pygame
from maze_generator import generate_maze
from maze_solver import solve_maze
from utils import stop_thread
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
import uygulama
from random import randint, choice

class Engel():
    def __init__(self, wallType):
        self.wallType = wallType
        if self.wallType == 1:
            self.image = 'engel1.jpg'
        
        elif self.wallType == 2:
            self.image = 'engel2.jpg'
        
        elif self.wallType == 3:
            self.image = 'engel3.jpg'


class problem2():
    kareSayısı = 0
    refreshTime = pygame.time.get_ticks()
    def init(self):
        pygame.init()
        self.cell_size = 40
        self.HEADER = 40
        self.cell_padding = 5
        self.WIDTH = (self.cell_size * grid.sutun) + (2 * self.cell_padding)
        self.HEIGHT = self.WIDTH + self.HEADER
        self.WINDOW = (self.WIDTH, self.HEIGHT)
        self.refreshTime = pygame.time.get_ticks()
        self.TITLE = "Problem2"
        self.SCREEN = pygame.display.set_mode(self.WINDOW)
        pygame.display.set_caption(self.TITLE)
        self.CLOCK = pygame.time.Clock()
        self.startTime = pygame.time.get_ticks()

        #Colors
        self.WhiteColor = (255, 255, 255)
        self.BlackColor = (0, 0, 0)
        self.RedColor = (175, 0, 0)
        self.GreenColor = (0, 175, 0)
        self.BlueColor = (0, 0, 255)
        self.GrayColor = (45, 45, 45)
        self.BUTTONS = []
        self.SOLVE_THREAD = None

    def main(self):
        
        self.MAZE, self.ENTRANCE, self.EXIT = generate_maze(grid.satır, grid.sutun)
        print("MAZE: ", self.MAZE)
        print("ENTRANCE: ", self.ENTRANCE)
        print("Exit: ", self.EXIT)
        print("type(MAZE): ", type(self.MAZE))
        print("type(ENTRANCE): ", type(self.ENTRANCE))
        print("type(EXIT): ",type(self.EXIT))
        self.SOLVE_THREAD = threading.Thread(target=solve_maze, args=(self.MAZE, self.ENTRANCE, self.EXIT, self.draw_mazeStart))
        self.SOLVE_THREAD.start()
        self.infoWindow = uygulama.uygulama()
        self.infoVisible = False
        while True:
            self.CLOCK.tick(60)
            if not self.SOLVE_THREAD.is_alive() and not self.infoVisible:
                self.infoWindow.show()
                self.infoVisible = True
                self.draw_mazeEnd(self.MAZE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.SOLVE_THREAD is not None and self.SOLVE_THREAD.is_alive():
                        stop_thread(self.SOLVE_THREAD)
                        self.SOLVE_THREAD = None
                        print((pygame.time.get_ticks() - self.refreshTime)/1000.0)
                    exit(0)        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.dispatcher_click(mouse_pos)
            
        
    def draw_rect(self, x, y, len, color):
        pygame.draw.rect(self.SCREEN, color, [x, y, len, len], 0)


    def draw_button(self, x, y, len, height, text):
        self.FONT_SIZE = 25
        FONT = pygame.font.SysFont("MS Shell Dlg2", self.FONT_SIZE)
        pygame.draw.rect(self.SCREEN, self.WhiteColor, [x, y, len, height], 1)
        text_surface = FONT.render(text, True, self.WhiteColor)
        text_len = text.__len__() * self.FONT_SIZE
        self.SCREEN.blit(text_surface, (x + (len - text_len) / 2, y + 2))


    def refresh(self):
        self.infoVisible = False
        self.refreshTime = pygame.time.get_ticks()
        pygame.time.set_timer=0
        if self.SOLVE_THREAD is not None and self.SOLVE_THREAD.is_alive():
            stop_thread(self.SOLVE_THREAD)
            self.SOLVE_THREAD = None
        size = 20
        self.MAZE, self.ENTRANCE, self.EXIT = generate_maze(grid.satır, grid.sutun)
        self.SOLVE_THREAD = threading.Thread(target=solve_maze, args=(self.MAZE, self.ENTRANCE, self.EXIT, self.draw_mazeStart))
        self.SOLVE_THREAD.start()


    def draw_mazeStart(self, maze, cur_pos):
        self.SCREEN.fill(self.GrayColor)
        self.draw_button(2, 2, self.WIDTH - 4, self.HEADER - 4, 'Değiştir')
        if len(self.BUTTONS) == 0:
            self.BUTTONS.append({
                'x': 2,
                'y': 2,
                'length': self.WIDTH - 4,
                'height': self.HEADER - 4,
                'click': self.refresh
            })

        size = len(maze)
        for y in range(size):
            for x in range(size):
                cell = maze[y][x]
                print("curr_pos[1]: ",cur_pos[1])
                print("curr_pos[2]: ",cur_pos[2])
                """
                if x == cur_pos[1] + 1:
                    cellNeighbor = maze[y][x+1]
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    self.draw_rect(cell_padding + (x+1) * cell_size, self.HEADER + cell_padding + y * cell_size, cell_size - 1, color)
                    #pygame.display.flip()
                        
                elif x == cur_pos[1] - 1 and y == cur_pos[2]:
                    cellNeighbor = maze[y][x-1]
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    self.draw_rect(cell_padding + (x-1) * cell_size, self.HEADER + cell_padding + y * cell_size, cell_size - 1, color)
                    #pygame.display.flip()
                    
                elif y == cur_pos[2] + 1 and x == cur_pos[1]:
                    cellNeighbor = maze[y+1][x]
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    self.draw_rect(cell_padding + x * cell_size, self.HEADER + cell_padding + (y+1) * cell_size, cell_size - 1, color)
                    #pygame.display.flip()
                    
                elif y == cur_pos[2] - 1 and x == cur_pos[1]:
                    cellNeighbor = maze[y-1][x]
                    if cellNeighbor == 1:
                        color = self.BlackColor
                    
                    elif cellNeighbor == 0:
                        color = self.WhiteColor
                    self.draw_rect(cell_padding + x * cell_size, self.HEADER + cell_padding + (y-1) * cell_size, cell_size - 1, color)
                    #pygame.display.flip()
                    """
                if cell == 2:
                    color = self.GreenColor
                
                elif cell == 3:
                    color = self.RedColor
                    
                else:
                    color = self.GrayColor
                    
                if x == cur_pos[1] and y == cur_pos[2]:
                    color = self.BlueColor
                self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
        pygame.display.flip()

    def draw_mazeEnd(self, maze):
        self.SCREEN.fill(self.GrayColor)
        self.draw_button(2, 2, self.WIDTH - 4, self.HEADER - 4, 'Değiştir')
        if len(self.BUTTONS) == 0:
            self.BUTTONS.append({
                'x': 2,
                'y': 2,
                'length': self.WIDTH - 4,
                'height': self.HEADER - 4,
                'click': self.refresh
            })

        size = len(maze)
        self.cell_padding = (self.WIDTH - (self.cell_size * size)) / 2
        for y in range(size):
            for x in range(size):
                cell = maze[y][x]
                
                if cell==1:
                    color = self.BlackColor
                elif cell == 2:
                    color = self.GreenColor
                elif cell == 3:
                    color = self.RedColor
                else:
                    color = self.WhiteColor
                self.draw_rect(self.cell_padding + x * self.cell_size, self.HEADER + self.cell_padding + y * self.cell_size, self.cell_size - 1, color)
        pygame.display.flip()
    

    def dispatcher_click(self, pos):
        for button in self.BUTTONS:
            x, y, length, height = button['x'], button['y'], button['length'], button['height']
            pos_x, pos_y = pos
            if x <= pos_x <= x + length and y <= pos_y <= y + height:
                button['click']()

class Maze:
    
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

def do_random_prime(maze):
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

def girişÇıkışAyarla(maze):
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


def generate_maze(height, width):
        # labirenti başlat
        maze = Maze(width, height)
        print("maze: ",maze)
        
        # Harita oluştur
        do_random_prime(maze)
        
        # Başlangıç ve bitişi seçin
        başlangıç, çıkış = girişÇıkışAyarla(maze)
        
        # Haritaya Dön
        return maze.maze, başlangıç, çıkış
        
                    
class grid(QMainWindow, problem2):
    def __init__(self):
        super(grid,self).__init__()
        self.initUI()
    
    def initUI(self):
        self.setFixedSize(600, 400)
        self.move(600, 300)
        #self.setStyleSheet("background-color: darkGray;")
        self.setWindowTitle("Prolab2.1")
        myFont = QtGui.QFont('MS Shell Dlg2',14)
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
        self.bp1.clicked.connect(self.button_clicked_bp1)
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
    
    def button_clicked_bp1(self):
        pass
    
    def button_clicked_bp2(self):
        self.bp1.setVisible(False)
        self.bp2.setVisible(False)
        self.textbox1.setVisible(True)
        self.textbox2.setVisible(True)
        self.label3.setVisible(True)
        self.label4.setVisible(True)
        self.label5.setVisible(True)
        self.bg2.setVisible(True)
        
    def button_clicked_bg2(self):
        grid.satır = int(self.textbox1.text())
        grid.sutun = int(self.textbox2.text())
        maze = problem2()
        self.setVisible(False)
        maze.init()
        maze.main()
        
    
        
def window():
    app = QApplication(sys.argv)
    win = grid()
    win.show()
    sys.exit(app.exec_())
window()