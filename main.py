import libtcodpy as libtcod
import kruskal

SCREEN_WIDTH = 110
SCREEN_HEIGHT = 60

TILE_SIZE = 4

MAP_ROWS = 25
MAP_WIDTH = TILE_SIZE * MAP_ROWS

MAP_COLS = 12
MAP_HEIGHT = TILE_SIZE * MAP_COLS

LIMIT_FPS = 20

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

def render_all(player, con):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].wall
            if wall:
                libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.black)

            else:
                libtcod.console_put_char_ex(con, x, y, '.', libtcod.white, libtcod.black)

    player.draw(con)

def render_solution(cells, con):
    visited = [[ False
        for y in xrange(MAP_COLS)]
        for x in xrange(MAP_ROWS)]

    # print cells[11][0].bottom

    path = []
    dfs(cells, 0, 0, visited, path)

    # print path

    for y in range(MAP_COLS):
        for x in range(MAP_ROWS):
            if (x, y) in path:
                for i in xrange(1, TILE_SIZE - 1):
                    for j in xrange(1, TILE_SIZE - 1):
                        libtcod.console_put_char_ex(con, x * TILE_SIZE + i, y * TILE_SIZE + j, 'X', libtcod.green, libtcod.black)

def dfs(cells, x, y, visited, path):
    if x < 0 or y < 0 or x >= MAP_ROWS or y >= MAP_COLS:
        return False

    # print x
    # print y
    if visited[x][y]:
        return False

    if x == MAP_ROWS - 1 and y == MAP_COLS - 1:
        return True

    visited[x][y] = True
    if not cells[x][y].right:
        path.append((x, y))
        if dfs(cells, x, y+1, visited, path):
            return True
        path.remove((x, y))

    if not cells[x][y].top:
        path.append((x, y))
        if dfs(cells, x-1, y, visited, path):
            return True
        path.remove((x, y))

    if not cells[x][y].left:
        path.append((x, y))
        if dfs(cells, x, y-1, visited, path):
            return True
        path.remove((x, y))

    if not cells[x][y].bottom:
        path.append((x, y))
        if dfs(cells, x+1, y, visited, path):
            return True
        path.remove((x, y))

def keyboard_input(player):

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ESCAPE:
        return True

    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)

    if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)

    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)

    if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)

    return False

def main():

    player = Object(1, 1, '@', libtcod.white)

    libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'maze game', False)

    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    libtcod.sys_set_fps(LIMIT_FPS)

    cells = kruskal.generate_maze(MAP_ROWS, MAP_COLS)

    make_map(cells)

    while not libtcod.console_is_window_closed():

        # player.draw(con)
        render_all(player, con)

        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        player.erase(con)

        quit = keyboard_input(player)

        if quit:
            render_solution(cells, con)
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)
            break

if __name__ == '__main__':
    main()
