import libtcodpy as libtcod
import random
import kruskal
import prim
import binarytree as bt

SCREEN_WIDTH = 110
SCREEN_HEIGHT = 60

TILE_SIZE = 4

MAP_ROWS = 27
MAP_WIDTH = TILE_SIZE * MAP_ROWS

MAP_COLS = 12
MAP_HEIGHT = TILE_SIZE * MAP_COLS

PANEL_HEIGHT = 10
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

LIMIT_FPS = 20

FOV_ALGO = 0 # default field of view algorithm provided by libtcod
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 4

class Cell:
    def __init__(self):
        self.top = True
        self.bottom = True
        self.left = True
        self.right = True

class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        global map
        global move_count
        global compute_fov
        if not map[self.x + dx][self.y + dy].wall:
            self.x += dx
            self.y += dy
            map[self.x][self.y].visited = True
            move_count += 1
            compute_fov = True

    def draw(self, con):
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def erase(self, con):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

class Tile:
    def __init__(self, is_wall):
        self.wall = is_wall
        self.explored = False
        self.visited = False

""" creates a 2D array of dimensions of map using the cell matrix given as input"""
def make_map(cells):
    global map

    map = [[ Tile(False)
        for y in xrange(MAP_HEIGHT) ]
        for x in xrange(MAP_WIDTH) ]

    for y in xrange(MAP_HEIGHT):
        map[0][y].wall = True
        map[0][y].explored = True
        map[MAP_WIDTH - 1][y].wall = True
        map[MAP_WIDTH - 1][y].explored = True

    for x in xrange(MAP_WIDTH):
        map[x][0].wall = True
        map[x][0].explored = True
        map[x][MAP_HEIGHT - 1].explored = True

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

""" Helper function to clear the entire map's contents"""
def erase_map(con):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            libtcod.console_put_char_ex(con, x, y, ' ', libtcod.white, libtcod.black)

""" Function to render walls of map using fog of war and field of view, panel and player
" fov_map: Existing field of view map
" check_explored: Boolean variable indicating whether fog of war needs to be enabled
" msgs: msgs to be rendered on panel
"""
def render_all(player, con, panel, fov_map, check_explored, msgs):
    libtcod.map_compute_fov(fov_map, player.x, player.y, TORCH_RADIUS, FOV_LIGHT_WALLS, FOV_ALGO)

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            visible = libtcod.map_is_in_fov(fov_map, x, y)
            compute_fov = False
            wall = map[x][y].wall
            if not visible and (map[x][y].explored or not check_explored):
                if check_explored:
                    color = libtcod.grey
                else:
                    color = libtcod.light_grey

                if wall:
                    libtcod.console_put_char_ex(con, x, y, '#', color, libtcod.black)

                else:
                    libtcod.console_put_char_ex(con, x, y, '.', color, libtcod.black)

            if visible:
                map[x][y].explored = True
                if wall:
                    libtcod.console_put_char_ex(con, x, y, '#', libtcod.light_yellow, libtcod.black)

                else:
                    libtcod.console_put_char_ex(con, x, y, '.', libtcod.light_yellow, libtcod.black)

    libtcod.console_put_char_ex(con, MAP_WIDTH-2, MAP_HEIGHT-2, 'X', libtcod.fuchsia, libtcod.black)

    render_panel(msgs, panel)

    player.draw(con)

""" Helper function to render panel
" msgs: messages to be displayed on panel
"""
def render_panel(msgs, panel):
    y = 1
    libtcod.console_clear(panel)
    for msg in msgs:
        libtcod.console_set_default_background(panel, libtcod.black)
        libtcod.console_set_default_foreground(panel, msg[1])
        libtcod.console_print_ex(panel, 2, y, libtcod.BKGND_NONE, libtcod.LEFT, msg[0])
        libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)
        y = y + 1;

    global move_count

    if move_count != 0:
        libtcod.console_set_default_background(panel, libtcod.black)
        libtcod.console_set_default_foreground(panel, libtcod.sky)
        libtcod.console_print_ex(panel, 70, 1, libtcod.BKGND_NONE, libtcod.LEFT, "Move count: " + str(move_count))
        libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

""" Helper function to render the route player has travelled"""
def render_travelled(con):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if(map[x][y].visited):
                libtcod.console_put_char_ex(con, x, y, '+', libtcod.green, libtcod.black)

""" Helper function to render the solution route"""
def render_solution(cells, con):
    visited = [[ False
        for y in xrange(MAP_COLS)]
        for x in xrange(MAP_ROWS)]

    # print cells[11][0].bottom

    path = []
    dfs(cells, 0, 0, visited, path)

    # print path

    for cell in path:
        # print cell
        for x in range(1, TILE_SIZE - 1):
            for y in range(1, TILE_SIZE - 1):
                libtcod.console_put_char_ex(con, cell[0] * TILE_SIZE + x, cell[1] * TILE_SIZE + y, '+', libtcod.light_sky, libtcod.black)
                pass

    for i in range(len(path)-1):
        if path[i][0] == path[i+1][0]:
            offset_x = 0
            offset_y = TILE_SIZE/2

            if path[i][1] > path[i+1][1]:
                # left cell
                offset_y *= -1
        else:
            offset_x = TILE_SIZE/2
            offset_y = 0

            if path[i][0] > path[i+1][0]:
                # upper cell
                offset_x *= -1

        for x in range(1, TILE_SIZE - 1):
            for y in range(1, TILE_SIZE - 1):
                libtcod.console_put_char_ex(con, path[i][0] * TILE_SIZE + x + offset_x, path[i][1] * TILE_SIZE + y + offset_y, '+', libtcod.dark_sky, libtcod.black) 

def dfs(cells, x, y, visited, path):
    if visited[x][y]:
        return False

    path.append((x, y))
    if x == MAP_ROWS - 1 and y == MAP_COLS - 1:
        return True

    visited[x][y] = True
    if not cells[x][y].right:
        if dfs(cells, x, y+1, visited, path):
            return True

    if not cells[x][y].top:
        if dfs(cells, x-1, y, visited, path):
            return True

    if not cells[x][y].left:
        if dfs(cells, x, y-1, visited, path):
            return True

    if not cells[x][y].bottom:
        if dfs(cells, x+1, y, visited, path):
            return True

    path.remove((x, y))
    return False

""" Function that takes in keyboard input for player movement, toggling map and exiting"""
def keyboard_input(player, con):

    global fog_of_war

    key = libtcod.console_wait_for_keypress(True)

    if key.vk == libtcod.KEY_ESCAPE:
        return True

    if key.vk == libtcod.KEY_SPACE:
        fog_of_war = not fog_of_war
        erase_map(con)

    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)

    if libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)

    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)

    if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)

    return False

""" Helper function to show in-game messages"""
def in_game_messages(msgs = []):
    msgs.append(("Game is in session...", libtcod.white))
    msgs.append(("", libtcod.white))
    msgs.append(("Use the arrow keys to move and reach the X on the right bottom corner", libtcod.light_blue))
    msgs.append(("Press Esc at any time to display solution and quit", libtcod.light_blue))
    msgs.append(("Press Space to toggle fog of war", libtcod.light_blue))
    return msgs

def main():

    player = Object(1, 1, '@', libtcod.red)

    libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    # specify screen size, title and whether or not fullscreen for root console
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'maze game', False)

    # off-screen console for the map
    con = libtcod.console_new(MAP_WIDTH, MAP_HEIGHT)

    # off-screen console for display panel
    panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

    # Only for real time, Frames per second
    libtcod.sys_set_fps(LIMIT_FPS)

    fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
    global compute_fov
    compute_fov = False

    cells = [[ Cell()
        for y in range(MAP_COLS)]
        for x in range(MAP_ROWS)]

    make_map(cells)

    msgs = []
    choice = 0

    global move_count
    move_count = 0

    while True:

        msgs.append(("Which algorithm would you like to generate the maze?", libtcod.white))
        msgs.append(("[1]. Kruskal's algorithm", libtcod.white))
        msgs.append(("[2]. Prim's algorithm", libtcod.white))
        msgs.append(("[3]. Binary tree method", libtcod.white))
        msgs.append(("[4]. Random method", libtcod.white))

        render_all(player, con, panel, fov_map, True, msgs)
        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        msgs = []

        form_messages = [("Maze has been formed by Kruskal's method", libtcod.green), ("Maze has been formed by Prim's method", libtcod.green), ("Maze has been formed by Binary tree method", libtcod.green)]

        key = libtcod.console_wait_for_keypress(True)

        if key.vk == libtcod.KEY_1:
            choice = 1

        if key.vk == libtcod.KEY_2:
            choice = 2

        if key.vk == libtcod.KEY_3:
            choice = 3

        if key.vk == libtcod.KEY_4:
            choice = random.randint(0, 3)

        if choice in [1, 2, 3]:
            print "User's choice for maze generation is " + str(choice)
            msgs.append(form_messages[choice-1])
            break

        else: 
            msgs.append(("Sorry that is not an option!", libtcod.red))
            msgs.append(("", libtcod.red))

    if choice == 1:
        (edges, cell_set, cell_list, cells) = kruskal.init_variables(MAP_ROWS, MAP_COLS)

        while cell_set.size() != 1:
            cells = kruskal.generate_maze(edges, cell_set, cell_list, cells)

    if choice == 2:
        (wall_set, cells_finished, cells) = prim.init_variables(MAP_ROWS, MAP_COLS)

        while len(cells_finished) != MAP_ROWS*MAP_COLS:
            cells = prim.generate_maze(wall_set, cells_finished, cells, MAP_ROWS, MAP_COLS)

    if choice == 3:
        (cells) = bt.init_variables(MAP_ROWS, MAP_COLS)

        for x in range(MAP_ROWS-1, -1, -1):
            for y in range(MAP_COLS):
                cells = bt.generate_maze(cells, x, y, MAP_ROWS, MAP_COLS)

    make_map(cells)

    msgs = in_game_messages(msgs)

    for y in xrange(MAP_HEIGHT):
        for x in xrange(MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].wall, not map[x][y].wall)

    render_all(player, con, panel, fov_map, True, msgs)
    libtcod.console_blit(con, 0, 0, MAP_WIDTH, MAP_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    global fog_of_war
    fog_of_war  = True

    while not libtcod.console_is_window_closed():

        if player.x == MAP_WIDTH-2 and player.y == MAP_HEIGHT-2:
            msgs = []
            msgs.append(("Congratulations! You have won the game", libtcod.purple))
            msgs.append(("", libtcod.white))
            msgs.append(("Displaying player's route in green", libtcod.light_green))
            msgs.append(("", libtcod.white))
            msgs.append(("Press any key to exit game now", libtcod.white))
            render_all(player, con, panel, fov_map, False, msgs)
            render_travelled(con)
            libtcod.console_put_char_ex(con, 1, 1, 'S', libtcod.pink, libtcod.black)
            player.draw(con)
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)
            break

        render_all(player, con, panel, fov_map, fog_of_war, msgs)

        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        player.erase(con)

        quit = keyboard_input(player, con)

        if quit:
            quit_msgs = []
            quit_msgs.append(("Are you sure you want to quit?", libtcod.red))
            quit_msgs.append(("", libtcod.red))
            quit_msgs.append(("Enter Esc again to display solution and exit", libtcod.white))
            quit_msgs.append(("Enter any other key otherwise", libtcod.white))

            render_all(player, con, panel, fov_map, True, quit_msgs)
            libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
            libtcod.console_flush()

            key = libtcod.console_wait_for_keypress(True)

            if key.vk == libtcod.KEY_ESCAPE:
                quit_msgs = []
                quit_msgs.append(("Displaying solution in blue", libtcod.sky))
                quit_msgs.append(("", libtcod.green))
                quit_msgs.append(("Displaying player's route (not overlapping with solution) in green", libtcod.light_green))
                quit_msgs.append(("", libtcod.green))
                quit_msgs.append(("Press any key to exit game now", libtcod.white))
                render_all(player, con, panel, fov_map, False, quit_msgs)
                render_travelled(con)
                render_solution(cells, con)
                player.draw(con)
                libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
                libtcod.console_flush()

                key = libtcod.console_wait_for_keypress(True)
                break

if __name__ == '__main__':
    main()
