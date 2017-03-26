import libtcodpy as libtcod

SCREEN_WIDTH = 110
SCREEN_HEIGHT = 60
MAP_ROWS = 25
MAP_COLS = 12
LIMIT_FPS = 20

class Object:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, con):
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def erase(self, con):
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

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

    while not libtcod.console_is_window_closed():

        player.draw(con)

        libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
        libtcod.console_flush()

        player.erase(con)

        exit = keyboard_input(player)
        if exit:
            break

if __name__ == '__main__':
    main()
