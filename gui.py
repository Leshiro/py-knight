#import
import engine
import assets
import colors
import config

import pygame
import tkinter as tk

#assets
icon = assets.icon

piece_set = assets.chosen_set
piece_file_format = assets.piece_file_format
piece_assets = assets.piece_assets

sound_folder = assets.sound_folder

sound_folder = assets.sound_folder
sounds = assets.sounds

#colors
LIGHT = colors.LIGHT
DARK  = colors.DARK

BORDER_COLOR = colors.BORDER_COLOR
UI_COLOR = colors.UI_COLOR
LEGAL_MOVES_COLOR = colors.LEGAL_MOVES_COLOR
CHECKMATE_COLOR = colors.CHECKMATE_COLOR
SELECTION_COLOR = colors.SELECTION_COLOR

##config
title = config.title
author = config.author
fps_limit = config.fps_limit

#tkinter windows
minimum = config.window_minimum
charpixel = config.charpixel

#board & square size
BOARD_SIZE = config.BOARD_SIZE
UI_HEIGHT = config.UI_HEIGHT
SQ = BOARD_SIZE // 8
SIZE = BOARD_SIZE + UI_HEIGHT

#borders & separator
BORDER_THICKNESS = config.BORDER_THICKNESS
SEPARATOR = config.SEPARATOR

#board position
BOARD_1_X = 0 + BORDER_THICKNESS
BOARD_2_X = BOARD_SIZE + SEPARATOR + BORDER_THICKNESS
BOARD_Y = 0 + BORDER_THICKNESS

#window size
WINDOW_WIDTH = BORDER_THICKNESS * 2 + BOARD_SIZE * 2 + SEPARATOR
WINDOW_HEIGHT = BORDER_THICKNESS + BOARD_SIZE + UI_HEIGHT

#buttons
BUTTON_W = config.BUTTON_W
BUTTON_H = config.BUTTON_H
GAP = config.BUTTON_GAP
START_X = config.BUTTON_START_X

UI_Y = BOARD_Y + BOARD_SIZE
UI_Y_MIDPOINT = UI_Y + (UI_HEIGHT - BUTTON_H) // 2

###

def ask_string(title, label):
    result = {"value": None}

    text_size = len(label) * charpixel
    size = minimum + text_size

    def submit():
        result["value"] = entry.get()
        root.destroy()

    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size}x120")
    root.resizable(False, False)

    #center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=label, font=("Arial", 12)).pack(pady=10)
    entry = tk.Entry(root, font=("Arial", 14))
    entry.pack(padx=20, fill="x")
    entry.focus()

    entry.bind("<Return>", lambda event: submit())

    tk.Button(root, text="OK", command=submit).pack(pady=10)

    root.mainloop()

    return result["value"]
def ask_yes_no(title, message):
    result = {"value": False}

    text_size = len(message) * charpixel
    size = minimum + text_size

    def yes():
        result["value"] = True
        root.destroy()

    def no():
        root.destroy()
        
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size}x90")
    root.resizable(False, False)

    # center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=message, font=("Arial", 12)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=(5, 0))

    tk.Button(frame, text="Yes", width=10, command=yes).pack(side="left", padx=10)
    tk.Button(frame, text="No", width=10, command=no).pack(side="right", padx=10)

    # keyboard support
    root.bind("<Return>", lambda e: yes())
    root.bind("<Escape>", lambda e: no())

    root.mainloop()

    return result["value"]
def notify(title, label):
    def close():
        root.destroy()

    text_size = len(label) * int(charpixel // 1.5)
    size = minimum + text_size

    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size}x85")
    root.resizable(False, False)

    #center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=label, font=("Arial", 12)).pack(padx=10, pady=(10, 10))
    tk.Button(root, text="OK", command=close).pack(pady=(0, 10))

    root.bind("<Return>", lambda event: close())

    root.mainloop()
def ask_promo(title, message):
    result = {"value": None}

    text_size = len(message) * charpixel
    size = minimum + text_size

    def queen():
        result["value"] = "queen"
        root.destroy()
    def rook():
        result["value"] = "rook"
        root.destroy()
    def bishop():
        result["value"] = "bishop"
        root.destroy()
    def knight():
        result["value"] = "knight"
        root.destroy()
        
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{size+100}x90")
    root.resizable(False, False)

    # center window
    root.update_idletasks()
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(root, text=message, font=("Arial", 12)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=(5, 0))

    tk.Button(frame, text="Queen", width=10, command=queen).pack(side="left", padx=5)
    tk.Button(frame, text="Rook", width=10, command=rook).pack(side="left", padx=5)
    tk.Button(frame, text="Bishop", width=10, command=bishop).pack(side="right", padx=5)
    tk.Button(frame, text="Knight", width=10, command=knight).pack(side="right", padx=5)

    root.mainloop()

    return result["value"]

pygame.init()

#pygame start
font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.NOFRAME)
pygame.display.set_caption(title)
#no icon yet - pygame.display.set_icon(pygame.image.load(icon).convert_alpha())
clock = pygame.time.Clock()

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

SOUNDS = {}
for sound in sounds:
    SOUNDS.update({sound : pygame.mixer.Sound(f"{sound_folder}{sounds[sound]}")})

def Start_Game(save=None):
    global end_notified
    end_notified = 0
    message = engine.load_game(save)
    return message

def load_images(piece_set):
    images = {}
    for name in assets.piece_assets.values():
        img = pygame.image.load(f"{piece_set}/{name}.{piece_file_format}").convert_alpha()
        images[name] = pygame.transform.smoothscale(img, (SQ, SQ))
    return images

Start_Game()
SOUNDS["start"].play()
PIECE_IMAGES = load_images(piece_set)

class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.hovered = False
        self.flash_t = 0

    #update on hover
    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    #draw button
    def draw(self, screen, font):
        if self.hovered:
            bg = (100, 100, 100) #hover color
        else:
            bg = (70, 70, 70)

        pygame.draw.rect(screen, bg, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        txt = font.render(self.text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    #do something on click
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.action()

def save_game_dialog():
    exists = 1
    file_name = ask_string(title, "Enter save file name:")
    if file_name == None or file_name == "":
        return
    exists = engine.save_game(file_name)
    while exists == 1:
        file_name = ask_string(title, f"[{file_name}.txt] already exists, please enter another name:")
        if file_name == None or file_name == "":
            return
    exists = engine.save_game(file_name)
    notify(title, f"Saved game to [{file_name}.txt]")

def load_game_dialog():
    file_name = ask_string(title, "Load save file:")
    if file_name:
        message = Start_Game(file_name)
        if message != None:
            notify(title, message)
        SOUNDS["start"].play()

def confirm_undo():
    confirm = ask_yes_no(title, "Undo move?")
    if confirm == True:
        exists = engine.undo_move()
        global end_notified
        end_notified = 0
        if exists == 1:
            SOUNDS["move"].play()
        else:
            notify(title, "Previous move does not exist.")

def confirm_restart():
    confirm = ask_yes_no(title, "Restart game?")
    if confirm == True:
        Start_Game()

def confirm_quit():
    confirm = ask_yes_no(title, "Quit game?")
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
    PIECE_IMAGES = load_images(piece_set)

save_button = Button((START_X + (BUTTON_W + GAP) * 0, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Save", lambda: save_game_dialog())
load_button = Button((START_X + (BUTTON_W + GAP) * 1, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Load", lambda: load_game_dialog())
undo_button = Button((START_X + (BUTTON_W + GAP) * 2 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Undo", lambda: confirm_undo())
restart_button = Button((START_X + (BUTTON_W + GAP) * 3 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Restart", lambda: confirm_restart())
quit_button = Button((START_X + (BUTTON_W + GAP) * 4 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Quit", lambda: confirm_quit())
previous_palette = Button((START_X + (BUTTON_W + GAP) *5 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Palette-1", lambda: switch_palette(-1))
next_palette = Button((START_X + (BUTTON_W + GAP) *6   , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Palette+1", lambda: switch_palette(1))
previous_set = Button((START_X + (BUTTON_W + GAP) *7 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Pieces-1", lambda: switch_piece_set(-1))
next_set = Button((START_X + (BUTTON_W + GAP) *8 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Pieces+1", lambda: switch_piece_set(1))

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
                notify(title, f"Checkmate! [{opponent}] wins the game.")
            if mate == 2:
                notify(title, f"Stalemate! [{player}] has no moves to play.")
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
        new_piece = ask_promo(title, "Promote pawn to: ")
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

def draw_board_at(offset_x, offset_y, flipped):
    for rank in range(8):
        for file in range(8):
            draw_file = 7 - file if flipped else file
            draw_rank = rank if flipped else 7 - rank
            color = LIGHT if (rank + file) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (offset_x + draw_file * SQ, offset_y + draw_rank * SQ, SQ, SQ))

def draw_pieces_at(offset_x, offset_y, flipped):
    for square, piece in engine.coords.items():
        if piece != engine.empty:
            x, y = square_to_screen(square, offset_x, offset_y, flipped)
            screen.blit(PIECE_IMAGES[piece_assets[piece]], (x, y))

def draw_selection_at(offset_x, offset_y, flipped):
    if not selected_square:
        return

    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(SELECTION_COLOR)

    x, y = square_to_screen(selected_square, offset_x, offset_y, flipped)
    screen.blit(overlay, (x, y))

def draw_checkmate_at(offset_x, offset_y, flipped):
    player_data = engine.PlayerData[engine.turn]
    own_pieces = player_data["pieces"]
    selected_square = engine.get_king_cd(own_pieces)
    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(CHECKMATE_COLOR)

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
    overlay.fill(LEGAL_MOVES_COLOR)

    for sq in legal_targets:
        x, y = square_to_screen(sq, offset_x, offset_y, flipped)
        screen.blit(overlay, (x, y))

def draw(end=None):
    screen.fill(UI_COLOR)
    #boards
    draw_board_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_board_at(BOARD_2_X, BOARD_Y, flipped=True)

    #legal moves
    draw_legal_moves_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_legal_moves_at(BOARD_2_X, BOARD_Y, flipped=True)

    #selection
    draw_selection_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_selection_at(BOARD_2_X, BOARD_Y, flipped=True)

    #checkmate
    if end !=None and end:
        draw_checkmate_at(BOARD_1_X, BOARD_Y, flipped=False)
        draw_checkmate_at(BOARD_2_X, BOARD_Y, flipped=True)
    
    #pieces (last)
    draw_pieces_at(BOARD_1_X, BOARD_Y, flipped=False)
    draw_pieces_at(BOARD_2_X, BOARD_Y, flipped=True)

    #border
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), BORDER_THICKNESS)
    #UI menu
    pygame.draw.rect(screen, UI_COLOR, (0, UI_Y, WINDOW_WIDTH, UI_HEIGHT))

    #UI buttons
    save_button.draw(screen, font)
    load_button.draw(screen, font)
    undo_button.draw(screen, font)
    restart_button.draw(screen, font)
    quit_button.draw(screen, font)
    previous_palette.draw(screen, font)
    next_palette.draw(screen, font)
    previous_set.draw(screen, font)
    next_set.draw(screen, font)

    pygame.display.flip()

selected_square = None
legal_targets = []
end = end_check(1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        save_button.handle_event(event)
        load_button.handle_event(event)
        undo_button.handle_event(event)
        restart_button.handle_event(event)
        quit_button.handle_event(event)
        previous_palette.handle_event(event)
        next_palette.handle_event(event)
        previous_set.handle_event(event)
        next_set.handle_event(event)

        #when clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            square = screen_to_square(mx, my)
            if square is None:
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

    save_button.update()
    load_button.update()
    undo_button.update()
    restart_button.update()
    quit_button.update()
    previous_palette.update()
    next_palette.update()
    previous_set.update()
    next_set.update()

    draw(end)
    
    clock.tick(fps_limit)

pygame.quit()