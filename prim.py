import random

class Cell:
    def __init__(self):
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True

def init_variables(rows, cols):
    cells = [[ Cell()
        for y in range(cols) ]
        for x in range(rows) ]

    wall_set = [(0, 0, 2), (0, 0, 3)]
    cells_finished = [(0, 0)]

    return (wall_set, cells_finished, cells)

def generate_maze(wall_set, cells_finished, cells):
    # left: 0, top: 1, right: 2, bottom: 3

    while len(cells_finished) != rows*cols:
    # while len(cells_finished) != 2:
        wall = random.choice(wall_set)

        x = wall[0]
        y = wall[1]

        if y != 0 and wall[2] == 0 and (x, y-1) not in cells_finished:
            wall_set.remove(wall)
            cells[x][y].left = False
            cells[x][y-1].right = False
            cells_finished.append((x, y-1))
            for i in xrange(4):
                wall_set.append((x, y-1, i))

        elif x != 0 and wall[2] == 1 and (x-1, y) not in cells_finished:
            wall_set.remove(wall)
            cells[x][y].top = False
            cells[x-1][y].bottom = False
            cells_finished.append((x-1, y))
            for i in xrange(4):
                wall_set.append((x-1, y, i))

        elif y != cols - 1 and wall[2] == 2 and (x, y+1) not in cells_finished:
            wall_set.remove(wall)
            cells[x][y].right = False
            cells[x][y+1].left = False
            cells_finished.append((x, y+1))
            for i in xrange(4):
                wall_set.append((x, y+1, i))

        elif x != rows - 1 and wall[2] == 3 and (x+1, y) not in cells_finished:
            wall_set.remove(wall)
            cells[x][y].bottom = False
            cells[x+1][y].top = False
            cells_finished.append((x+1, y))
            for i in xrange(4):
                wall_set.append((x+1, y, i))

        elif x == 0 and wall[2] == 1 or x == rows - 1 and wall[2] == 2:
            wall_set.remove(wall)

        elif y == 0 and wall[2] == 0 or y == cols - 1 and wall[2] == 3:
            wall_set.remove(wall)

    # print cells_finished
    return cells
