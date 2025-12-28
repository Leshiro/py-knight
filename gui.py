import engine
import game
import pygame
import tkinter as tk

config = game

title = config.title
minimum = config.window_minimum
charpixel = config.charpixel

piece_set = config.piece_set

LIGHT = config.LIGHT
DARK  = config.DARK

UI_COLOR = config.UI_COLOR
LEGAL_MOVES_COLOR = config.LEGAL_MOVES_COLOR
CHECKMATE_COLOR = config.CHECKMATE_COLOR
SELECTION_COLOR = config.SELECTION_COLOR

BOARD_SIZE = config.BOARD_SIZE
UI_HEIGHT = config.UI_HEIGHT
SQ = BOARD_SIZE // 8
SIZE = BOARD_SIZE + UI_HEIGHT

SEPARATOR = config.SEPARATOR
BOARD_2_X = BOARD_SIZE + SEPARATOR

WINDOW_WIDTH = BOARD_SIZE + BOARD_2_X
WINDOW_HEIGHT = BOARD_SIZE + UI_HEIGHT

BUTTON_W = config.BUTTON_W
BUTTON_H = config.BUTTON_H

GAP = config.GAP

UI_Y = BOARD_SIZE
UI_Y_MIDPOINT = UI_Y + (UI_HEIGHT - BUTTON_H) // 2
START_X = config.START_X

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

pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

SOUNDS = {
    "start": pygame.mixer.Sound("assets/sounds/game-start.mp3"),
    "end": pygame.mixer.Sound("assets/sounds/game-end.mp3"),
    "move": pygame.mixer.Sound("assets/sounds/move.mp3"),
    "capture": pygame.mixer.Sound("assets/sounds/capture.mp3"),
    "undo": pygame.mixer.Sound("assets/sounds/move.mp3"),
    "check": pygame.mixer.Sound("assets/sounds/check.mp3"),
    "castle": pygame.mixer.Sound("assets/sounds/castle.mp3"),
    "promote": pygame.mixer.Sound("assets/sounds/promote.mp3"),
}

def Start_Game(save=None):
    global end_notified
    end_notified = 0
    message = engine.load_game(save)
    return message

Start_Game()
SOUNDS["start"].play()

font = pygame.font.SysFont(None, 28)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(title)
icon = pygame.image.load(f"assets/icon.png").convert_alpha()
pygame.display.set_icon(icon)
info = pygame.display.Info()

pygame.draw.rect(
    screen,
    UI_COLOR,
    (0, UI_Y, BOARD_SIZE, UI_HEIGHT)
)

selected_square = None
running = True

PIECE_TO_IMAGE = {
    engine.wpawn: "wpawn",
    engine.wrook: "wrook",
    engine.wknight: "wknight",
    engine.wbishop: "wbishop",
    engine.wqueen: "wqueen",
    engine.wking: "wking",
    engine.bpawn: "bpawn",
    engine.brook: "brook",
    engine.bknight: "bknight",
    engine.bbishop: "bbishop",
    engine.bqueen: "bqueen",
    engine.bking: "bking",
}

def load_images():
    images = {}
    for name in PIECE_TO_IMAGE.values():
        img = pygame.image.load(f"assets/pieces/{piece_set}/{name}.png").convert_alpha()
        images[name] = pygame.transform.smoothscale(img, (SQ, SQ))
    return images

PIECE_IMAGES = load_images()

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

save_button = Button((START_X, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Save", lambda: save_game_dialog())
load_button = Button((START_X + BUTTON_W + GAP, UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Load", lambda: load_game_dialog())
undo_button = Button((START_X + (BUTTON_W + GAP) * 2 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Undo", lambda: confirm_undo())
restart_button = Button((START_X + (BUTTON_W + GAP) * 3 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Restart", lambda: confirm_restart())
quit_button = Button((START_X + (BUTTON_W + GAP) * 4 , UI_Y_MIDPOINT, BUTTON_W, BUTTON_H), "Quit", lambda: confirm_quit())

def end_check(popup=0, print=False):
    player_data = engine.PlayerData[engine.turn]
    player = player_data["name"]
    opponent = player_data["opponent"]
    is_check = engine.check_check(0)
    mate = engine.mate_check(is_check, print)
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

    is_castle = engine.coords[edc] in own_pieces
    if is_castle:
        dx = engine.coords_hor.index(edc[0]) - engine.coords_hor.index(stc[0])
        if abs(dx) == 3:
            move = move + " (O-O)"
        if abs(dx) == 4:
            move = move + " (O-O-O)"

    is_capture = engine.coords[edc] in opponent_pieces
    is_promotion = engine.promotion_check(stc, edc)
    if is_promotion:
        new_piece = ask_string(title, "Promote pawn to: ").strip().lower()
        engine.try_move(move, new_piece)
    else:
        engine.try_move(move)
    is_check = engine.check_check(0)
    is_end = end_check(0)

    #sounds
    if is_end:
        SOUNDS["end"].play()
    elif is_check == 1:
        SOUNDS["check"].play()
    elif is_capture:
        SOUNDS["capture"].play()
    elif is_castle:
        SOUNDS["castle"].play()
    elif is_promotion:
        SOUNDS["promote"].play()
    else:
        SOUNDS["move"].play()
    return is_end

def square_to_screen(square, offset_x, flipped):
    file = ord(square[0]) - ord('a')
    rank = int(square[1]) - 1

    if flipped:
        file = 7 - file
    rank = 7 - rank if not flipped else rank

    x = offset_x + file * SQ
    y = rank * SQ
    return x, y

def screen_to_square(mx, my):
    if my >= BOARD_SIZE:
        return None

    if mx < BOARD_SIZE:
        offset_x = 0
        flipped = False
    else:
        offset_x = BOARD_SIZE
        flipped = True

    file = (mx - offset_x) // SQ
    rank = my // SQ

    if flipped:
        file = 7 - file
    rank = 7 - rank if not flipped else rank

    return chr(ord('a') + file) + str(rank + 1)

def draw_board_at(offset_x, flipped):
    for rank in range(8):
        for file in range(8):
            draw_file = 7 - file if flipped else file
            draw_rank = rank if flipped else 7 - rank
            color = LIGHT if (rank + file) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, (offset_x + draw_file * SQ, draw_rank * SQ, SQ, SQ))

def draw_pieces_at(offset_x, flipped):
    for square, piece in engine.coords.items():
        if piece != engine.empty:
            x, y = square_to_screen(square, offset_x, flipped)
            screen.blit(PIECE_IMAGES[PIECE_TO_IMAGE[piece]], (x, y))

def draw_selection_at(offset_x, flipped):
    if not selected_square:
        return

    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(SELECTION_COLOR)

    x, y = square_to_screen(selected_square, offset_x, flipped)
    screen.blit(overlay, (x, y))

def draw_checkmate_at(offset_x, flipped):
    player_data = engine.PlayerData[engine.turn]
    own_pieces = player_data["pieces"]
    selected_square = engine.get_king_cd(own_pieces)
    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(CHECKMATE_COLOR)

    x, y = square_to_screen(selected_square, offset_x, flipped)
    screen.blit(overlay, (x, y))

def get_legal_targets(from_sq):
    targets = []
    viable_moves = engine.find_viable_moves()
    for move in viable_moves:
        if move[:2] == from_sq:
            targets.append(move[2:4])
    return targets

def draw_legal_moves_at(offset_x, flipped):
    overlay = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
    overlay.fill(LEGAL_MOVES_COLOR)

    for sq in legal_targets:
        x, y = square_to_screen(sq, offset_x, flipped)
        screen.blit(overlay, (x, y))

def draw(end):
    screen.fill((0, 0, 0))
 
    #boards
    draw_board_at(0, flipped=False)
    draw_board_at(BOARD_2_X, flipped=True)

    #legal moves
    draw_legal_moves_at(0, flipped=False)
    draw_legal_moves_at(BOARD_2_X, flipped=True)

    #selection
    draw_selection_at(0, flipped=False)
    draw_selection_at(BOARD_2_X, flipped=True)

    #checkmate
    if end:
        draw_checkmate_at(0, flipped=False)
        draw_checkmate_at(BOARD_2_X, flipped=True)
    
    #pieces (last)
    draw_pieces_at(0, flipped=False)
    draw_pieces_at(BOARD_2_X, flipped=True)

    #SEPARATOR
    pygame.draw.line(screen, UI_COLOR, ((BOARD_SIZE + BOARD_2_X) // 2, 0), ((BOARD_SIZE + BOARD_2_X) // 2, BOARD_SIZE), SEPARATOR)
    # UI bar
    pygame.draw.rect(screen, UI_COLOR, (0, UI_Y, WINDOW_WIDTH, UI_HEIGHT))

    # buttons
    save_button.draw(screen, font)
    load_button.draw(screen, font)
    undo_button.draw(screen, font)
    restart_button.draw(screen, font)
    quit_button.draw(screen, font)

    pygame.display.flip()

selected_square = None
legal_targets = []

while running:
    if end_notified == 0:
        end = end_check(1, True)
        if end:
            end_notified = 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        save_button.handle_event(event)
        load_button.handle_event(event)
        undo_button.handle_event(event)
        restart_button.handle_event(event)
        quit_button.handle_event(event)

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

    save_button.update()
    load_button.update()
    undo_button.update()
    restart_button.update()
    quit_button.update()

    draw(end)

pygame.quit()