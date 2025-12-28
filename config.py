import colors

title = "Chess Alpha"
author = "Leshiro"
icon = "assets/icon.png"

piece_folder = "assets/pieces/default"
sound_folder = "assets/sounds"

window_minimum = 180
charpixel = 6

fps_limit = 20

def switch_palette(value):
    global CHOSEN_PALETTE
    keys = list(colors.BOARD_PALETTES)
    i = keys.index(CHOSEN_PALETTE)
    CHOSEN_PALETTE = keys[(i + value) % len(keys)]
    return colors.BOARD_PALETTES[CHOSEN_PALETTE]

CHOSEN_PALETTE = "WOOD_CLASSIC"
BOARD_COLORS = colors.BOARD_PALETTES[CHOSEN_PALETTE]

LIGHT = BOARD_COLORS[0]
DARK = BOARD_COLORS[1]

UI_COLOR = colors.dark_gray
LEGAL_MOVES_COLOR = colors.green_tint
SELECTION_COLOR = colors.red_tint
CHECKMATE_COLOR = colors.blue_tint

BOARD_SIZE = 640
UI_HEIGHT = 70
SEPARATOR = 15

BUTTON_W = 100
BUTTON_H = 35
GAP = 15
START_X = 20