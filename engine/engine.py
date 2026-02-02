#imports
import os

from engine.constant import *

#reader
def read_variables(coords_list):
    global moves, turn, king_moved, last_move
    turn = int(coords_list[0].replace("turn=","").strip())
    moves = int(coords_list[1].replace("moves=","").strip())

    king_moved = (coords_list[2].replace("king_moved=","")).strip().split("/")
    king_moved.insert(0, "None")

    last_move = coords_list[3].replace("last_move=","").strip()
    if last_move != "None":
        last_move = last_move.split("/")

def write_variables():
    #check if last move exist
    if last_move == None or last_move == "None":
        last_move_value = "None"
    else:
        last_move_value = f"{last_move[0]}/{last_move[1]}"
    #write variables
    variables = f"""turn={turn}
moves={moves}
king_moved={king_moved[1]}/{king_moved[2]}
last_move={last_move_value}
---"""
    return variables

#load .txt files
def load_data(folder, file):
    path = os.path.join(folder, file)
    with open(path, 'r', encoding="utf-8") as file:
        file_content = file.read()
        coords_list = file_content.split("\n")

        read_variables(coords_list)

        while "---" in coords_list:
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

#default game
def default_game():
    global coords
    coords = load_data(perma_path, "default.txt")

#save current         
def save_current_state():
    path = os.path.join(current_game_path, f"move{moves}.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write(write_variables())
        for coord in coords:
            coord_piece = coords[coord]
            i = pieces.index(coord_piece)
            piece_name = piece_values[i]
            line = coord + "=" + piece_name
            file.write(f"\n{line}")

#save game
def save_game(path):
    with open(path, "w", encoding="utf-8") as file:
        file.write(write_variables())
        for coord in coords:
            coord_piece = coords[coord]
            i = pieces.index(coord_piece)
            piece_name = piece_values[i]
            line = coord + "=" + piece_name
            file.write(f"\n{line}")
        
#load & start game
def load_game(path):
    #create saves folder
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    #create current folder
    if not os.path.exists(current_game_path):
        os.makedirs(current_game_path)
        
    #clear current folder
    for file in os.listdir(current_game_path):
        file_path = os.path.join(current_game_path, file)
        if os.path.isfile(file_path) and file[:4] == "move":
            os.remove(file_path)

    #load save data
    global coords
    if path != None:  
        try: 
            folder, file = os.path.split(path)
            coords = load_data(folder, file)
            message = (f"[{file}] loaded successfully.")
        except:
            message = (f"Save file [{file}] is corrupted.")
            return message, False
    else:
        default_game()
        message = None

    afterturn_reset()
    save_current_state()
    return message, True

### CHESS RULES

#collision checks
def diagonal_collision_check(s, e):
    collisions = 0
    horizontal_change = HOR[e[0]] - HOR[s[0]]
    vertical_change = VER[e[1]] - VER[s[1]]
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
    horizontal_change = HOR[e[0]] - HOR[s[0]]
    vertical_change = VER[e[1]] - VER[s[1]]
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

def mate_check(check):
    viable_moves = find_viable_moves()
    if len(viable_moves) == 0:
        if check == 0:
            mate = 2
        elif check == 1:
            mate = 1
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

def check_castleable(type):
    y = 1 if turn == 1 else 8
    if type == 4:
        xs = ["e", "d", "c"]
    if type == 3:
        xs = ["e", "f", "g"]
    for x in xs:
        coord = f"{x}{y}"
        check_sq = check_check(turn, coord)
        if check_sq == 1:
            return False
    return True

def check_check(turn_given=None, square=None):
    player_data = PlayerData[turn_given] if turn_given != None else PlayerData[turn]

    opponent_pieces = player_data["opponent_pieces"]
    direction = player_data["direction"]

    if square != None:
        king_cd = square
    else: 
        king_cd = get_king_cd(player_data["pieces"])

    for s in coords:
        piece = coords[s]
        if piece not in opponent_pieces:
            continue

        attacker_x = HOR[s[0]]
        attacker_y = VER[s[1]]

        king_x = HOR[king_cd[0]]
        king_y = VER[king_cd[1]]

        dx = king_x - attacker_x
        dy = king_y - attacker_y

        # opponent king
        if piece == opponent_pieces[0]:
            if abs(dx) <= 1 and abs(dy) <= 1:
                return 1
        # bishop
        elif piece == opponent_pieces[1]:
            if abs(dx) == abs(dy) and diagonal_collision_check(s, king_cd):
                return 1
        # pawn
        elif piece == opponent_pieces[2]:
            if dy == -direction and abs(dx) == 1:
                return 1
        # knight
        elif piece == opponent_pieces[3]:
            if (abs(dx), abs(dy)) in [(1, 2), (2, 1)]:
                return 1
        # rook
        elif piece == opponent_pieces[4]:
            if (dx == 0 or dy == 0) and collision_check(s, king_cd):
                return 1
        # queen
        elif piece == opponent_pieces[5]:
            if (
                ((dx == 0 or dy == 0) and collision_check(s, king_cd))
                or (abs(dx) == abs(dy) and diagonal_collision_check(s, king_cd))
            ):
                return 1
    return 0

#viable moves
def find_viable_moves(stc=None):
    global piece
    player_data = PlayerData[turn]
    own_pieces = player_data["pieces"]
    opponent_pieces = player_data["opponent_pieces"]
    direction = player_data["direction"]

    #find playable moves
    playable = []
    if stc != None:
        s_iter = [stc]
    else:
        s_iter = [sq for sq, p in coords.items() if p in own_pieces]
    for s in s_iter:
        piece = coords[s]
        if piece in own_pieces:
            for e in coords:
                if s != e and ((coords[e] not in own_pieces) or (piece == own_pieces[0] and coords[e] == own_pieces[4])):
                    #start
                    sx = HOR[s[0]]
                    sy = VER[s[1]]
                    #end
                    ex = HOR[e[0]]
                    ey = VER[e[1]]
                    #change
                    dx = ex - sx
                    dy = ey - sy
                    if piece == own_pieces[0]: #king
                        if coords[e] == own_pieces[4]: #castling
                            if (sx == 5) and (ex in [1, 8]) and ((ey == 1 and turn == 1) or (ey == 8 and turn == 2)):
                                if king_moved[turn] == "0":
                                    passes_collision = collision_check(s, e)
                                    if passes_collision:
                                        castleable = check_castleable(abs(dx))
                                        if castleable:
                                            if abs(dx) == 3:
                                                playable.append(s+e + "(O-O)")
                                            if abs(dx) == 4:
                                                playable.append(s+e + "(O-O-O)")
                        else:
                            if abs(dx) <= 1 and abs(dy) <= 1:
                                playable.append(s+e)
                    if piece == own_pieces[1]: #bishop
                        passes_collision = diagonal_collision_check(s, e)
                        if passes_collision:
                            playable.append(s+e)
                    if piece == own_pieces[2]: #pawn
                        #move 1 forward
                        if coords[e] == empty and dx == 0 and (dy) == 1 * direction:
                            playable.append(s+e)
                        #move 2 forward
                        if coords[e] == empty and dx == 0 and sy == 4.5 - (2.5 * direction) and (dy) == 2 * direction and coords[f"{e[0]}{ey + (-1 * direction)}"] == empty:
                            playable.append(s+e)
                        #capture
                        if coords[e] != empty and abs(dx) == 1 and (dy) == 1 * direction:
                            playable.append(s+e)
                        #en passant
                        if coords[e] == empty and ((sy == 5 and turn == 1) or (sy == 4 and turn == 2)) and abs(dx) == 1 and (dy) == 1 * direction:
                            if last_move != "None":
                                epcord = f"{e[0]}{ey + (-1 * direction)}"
                                piece_underneath = coords[epcord]
                                last_moved_piece = last_move[0]
                                if piece_underneath in opponent_pieces and piece_underneath[1:] == "pawn":
                                    last_move_stc = last_move[1][:2]
                                    last_move_edc = last_move[1][2:4]
                                    last_move_dy = int(last_move_edc[1]) - int(last_move_stc[1]) 
                                    if piece_underneath == last_moved_piece and epcord == last_move_edc and abs(last_move_dy) == 2:
                                        playable.append(s+e + "(enp:" + epcord + ")") 
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
    playable = list(dict.fromkeys(playable)) #remove duplicates
    viable = []
    for move in playable:
        #save previous state
        stc_p = coords[move[:2]]
        edc_p = coords[move[2:4]]
        #check if move escapes check
        piece = stc_p
        ghost_move(move)
        check = check_check()
        if check == 0:
            viable.append(move)
        #revert move
        if "(" in move and ")" in move:
            revert()
        else:
            coords[move[:2]] = stc_p
            coords[move[2:4]] = edc_p
    return viable

#after turn reset
def afterturn_reset():
    global check, capture, checkmate, stalemate, promotion
    check = 0
    capture = 0
    checkmate = 0
    stalemate = 0 
    promotion = 0

def enpassant(move):
    global coords
    stc = move[:2]
    edc = move[2:4]

    i = move.index(":") + 1
    captured_pawn = move[i:i+2]

    coords[stc] = empty
    coords[captured_pawn] = empty
    if turn == 1:
        coords[edc] = wpawn
    else:
        coords[edc] = bpawn

def castle(move):
    global coords
    stc = move[:2]
    coords[stc] = empty 
    if turn == 1:
        if "(O-O-O)" in move:
            coords["a1"] = empty
            coords["c1"] = wking
            coords["d1"] = wrook 
        if "(O-O)" in move:
            coords["h1"] = empty
            coords["g1"] = wking
            coords["f1"] = wrook
    else:
        if "(O-O-O)" in move:
            coords["a8"] = empty
            coords["c8"] = bking
            coords["d8"] = brook
        if "(O-O)" in move:
            coords["h8"] = empty
            coords["g8"] = bking
            coords["f8"] = brook

#move functions
def play_move(move, promoted_to=None):
    stc = move[:2]
    edc = move[2:4]
    piece = coords[stc]
    if piece[1:] == "king":
        king_moved[turn] = "1"
    promotion = promotion_check(stc, edc)
    if promotion == 1:
        color = piece[0]
        new_piece = color + promoted_to
        coords[edc] =  new_piece
        coords[stc] = empty
    else:
        ghost_move(move)
    global last_move
    last_move = [piece, move]

def ghost_move(move):
    stc = move[:2]
    edc = move[2:4]
    piece = coords[stc]
    if "(" in move and ")" in move:
        if "O" in move:
            castle(move)
        if "enp" in move:
            enpassant(move)
    else:
        coords[edc] = piece
        coords[stc] = empty   

def revert():
    global coords
    file = f"move{moves}.txt"
    coords = load_data(current_folder, file)

def undo_move():
    global coords
    file = f"move{moves-1}.txt"
    try:
        coords = load_data(current_folder, file)
        file = f"move{moves+1}.txt"
        file_exists = 1
    except:
        file_exists = 0
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