""" Helper module to implement maze generation using binary tree method
"""
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

    return cells

""" Function that takes partially formed cells array and performs one step on it"""
def generate_maze(cells, x, y, rows, cols):
    sides = []
    if y != cols-1:
        sides.append('R')
    if x != rows-1:
        sides.append('D')

    if sides == []:
        return cells
    side = random.choice(sides)

    if side == 'R':
        cells[x][y].right = False
        cells[x][y+1].left = False

    if side == 'D':
        cells[x][y].bottom = False
        cells[x+1][y].top = False

    return cells
    
