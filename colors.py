#colors
black = (0, 0, 0)
dark_gray = (30, 30, 30)
gray = (80, 80, 80)

#tints
green_tint = (50, 180, 50, 150)
red_tint = (200, 50, 50, 150)
blue_tint = (30, 144, 255, 150)
yellow_tint = (255, 255, 0, 150)

#board palettes
BOARD_PALETTES = {
    #brown
    "WOOD_CLASSIC" : [(238, 210, 183), (160, 110, 70)],
    "CHESS.COM_BROWN" : [(240, 217, 181), (181, 136, 99)],
    "PARCHMENT" : [(245, 238, 220), (174, 155, 121)],

    #green
    "CHESS.COM_GREEN" : [(238, 238, 210), (118, 150, 86)],
    "TOURNAMENT" : [(235, 235, 231), (50, 103, 74)],
    "FADED_GREEN" : [(231, 237, 229), (132, 156, 136)],

    #blue
    "CHESS.COM_BLUE" : [(234, 233, 210), (75, 115, 153)],

    #red
    "CHESS.COM_RED" : [(245, 219, 195), (187, 50, 50)],
    "BLOOD_RED" : [(245, 210, 180), (139, 0, 0)],

    #dark
    "CHARCOAL" : [(79, 91, 102), (46, 52, 64)],
    "PURPLE_NIGHT" : [(94, 90, 111), (44, 42, 58)],
    "GRAPHITE" : [(90, 94, 98), (45, 47, 50)],
    "MIDNIGHT" : [(70, 74, 84), (30, 32, 38)],
}

def switch_palette(value):
    global CHOSEN_PALETTE
    keys = list(BOARD_PALETTES)
    i = keys.index(CHOSEN_PALETTE)
    CHOSEN_PALETTE = keys[(i + value) % len(keys)]
    return BOARD_PALETTES[CHOSEN_PALETTE]

#assign
CHOSEN_PALETTE = "WOOD_CLASSIC"
BOARD_COLORS = BOARD_PALETTES[CHOSEN_PALETTE]

LIGHT = BOARD_COLORS[0]
DARK = BOARD_COLORS[1]

BORDER_COLOR = dark_gray
UI_COLOR = dark_gray
COORDS_COLOR = gray
LEGAL_MOVES_COLOR = green_tint
SELECTION_COLOR = red_tint
LAST_MOVE_COLOR = yellow_tint
CHECKMATE_COLOR = blue_tint