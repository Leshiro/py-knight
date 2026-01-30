#imports
import os
import pygame

pygame.init()

#components
import engine

#ui
import ui.assets as assets
import ui.colors as colors
import ui.widgets as widgets

from ui.config import *
from ui.assets import SOUNDS
from ui.colors import LIGHT, DARK
from ui.widgets import Button, ExpandableButton

#tk
import ui.tk as tk

font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
pygame.display.set_caption(f"{title}")
clock = pygame.time.Clock()

#load & resize assets
def resize(img, width):
    w, h = img.get_size()
    ratio = width / w
    return pygame.transform.smoothscale(img, (int(w*ratio), int(h*ratio)))

icon_img = resize(pygame.image.load(assets.icon), assets.iconsize)
logo_img = resize(pygame.image.load(assets.logo), assets.logosize)
namelogo_img = resize(pygame.image.load(assets.namelogo), assets.namelogosize)

#start
def Start_Game(path=None):
    global end_notified
    end_notified = 0
    message, success = engine.load_game(path)
    return message, success

#first time
Start_Game()
SOUNDS["start"].play()
PIECE_IMAGES = assets.load_pieces(assets.chosen_set)

#create buttons & expandable buttons
save_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 0, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Save", lambda: save_game_dialog())
load_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 1, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Load", lambda: load_game_dialog())
undo_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 2 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Undo", lambda: confirm_undo())
restart_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 3 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Restart", lambda: confirm_restart())
quit_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 4 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Quit", lambda: confirm_quit())

palette_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 5, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Palette", lambda: None)
palette_prev = Button((0, 0, BUTTON_W, BUTTON_H), "Previous", lambda: switch_palette(-1))
palette_next = Button((0, 0, BUTTON_W, BUTTON_H), "Next", lambda: switch_palette(1))
palette_menu = ExpandableButton(palette_button, [palette_prev, palette_next])

pieces_button = Button((BUTTON_START_X + (BUTTON_W + BUTTON_GAP) * 6, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Pieces", lambda: None)
pieces_prev = Button((0, 0, BUTTON_W, BUTTON_H), "Previous", lambda: switch_piece_set(-1))
pieces_next = Button((0, 0, BUTTON_W, BUTTON_H), "Next", lambda: switch_piece_set(1))
pieces_menu = ExpandableButton(pieces_button, [pieces_prev, pieces_next])

#list of buttons
buttons = [
    save_button, 
    load_button, 
    undo_button, 
    restart_button, 
    quit_button,
    ]
expandable_menus = [
    palette_menu, 
    pieces_menu,
    ]

#engine connected
def end_check(popup=0):
    player_data = engine.PlayerData[engine.turn]
    player = player_data["name"]
    opponent = player_data["opponent"]
    is_check = engine.check_check()
    mate = engine.mate_check(is_check)
    end = False
    if mate != 0:
        end = True
        if popup == 1:
            if mate == 1:
                tk.notify(title, f"Checkmate! [{opponent}] wins the game.")
            if mate == 2:
                tk.notify(title, f"Stalemate! [{player}] has no moves to play.")
    return end

def make_move(move):
    player_data = engine.PlayerData[engine.turn]
    own_pieces = player_data["pieces"]
    opponent_pieces = player_data["opponent_pieces"]

    stc = move[:2]
    edc = move[2:4]

    viable_moves = engine.find_viable_moves(stc)

    for viable_move in viable_moves:
        if viable_move[:4] == move:
            move = viable_move

    is_castle = "O" in move
    is_enpassant = "enp" in move
    is_capture = engine.coords[edc] in opponent_pieces
    is_promotion = engine.promotion_check(stc, edc)
    if is_promotion:
        new_piece = tk.ask_promo(title, "Promote pawn to: ")
        engine.try_move(move, new_piece)
    else:
        engine.try_move(move)
    is_check = engine.check_check()
    is_end = end_check(0)

    #sounds
    if is_end:
        SOUNDS["end"].play()
    elif is_check == 1:
        SOUNDS["check"].play()
    elif is_capture or is_enpassant:
        SOUNDS["capture"].play()
    elif is_castle:
        SOUNDS["castle"].play()
    elif is_promotion:
        SOUNDS["promote"].play()
    else:
        SOUNDS["move"].play()
    return is_end

#ui functions
def save_game_dialog():
    path = tk.ask_file_save(title)
    if not path:
        return
    else:
        folder, filename = os.path.split(path)
        folder_name = os.path.basename(folder)
        engine.save_game(path)
    tk.notify(title, f"Saved game to [{folder_name}/{filename}]")

def load_game_dialog():
    file = tk.ask_file_open(title)
    if file:
        message, success = Start_Game(file)
        if message != None:
            tk.notify(title, message)
            if success:
                SOUNDS["start"].play()

def confirm_undo():
    confirm = tk.ask_yes_no(title, "Undo move?")
    if confirm == True:
        exists = engine.undo_move()
        global end_notified
        end_notified = 0
        if exists == 1:
            SOUNDS["move"].play()
        else:
            tk.notify(title, "Previous move does not exist.")

def confirm_restart():
    confirm = tk.ask_yes_no(title, "Restart game?")
    if confirm == True:
        Start_Game()
        SOUNDS["start"].play()

def confirm_quit():
    confirm = tk.ask_yes_no(title, "Quit game?")
    if confirm == True:
        exit()

def switch_palette(value):
    board_colors = colors.switch_palette(value)
    global LIGHT, DARK
    LIGHT = board_colors[0]
    DARK  = board_colors[1]

def switch_piece_set(value):
    global PIECE_IMAGES
    piece_set = assets.switch_piece_set(value)
    PIECE_IMAGES = assets.load_pieces(piece_set)

#sq2screen & screen2sq
def square_to_screen(square, offset_x, offset_y, flipped):
    file = ord(square[0]) - ord('a')
    rank = int(square[1]) - 1

    if flipped:
        file = 7 - file
    rank = 7 - rank if not flipped else rank

    x = offset_x + file * SQ
    y = offset_y + rank * SQ
    return x, y

def screen_to_square(mx, my):
    if my < BOARD_Y or my >= BOARD_Y + BOARD_SIZE:
        return None
    if BOARD_1_X < mx < BOARD_1_X + BOARD_SIZE:
        offset_x = BOARD_1_X
        flipped = False
    elif BOARD_2_X + BOARD_SIZE > mx > BOARD_2_X:
        offset_x = BOARD_2_X
        flipped = True
    else:
        return None
    file = (mx - offset_x) // SQ
    rank = (my - BOARD_Y) // SQ
    if flipped:
        file = 7 - file
    rank = 7 - rank if not flipped else rank

    return chr(ord('a') + file) + str(rank + 1)

#draw components
def draw_board_at(offset_x, offset_y, flipped):
    for rank in range(8):
        for file in range(8):
            draw_file = 7 - file if flipped else file
            draw_rank = rank if flipped else 7 - rank
            color = LIGHT if (rank + file) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (offset_x + draw_file * SQ, offset_y + draw_rank * SQ, SQ, SQ))

def draw_files_at(offset_x, offset_y, flipped):
    files = "abcdefgh"
    files = files[::-1] if flipped else files
    for file in range(8):
        label = font.render(files[file], True, colors.COORDS_COLOR)
        x = offset_x + file * SQ + SQ - label.get_width() - 2
        y = offset_y + 7 * SQ + SQ - label.get_height() - 2
        screen.blit(label, (x, y))

def draw_ranks_at(offset_x, offset_y, flipped):
    for rank in range(8):
        text =  str(rank + 1) if flipped else str(8 - rank)
        label = font.render(text, True, colors.COORDS_COLOR)
        x = offset_x + 2
        y = offset_y + rank * SQ + 2
        screen.blit(label, (x, y))

def draw_coordinates_at(offset_x, offset_y, flipped):
    draw_files_at(offset_x, offset_y, flipped)
    draw_ranks_at(offset_x, offset_y, flipped)

def draw_pieces_at(offset_x, offset_y, flipped):
    for square, piece in engine.coords.items():
        if piece != engine.empty:
            x, y = square_to_screen(square, offset_x, offset_y, flipped)
            screen.blit(PIECE_IMAGES[assets.piece_assets[piece]], (x, y))

def draw_selection_at(offset_x, offset_y, flipped):
    if not selected_square:
        return

    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(colors.SELECTION_COLOR)

    x, y = square_to_screen(selected_square, offset_x, offset_y, flipped)
    screen.blit(overlay, (x, y))

def last_move_at(offset_x, offset_y, flipped):
    if not selected_square:
        return

    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(colors.SELECTION_COLOR)

    x, y = square_to_screen(selected_square, offset_x, offset_y, flipped)
    screen.blit(overlay, (x, y))

def draw_checkmate_at(offset_x, offset_y, flipped):
    player_data = engine.PlayerData[engine.turn]
    own_pieces = player_data["pieces"]
    selected_square = engine.get_king_cd(own_pieces)
    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(colors.CHECKMATE_COLOR)

    x, y = square_to_screen(selected_square, offset_x, offset_y, flipped)
    screen.blit(overlay, (x, y))

def get_legal_targets(from_sq):
    targets = []
    viable_moves = engine.find_viable_moves(from_sq)
    for move in viable_moves:
        targets.append(move[2:4])
    return targets

def draw_legal_moves_at(offset_x, offset_y, flipped):
    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(colors.LEGAL_MOVES_COLOR)

    for sq in legal_targets:
        x, y = square_to_screen(sq, offset_x, offset_y, flipped)
        screen.blit(overlay, (x, y))

#main draw function
def draw(end=None):
    screen.fill((colors.BG_COLOR))
    #boards
    draw_board_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_board_at(BOARD_2_X, BOARD_Y, flipped=True)

    #coordinates
    draw_coordinates_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_coordinates_at(BOARD_2_X, BOARD_Y, flipped=True)

    #legal moves
    if engine.turn == 1:
        draw_legal_moves_at(BOARD_1_X, BOARD_Y, flipped=False)
    else:
        draw_legal_moves_at(BOARD_2_X, BOARD_Y, flipped=True)

    #selection
    if engine.turn == 1:
        draw_selection_at(BOARD_1_X, BOARD_Y, flipped=False)
    else: 
        draw_selection_at(BOARD_2_X, BOARD_Y, flipped=True)

    #checkmate
    if end !=None and end:
        draw_checkmate_at(BOARD_1_X, BOARD_Y, flipped=False)
        draw_checkmate_at(BOARD_2_X, BOARD_Y, flipped=True)
    
    #pieces (last)
    draw_pieces_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_pieces_at(BOARD_2_X, BOARD_Y, flipped=True)

    #border
    pygame.draw.rect(screen, colors.BORDER_COLOR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), BORDER_THICKNESS)
    #UI menu
    pygame.draw.rect(screen, colors.UI_COLOR, (0, UI_Y, WINDOW_WIDTH, UI_HEIGHT))

    #brand assets
    # screen.blit(logo_img, (LOGO_x, LOGO_Y))
    # screen.blit(namelogo_img, (NAMELOGO_X, NAMELOGO_Y))

    #UI buttons
    for button in buttons:
        button.draw(screen, font)
    for menu in expandable_menus:
        menu.draw(screen, font)

    pygame.display.flip()

selected_square = None
legal_targets = []
end = end_check(1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        ui_used = False #start with false

        #handle button & menu events
        for button in buttons:
            if button.handle_event(event):
                ui_used = True

        for menu in expandable_menus:
            if menu.handle_event(event):
                ui_used = True

        #when clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            square = screen_to_square(mx, my)
            if square is None:
                continue 

            if ui_used:
                continue

            # first click → select piece
            if selected_square is None:
                selected_square = square
                legal_targets = get_legal_targets(square)

            # second click → attempt move
            else:
                if square in legal_targets:
                    end = make_move(selected_square + square)
                # reset selection
                selected_square = None
                legal_targets = []

            if end_notified == 0:
                end = end_check(0)
                if end:
                    draw(end)
                    end = end_check(1)
                    end_notified = 1

    #update buttons & menus
    for button in buttons:
        button.update() 
    for menu in expandable_menus:
        menu.update()  

    draw(end)#draw game end (if true)

    clock.tick(fps_limit) #fps limiter

#quit
pygame.quit()