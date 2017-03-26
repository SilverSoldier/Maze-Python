import random
import disjoint_set as ds

class Cell:
    def __init__(self):
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True

def generate_maze(rows, cols):

    cell_list = []
    for i in xrange(rows):
        for j in xrange(cols):
            cell_list.append((i, j))

    cell_set = ds.disjoint_set(cell_list)

    cells = [[ Cell()
        for y in range(cols) ]
        for x in range(rows) ]

    # print cells[2][0]
    # print cells[1][0]

    edges = []
    for x in xrange(rows):
        for y in xrange(cols):
            edges.append((x, y, 'L'))
            edges.append((x, y, 'U'))

    while cell_set.size() != 1:

        # choose random wall
        wall = random.choice(edges)

        x = wall[0]
        y = wall[1]

        if y > 0 and wall[2] == 'L' and cell_set.find((x, y)) != cell_set.find((x, y-1)):
            cell_set.union((x, y), (x, y-1))
            edges.remove(wall)
            cells[x][y].left = False
            cells[x][y-1].right = False

        if x > 0 and wall[2] == 'U' and cell_set.find((x, y)) != cell_set.find((x-1, y)):
            cell_set.union((x, y), (x-1, y))
            edges.remove(wall)
            cells[x][y].top = False
            cells[x-1][y].bottom = False

        if y == 0 and wall[2] == 'L' or x == 0 and wall[2] == 'U':
            edges.remove(wall)

    return cells

# cells = generate_maze(3, 3)
