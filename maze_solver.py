import time


# Hücre Tipi
# 0 - Yol，
# 1 - Duvar，
# 2-Gidilen Yol，
# 3-Çıkmaz Sokak

# Duvar Yönü
# LEFT
# UP
# RIGHT
# DOWN

def valid(maze, x, y):
    if x < 0 or y < 0:
        return False
    if x >= len(maze) or y >= len(maze):
        return False
    val = maze[y][x]
    if val == 1 or val == 3:
        return False
    return val, x, y


def neighbors(maze, pos):
    x, y = pos
    t, r, d, l = valid(maze, x, y - 1), valid(maze, x + 1, y), valid(maze, x, y + 1), valid(maze, x - 1, y)
    return t, r, d, l


def suggest_pos(cells):
    arr = []
    for cell in cells:
        print("cell: ",cell)
        if cell:
            arr.append(cell[0])
        else:
            arr.append(3)
    return cells[arr.index(min(arr))]


def solve_maze(maze, pos, end, callback):
    time.sleep(0.1)
    # Çıkışa Ulaşmak
    if pos[0] == end[0] and pos[1] == end[1]:
        maze[pos[1]][pos[0]] = 2
        return True
    # 4 bitişik pozisyon al
    t, r, d, l = neighbors(maze, pos)
    
    print("t: ",t)
    print("r: ",r)
    print("d: ",d)
    print("l: ",l)
    
    next_pos = suggest_pos((t, r, d, l))
    
    if next_pos:
        print("nextPos: ",next_pos)
        if next_pos[0] == 2:
            maze[pos[1]][pos[0]] = 3
        else:
            maze[pos[1]][pos[0]] = 2
        callback(maze, next_pos)
        return solve_maze(maze, (next_pos[1], next_pos[2]), end, callback)
    else:
        print("next_pos: ",next_pos)
        maze[pos[1]][pos[0]] = 3
        callback(maze, next_pos)
        return False
