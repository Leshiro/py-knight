import os

#icon
icon = None

#pieces
piece_assets = {
    "wpawn" : "wP",
    "wrook" : "wR",
    "wknight" : "wN",
    "wbishop" : "wB",
    "wqueen" : "wQ",
    "wking" : "wK",
    "bpawn" : "bP",
    "brook" : "bR",
    "bknight" : "bN",
    "bbishop" : "bB",
    "bqueen" : "bQ",
    "bking" : "bK",
}    
piece_file_format = "png"

default = "cburnett"

piece_folder = "assets/pieces/"
chosen_set = piece_folder + default 

piece_sets = []
for name in os.listdir(piece_folder):
    path = os.path.join(piece_folder, name)
    if os.path.isdir(path):
        piece_sets.append(piece_folder + name)

def switch_piece_set(value):
    global chosen_set
    current_set_i = piece_sets.index(chosen_set)
    new_i = (current_set_i + value) % len(piece_sets)
    chosen_set = piece_sets[new_i]
    return chosen_set

#sounds
sound_folder = "assets/sounds/"
sounds = {
    "start": "game-start.mp3",
    "end": "game-end.mp3",
    "move": "move.mp3",
    "capture": "capture.mp3",
    "undo": "move.mp3",
    "check": "check.mp3",
    "castle": "castle.mp3",
    "promote" : "promote.mp3",
}