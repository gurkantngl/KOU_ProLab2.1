# coding=utf-8
from random import randint, choice


# Hücre Tipi
# 0 - Yol，1 - Duvar
class CellType:
    ROAD = 0
    WALL = 1



# Labirent Haritası
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
