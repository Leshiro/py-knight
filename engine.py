#imports
import os

#folder names
save_folder = "saves"
current_folder = "current"
perma_folder = "permanent"

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

#load .txt files
def load_data(folder, file):
    global moves, turn
    with open(rf"{folder}\{file}", 'r') as file:
        file_content = file.read()
        coords_list = file_content.split("\n")
        turn = int(coords_list[0].replace("turn=",""))
        if turn != 1 and turn != 2:
            turn = 1 
        moves = int(coords_list[1].replace("moves=",""))
        coords_list.remove(coords_list[0])
        coords_list.remove(coords_list[0])
        for n in range(len(coords_list)):
            coord = coords_list[n][3:]
            i = piece_values.index(coord)
            coords_list[n] = pieces[i]                               
        coords_list.insert(0, "START")
        coords = {}
        for i in range(1, 9):
            for a in range(1, 9):
                coords[f"{coords_hor[a]}{coords_ver[i]}"] = coords_list[(i - 1) * 8 + a]
        return coords    

#collision checks
def diagonal_collision_check(s, e):
    collisions = 0
    horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
    vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
    if abs(horizontal_change) == abs(vertical_change):
        change = abs(horizontal_change)
        if horizontal_change > 0 and vertical_change > 0: #direction 1
            dx = 1
            dy = 1
        if horizontal_change < 0 and vertical_change > 0: #direction 2
            dx = -1
            dy = 1
        if horizontal_change < 0 and vertical_change < 0: #direction 3
            dx = -1
            dy = -1
        if horizontal_change > 0 and vertical_change < 0: #direction 4
            dx = 1
            dy = -1
        for n in range(1, change):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])+n * dx]}{coords_ver[coords_ver.index(s[1])+n * dy]}"]
            if check_collision != empty:
                collisions = collisions + 1
        return False if collisions > 0 else True

def collision_check(s, e):
    collisions = 0
    horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
    vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
    dx = 1 if horizontal_change > 0 else -1
    dy = 1 if vertical_change > 0 else -1
    for n in range(1, abs(horizontal_change)):
        check_collision = coords[f"{coords_hor[coords_hor.index(s[0])+n * dx]}{s[1]}"]
        if check_collision != empty:
            collisions = collisions + 1               
    for n in range(1, abs(vertical_change)):
        check_collision = coords[f"{s[0]}{coords_ver[coords_ver.index(s[1])+n * dy]}"]
        if check_collision != empty:
            collisions = collisions + 1
    return False if collisions > 0 else True

#event checks
def capture_check(edc):  
    global capture  
    if coords[edc] != empty:
        capture = 1
    else:
        capture = 0
    return capture

def promotion_check(stc, edc):
    promotion = 0
    if (coords[stc] == wpawn and edc[1] == "8") or (coords[stc] == bpawn and edc[1] == "1"):
        promotion = 1
    return promotion

def mate_check(check, printmsg=False):
    viable_moves = find_viable_moves()
    if len(viable_moves) == 0:
        if check == 0:
            mate = 2
            if printmsg:
                print(f"Stalemate! [{player}] has no moves to play.\n") 
        elif check == 1:
            mate = 1
            if printmsg:
                print(f"Checkmate! [{opponent}] wins the game.\n")
    else:
        mate = 0
    return mate

#get king coordinate
def get_king_cd(pieces):
    for i in coords:
        if coords[i] == pieces[0]:
            king_cd = i
            break
    return king_cd

def check_check(print_msg, turn_given=None):
    if turn_given != None:
        player_data = PlayerData[turn_given]
    else:
        player_data = PlayerData[turn]
    own_pieces = player_data["pieces"]
    opponent_pieces = player_data["opponent_pieces"]
    direction = player_data["direction"]

    #get king coordinate
    king_cd = get_king_cd(own_pieces)

    #get covered cds
    covered_cds = []
    for s in coords:
        piece = coords[s]
        if piece != empty:
            for e in coords:
                if s != e and e not in covered_cds:
                    #changes
                    dx = coords_hor.index(e[0]) - coords_hor.index(s[0])
                    dy = coords_ver.index(e[1]) - coords_ver.index(s[1])

                    if piece == opponent_pieces[0]: #king
                        if abs(dx) <= 1 and abs(dy) <= 1:
                            if coords[e] not in opponent_pieces:
                                covered_cds.append(e)
                    if piece == opponent_pieces[1]: #bishop
                        if abs(dx) == abs(dy):
                            passes_collision = diagonal_collision_check(s, e)
                            if passes_collision:
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)
                    if piece == opponent_pieces[2]: #pawn
                        if (dy) == 1 * -1 * direction and abs(dx) == 1:
                            if coords[e] not in opponent_pieces:
                                covered_cds.append(e)
                    if piece == opponent_pieces[3]: #knight
                        if abs(dx) == 1 and abs(dy) == 2:
                            covered_cds.append(e)
                        elif abs(dx) == 2 and abs(dy) == 1:    
                            covered_cds.append(e)
                    if piece == opponent_pieces[4]: #rook
                        if dx == 0 or dy == 0:
                            passes_collision = collision_check(s, e)  
                            if passes_collision:
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)
                    if piece == opponent_pieces[5]: #queen
                        if dx == 0 or dy == 0:
                            passes_collision = collision_check(s, e)  
                            if passes_collision:
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)
                        elif abs(dx) == abs(dy):
                            passes_collision = diagonal_collision_check(s, e)
                            if passes_collision:        
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)    
    #check detection
    check = 0
    if king_cd in covered_cds:
        check = 1
        if print_msg == 1:
            print(f"The {player} [King] is in check!")
    else:
        check = 0
    return check

#viable moves
def find_viable_moves(stc=None):
    global piece
    player_data = PlayerData[turn]
    own_pieces = player_data["pieces"]
    direction = player_data["direction"]
    #find playable moves
    playable = []
    for s in coords:
        piece = coords[s]
        if piece in own_pieces:
            for e in coords:
                if s != e and e not in playable and ((coords[e] not in own_pieces) or (piece == own_pieces[0] and coords[e] == own_pieces[4])):
                    #changes
                    dx = coords_hor.index(e[0]) - coords_hor.index(s[0])
                    dy = coords_ver.index(e[1]) - coords_ver.index(s[1])

                    if piece == own_pieces[0]: #king
                        if coords[e] == own_pieces[4]: #castling
                            if (s[0] == "e")  and (e[0] in ["a", "h"] and e[1] in ["1", "8"]):
                                passes_collision = collision_check(s, e)
                                if passes_collision:
                                    if abs(dx) == 3:
                                        playable.append(s+e + " (O-O)")
                                    if abs(dx) == 4:
                                        playable.append(s+e + " (O-O-O)")
                        else:
                            if abs(dx) <= 1 and abs(dy) <= 1:
                                playable.append(s+e)
                    if piece == own_pieces[1]: #bishop
                        passes_collision = diagonal_collision_check(s, e)
                        if passes_collision:
                            playable.append(s+e)
                    if piece == own_pieces[2]: #pawn
                        if coords[e] == empty and dx == 0 and (dy) == 1 * direction:
                            playable.append(s+e)
                        if coords[e] == empty and dx == 0 and coords_ver.index(s[1]) == 4.5 - (2.5 * direction) and (dy) == 2 * direction and coords[f"{e[0]}{int(e[1]) + (-1 * direction)}"] == empty:
                            playable.append(s+e)
                        if coords[e] != empty and abs(dx) == 1 and (dy) == 1 * direction:
                            playable.append(s+e) 
                    if piece == own_pieces[3]: #knight
                        if abs(dx) == 1 and abs(dy) == 2:
                            playable.append(s+e)
                        elif abs(dx) == 2 and abs(dy) == 1:    
                            playable.append(s+e)
                    if piece == own_pieces[4]: #rook
                        if dx == 0 or dy == 0:
                            passes_collision = collision_check(s, e)  
                            if passes_collision:
                                playable.append(s+e)
                    if piece == own_pieces[5]: #queen
                        if dx == 0 or dy == 0:
                            passes_collision = collision_check(s, e) 
                            if passes_collision:
                                playable.append(s+e)
                        elif abs(dx) == abs(dy):
                            passes_collision = diagonal_collision_check(s, e)
                            if passes_collision:        
                                playable.append(s+e)  
    viable = []
    for move in playable:
        #save previous state
        stc_p = coords[move[:2]]
        edc_p = coords[move[2:4]]
        #check if move escapes check
        piece = stc_p
        ghost_move(move)
        check = check_check(0)
        if check == 0:
            viable.append(move)
        #revert move
        if "(" in move and ")" in move:
            uncastle(move)
        coords[move[:2]] = stc_p
        coords[move[2:4]] = edc_p
    return viable

#game operations
def save_game(save_file_name):
    saved = 0
    while saved == 0:
        file_name = save_file_name
        try:
            with open(rf"{save_folder}\{file_name}.txt", "x") as file:
                file.write(f"turn={turn}\nmoves={moves}")
                for coord in coords:
                    coord_piece = coords[coord]
                    i = pieces.index(coord_piece)
                    piece_name = piece_values[i]
                    line = coord + "=" + piece_name
                    file.write(f"\n{line}")
                saved = 1
                print(f"Game successfully saved to [{file_name}.txt].\n")
                exists = 0
        except FileExistsError:
            print(f"[{file_name}.txt] already exists, please enter another name.")
            exists = 1
        return exists             
def save_current_state():
    with open(rf"{current_folder}\move{moves}.txt", "x") as file:
        file.write(f"turn={turn}\nmoves={moves}")
        for coord in coords:
            coord_piece = coords[coord]
            i = pieces.index(coord_piece)
            piece_name = piece_values[i]
            line = coord + "=" + piece_name
            file.write(f"\n{line}")

#after turn reset
def afterturn_reset():
    global check, capture, checkmate, stalemate, promotion
    check = 0
    capture = 0
    checkmate = 0
    stalemate = 0 
    promotion = 0

def castle(move):
    global coords
    stc = move[:2]
    player_data = PlayerData[turn]
    player = player_data["name"]
    coords[stc] = empty 
    if player == "WHITE":
        if "(O-O-O)" in move:
            coords["a1"] = empty
            coords["b1"] = wking
            coords["c1"] = wrook 
        if "(O-O)" in move:
            coords["h1"] = empty
            coords["g1"] = wking
            coords["f1"] = wrook
    if player == "BLACK":
        if "(O-O-O)" in move:
            coords["a8"] = empty
            coords["b8"] = bking
            coords["c8"] = brook
        if "(O-O)" in move:
            coords["h8"] = empty
            coords["g8"] = bking
            coords["f8"] = brook

def uncastle(move):
    global coords
    player_data = PlayerData[turn]
    player = player_data["name"]
    if player == "WHITE":
        if "(O-O-O)" in move:
            coords["b1"] = empty
            coords["c1"] = empty  
        if "(O-O)" in move:
            coords["g1"] = empty
            coords["f1"] = empty
    if player == "BLACK":
        if "(O-O-O)" in move:
            coords["b8"] = empty
            coords["c8"] = empty 
        if "(O-O)" in move:
            coords["g8"] = empty
            coords["f8"] = empty

#move functions
def play_move(move, promoted_to=None):
    stc = move[:2]
    edc = move[2:4]
    piece = coords[stc]
    capture = capture_check(edc)
    promotion = promotion_check(stc, edc)
    if promotion == 1:
        if piece == wpawn:
            color = "w"
        if piece == bpawn:
            color = "b"
        new_piece = color + promoted_to
        coords[edc] =  new_piece
        coords[stc] = empty
    else:
        ghost_move(move)

    piece_name = piece[1:].capitalize()
    if capture == 0: 
        print(f"- {player} plays [{piece_name}] to [{edc}].\n")
    elif capture == 1:
        i = pieces.index(coords[edc])
        captured_piece_name = piece_values[i][1:].capitalize()
        print(f"- {player} plays [{piece_name}] to [{edc}] and captures the [{captured_piece_name}]!\n")
    if promotion == 1: 
        chosen_piece = new_piece[1:].capitalize()
        print(f"- The {player} [{piece_name}] has been promoted to [{chosen_piece.capitalize()}]!\n")     

def ghost_move(move):
    stc = move[:2]
    edc = move[2:4]
    piece = coords[stc]
    if "(" in move and ")" in move:
        castle(move)
    else:
        coords[edc] = piece
        coords[stc] = empty   

def undo_move():
    global coords
    file_exists = 0
    for file in os.listdir(current_game_path):
        if file == f"move{moves-1}.txt":
            file_exists = 1
            coords = load_data(current_folder, file)
            break
    if file_exists == 0:
        print("Previous move does not exist.\n")
    else:
        file = f"move{moves+1}.txt"
        file_path = os.path.join(current_game_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
    return file_exists

def try_move(input, promoted_to=None):
    global move, turn, moves
    global player, opponent, direction, own_pieces, opponent_pieces

    #load turn data
    player_data = PlayerData[turn]
    player = player_data["name"]
    opponent = player_data["opponent"]
    own_pieces = player_data["pieces"]
    opponent_pieces = player_data["opponent_pieces"]
    direction = player_data["direction"]

    #get move
    move = input
    play_move(move, promoted_to)

    #next turn
    turn = PlayerData[turn]["next"]
    moves = moves + 1
    save_current_state()
    afterturn_reset()

    #load turn data (next)
    player_data = PlayerData[turn]
    player = player_data["name"]
    opponent = player_data["opponent"]
    own_pieces = player_data["pieces"]
    opponent_pieces = player_data["opponent_pieces"]
    direction = player_data["direction"]

#load & start game
def load_game(savefilename=None):
    #create saves folder
    cwd = os.getcwd()
    save_path = rf"{cwd}\{save_folder}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    #create current folder
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)
        
    #clear current folder
    global current_game_path
    current_game_path = rf"{cwd}\{current_folder}"
    for file in os.listdir(current_game_path):
        file_path = os.path.join(current_game_path, file)
        if os.path.isfile(file_path) and file[:4] == "move":
            os.remove(file_path)

    #defaultcoords
    default_coords = load_data(perma_folder, "default.txt")

    #load save data
    global coords, moves, turn
    if savefilename != None:  
        save_file = savefilename
        save_file = save_file.lower().strip()
        if save_file[-4:] != ".txt":
            save_file = save_file + ".txt"
        #load save file
        try: 
            coords = load_data(save_folder, save_file)
            message = (f"[{save_file}] loaded successfully.")
        except FileNotFoundError:
            if save_file != ".txt":   
                message = (f"Save file [{save_file}] does not exist.")
                return message
        except:
            message = (f"Save file [{save_file}] is corrupted.")
            return message
    else:
        message = None
        coords = default_coords
        turn = 1
        moves = 0
    
    #at start
    afterturn_reset()
    save_current_state()

    check = check_check(1)
    mate_check(check)
    
    return message