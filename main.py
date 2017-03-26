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
    player.draw(con)
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].wall
            if x == 0 or y == 0:
                libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.dark_green)
            if wall:
                libtcod.console_put_char_ex(con, x, y, '#', libtcod.white, libtcod.dark_blue)

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

        exit = keyboard_input(player)
        if exit:
            break

if __name__ == '__main__':
    main()
