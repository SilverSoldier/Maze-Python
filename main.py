import libtcodpy as libtcod
import kruskal
import prim

SCREEN_WIDTH = 110
SCREEN_HEIGHT = 60

TILE_SIZE = 4

MAP_ROWS = 25
MAP_WIDTH = TILE_SIZE * MAP_ROWS

MAP_COLS = 12
MAP_HEIGHT = TILE_SIZE * MAP_COLS

LIMIT_FPS = 20

FOV_ALGO = 0 # default field of view algorithm provided by libtcod
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 40

class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        if not map[self.x + dx][self.y + dy].wall:
            self.x += dx
            self.y += dy

    def draw(self, con):
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def erase(self, con):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Tile:
    def __init__(self, is_wall):
        self.wall = is_wall
        self.explored = False

def make_map(cells):
    global map

    map = [[ Tile(False)
        for y in xrange(MAP_HEIGHT) ]
        for x in xrange(MAP_WIDTH) ]

    for x in range(MAP_ROWS):
        for y in range(MAP_COLS):
            map[x * TILE_SIZE][y * TILE_SIZE].wall = True
            map[x * TILE_SIZE][(y+1) * TILE_SIZE - 1].wall = True
            map[(x+1) * TILE_SIZE - 1][y * TILE_SIZE].wall = True
            map[(x+1) * TILE_SIZE - 1][(y+1) * TILE_SIZE - 1].wall = True

            for k in range(1, TILE_SIZE - 1):

                map[x * TILE_SIZE][y * TILE_SIZE + k].wall = cells[x][y].top
                map[x * TILE_SIZE + k][y * TILE_SIZE].wall = cells[x][y].left
                map[x * TILE_SIZE + k][(y+1) * TILE_SIZE - 1].wall =  cells[x][y].right
                map[(x+1) * TILE_SIZE - 1][y * TILE_SIZE + k].wall = cells[x][y].bottom

def render_all(player, con, fov_map, check_explored):
    libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            compute_fov = False
            wall = map[x][y].wall
            if not visible and (map[x][y].explored or not check_explored):
                if wall:
                    libtcod.console_put_char_ex(con, x, y, '#', libtcod.grey, libtcod.black)

                else:
                    libtcod.console_put_char_ex(con, x, y, '.', libtcod.grey, libtcod.black)

            if visible:
                map[x][y].explored = True
                if wall:
                    libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.black)

                else:
                    libtcod.console_put_char_ex(con, x, y, '.', libtcod.white, libtcod.black)

    libtcod.console_put_char_ex(con, MAP_WIDTH-2, MAP_HEIGHT-2, 'X', libtcod.green, libtcod.white)


    player.draw(con)

def render_solution(cells, con):
    visited = [[ False
        for y in xrange(MAP_COLS)]
        for x in xrange(MAP_ROWS)]

    # print cells[11][0].bottom

    path = [(0, 0)]
    dfs(cells, 0, 0, visited, path)

    # print path

    for y in range(MAP_COLS):
        for x in range(MAP_ROWS):
            if (x, y) in path:
                for i in xrange(1, TILE_SIZE - 1):
                    for j in xrange(1, TILE_SIZE - 1):
                        libtcod.console_put_char_ex(con, x * TILE_SIZE + i, y * TILE_SIZE + j, 'X', libtcod.green, libtcod.black)

def dfs(cells, x, y, visited, path):
    # if x < 0 or y < 0 or x >= MAP_ROWS or y >= MAP_COLS:
    #     return False

    # print x
    # print y
    if visited[x][y]:
        return False

    path.append((x, y))
    if x == MAP_ROWS - 1 and y == MAP_COLS - 1:
        return True

    visited[x][y] = True
    if not cells[x][y].right:
        # path.append((x, y+1))
        if dfs(cells, x, y+1, visited, path):
            return True
        # path.remove((x, y+1))

    if not cells[x][y].top:
        # path.append((x-1, y))
        if dfs(cells, x-1, y, visited, path):
            return True
        # path.remove((x-1, y))

    if not cells[x][y].left:
        # path.append((x, y-1))
        if dfs(cells, x, y-1, visited, path):
            return True
        # path.remove((x, y-1))

    if not cells[x][y].bottom:
        # path.append((x+1, y))
        if dfs(cells, x+1, y, visited, path):
            return True
        # path.remove((x+1, y))

    path.remove((x, y))
    return False

def keyboard_input(player):

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ESCAPE:
        return True

    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)
        compute_fov = True

    if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
        compute_fov = True

    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
        compute_fov = True

    if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)
        compute_fov = True

    return False

def main():

    player = Object(1, 1, '@', libtcod.red)

    libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    print "Which algorithm would you prefer for generating maze?"
    print "Enter 1 for randomized Kruskal's, the mazes have a lot of dead ends, but have a regular pattern."
    print "Enter 2 for randomized Prim's, the mazes have a lot of dead ends."
    choice = int(raw_input())

    print "Would you like to see the maze being formed?"

    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'maze game', False)
    con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)

    libtcod.sys_set_fps(LIMIT_FPS)

    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    global compute_fov
    compute_fov = False

    for y in xrange(MAP_HEIGHT):
        for x in xrange(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not True, True)

    if choice == 1:
        (edges, cell_set, cell_list, cells) = kruskal.init_variables(MAP_ROWS, MAP_COLS)

        while cell_set.size() != 1:
            cells = kruskal.generate_maze(edges, cell_set, cell_list, cells)

        make_map(cells)
        render_all(player, con, fov_map, True)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

    # (wall_set, cells_finished, cells) = prim.init_variables(MAP_ROWS, MAP_COLS)
            # cells = prim.generate_maze(wall_set, cells_finished, cells)
    # cells = prim.generate_maze(MAP_ROWS, MAP_COLS)


    while not libtcod.console_is_window_closed():

        # player.draw(con)
        render_all(player, con, fov_map, True)

        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        player.erase(con)

        quit = keyboard_input(player)

        if player.x == MAP_WIDTH-2 and player.y == MAP_HEIGHT-2:
            break

        if quit:
            render_all(player, con, fov_map, False)
            render_solution(cells, con)
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)
            break

if __name__ == '__main__':
    main()
