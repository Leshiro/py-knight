#colors
black = (0, 0, 0)
dark_gray = (30, 30, 30)

#tints
green_tint = (50, 180, 50, 120)
red_tint = (200, 50, 50, 120)
blue_tint = (30, 144, 255, 120)

#board palettes
BOARD_PALETTES = {
    "WOOD_CLASSIC" : [(238, 210, 183), (160, 110, 70)],
    "GREEN_CLASSIC" : [(238, 238, 210), (118, 150, 86)],

    "FADED_GREEN" : [(231, 237, 229), (132, 156, 136)],
    "PARCHMENT" : [(245, 238, 220), (174, 155, 121)],

    "PURPLE_NIGHT" : [(94, 90, 111), (44, 42, 58)],
    "CHARCOAL" : [(79, 91, 102), (46, 52, 64)],
    "MIDNIGHT" : [(70, 74, 84), (30, 32, 38)],
    "GRAPHITE" : [(90, 94, 98), (45, 47, 50)],
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
LEGAL_MOVES_COLOR = green_tint
SELECTION_COLOR = red_tint
CHECKMATE_COLOR = blue_tint