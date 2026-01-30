#imports
import os

#folder names
data_folder = "data"
save_folder = os.path.join(data_folder, "saves")
current_folder = os.path.join(data_folder, "current")
perma_folder = os.path.join(data_folder, "permanent")

#paths
cwd = os.getcwd()
save_path = os.path.join(cwd, save_folder)
current_game_path = os.path.join(cwd, current_folder)
perma_path = os.path.join(cwd, perma_folder)

#pieces
empty = "empty"

wpawn = "wpawn"
wrook = "wrook"
wknight = "wknight"
wbishop = "wbishop"
wqueen = "wqueen"
wking = "wking"

bpawn ="bpawn"
brook = "brook"
bknight = "bknight"
bbishop = "bbishop"
bqueen = "bqueen"
bking = "bking"

#piece lists
pieces = [empty, wpawn, wrook, wknight, wbishop, wqueen, wking, bpawn, brook, bknight, bbishop, bqueen, bking]
piece_values = ["empty", "wpawn", "wrook", "wknight", "wbishop", "wqueen", "wking", "bpawn", "brook", "bknight", "bbishop", "bqueen", "bking"]

#coord types
coords_hor = ["0","a", "b", "c", "d", "e", "f", "g", "h"]
coords_ver = ["0","1", "2", "3", "4", "5", "6", "7", "8"]

#array
HOR = {c: i for i, c in enumerate(" abcdefgh")}
VER = {c: i for i, c in enumerate(" 12345678")}

#player data
PlayerData = {
    1: {
        "name": "WHITE",
        "opponent": "BLACK",
        "pieces": [wking, wbishop, wpawn, wknight, wrook, wqueen],
        "opponent_pieces": [bking, bbishop, bpawn, bknight, brook, bqueen],
        "direction": 1,
        "next": 2,
    },
    2: {
        "name": "BLACK",
        "opponent": "WHITE",
        "pieces": [bking, bbishop, bpawn, bknight, brook, bqueen],
        "opponent_pieces": [wking, wbishop, wpawn, wknight, wrook, wqueen],
        "direction": -1,
        "next": 1
    }
}