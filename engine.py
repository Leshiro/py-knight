#imports
import os

#folder names
save_folder = "saves"
current_folder = "current"

#create saves folder
cwd = os.getcwd()
print(f"\n{cwd}")
save_path = rf"{cwd}\{save_folder}"
if not os.path.exists(save_path):
    os.makedirs(save_path)

#colors
reset = u"\u001b[0m"
red = u"\u001b[31;1m"
blue = u"\u001b[34;1m"
green = u"\u001b[32;1m"
magenta = u"\u001b[35;1m"
yellow = u"\u001b[33;1m"
white = u"\u001b[37;1m"
black = u"\u001b[30;1m"

#background colors
tile1 = u"\u001b[47;1m" #white
tile2 = u"\u001b[40;1m" #black

#assign colors
default_color = green
highlight_color = magenta
board_color = white
white_color = blue
black_color = red

#pieces
empty = f"{board_color} {default_color}"

wpawn = f"{white_color}♙{default_color}"
wrook = f"{white_color}♖{default_color}"
wknight = f"{white_color}♘{default_color}"
wbishop = f"{white_color}♗{default_color}"
wqueen = f"{white_color}♕{default_color}"
wking = f"{white_color}♔{default_color}"

bpawn = f"{black_color}♙{default_color}"
brook = f"{black_color}♖{default_color}"
bknight = f"{black_color}♘{default_color}"
bbishop = f"{black_color}♗{default_color}"
bqueen = f"{black_color}♕{default_color}"
bking = f"{black_color}♔{default_color}"

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
        "next": 2
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

#game info
def game_info():
    print(f"""{highlight_color}\nCHESS {default_color}in {highlight_color}TERMINAL{default_color}\n\nHOW TO PLAY\n
Moves should be 4 characters. (2 coordinates)
The first two characters should be the coordinate of the piece you want to move.
The last two characters should be the coordinate that you want to move the piece to.
Example: {highlight_color}e2e4{default_color}\n
Enter {highlight_color}exit{default_color} to exit or {highlight_color}restart{default_color} to restart.
Enter {highlight_color}save{default_color} to save the game state.
Enter {highlight_color}undo{default_color} to undo move.""")

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

#invalid move msgs
def proper_form():
    print(f"\nPlease enter a move in proper form. \nExample: {highlight_color}e2e4{default_color}\n")     
def not_viable():
    print(f"\n{highlight_color}{move}{default_color} is not a viable move.\n")    
def no_piece():
    print(f"\nYou do not have a piece in [{start_coord}].\n")

#collision checks
def diagonal_collision_check(s, e):
    collisions = 0
    if horizontal_change > 0 and vertical_change > 0: #direction 1
        for n in range(change):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])+n]}{coords_ver[coords_ver.index(s[1])+n]}"]
            if check_collision != empty:
                collisions = collisions + 1
    if horizontal_change < 0 and vertical_change > 0: #direction 2
        for n in range(change):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])-n]}{coords_ver[coords_ver.index(s[1])+n]}"]
            if check_collision != empty:
                collisions = collisions + 1
    if horizontal_change < 0 and vertical_change < 0: #direction 3
        for n in range(change):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])-n]}{coords_ver[coords_ver.index(s[1])-n]}"]
            if check_collision != empty:
                collisions = collisions + 1    
    if horizontal_change > 0 and vertical_change < 0: #direction 4
        for n in range(change):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])+n]}{coords_ver[coords_ver.index(s[1])-n]}"]
            if check_collision != empty:
                collisions = collisions + 1
    return collisions
def collision_check(s, e):
    collisions = 0
    if horizontal_change > 0:
        for n in range(abs(horizontal_change)):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])+n]}{s[1]}"]
            if check_collision != empty:
                collisions = collisions + 1
    if horizontal_change < 0:
        for n in range(abs(horizontal_change)):
            check_collision = coords[f"{coords_hor[coords_hor.index(s[0])-n]}{s[1]}"]
            if check_collision != empty:
                collisions = collisions + 1  
    if vertical_change > 0:                      
        for n in range(abs(vertical_change)):
            check_collision = coords[f"{s[0]}{coords_ver[coords_ver.index(s[1])+n]}"]
            if check_collision != empty:
                collisions = collisions + 1
    if vertical_change < 0:                      
        for n in range(abs(vertical_change)):
            check_collision = coords[f"{s[0]}{coords_ver[coords_ver.index(s[1])-n]}"]
            if check_collision != empty:
                collisions = collisions + 1  
    return collisions

#move functions
def play_move(move):
    stc = move[:2]
    edc = move[2:]
    global previous1, previous2, captured_piece_name
    previous1 = coords[stc]
    previous2 = coords[edc]
    capture = capture_check(edc)
    promotion = promotion_check(stc, edc)
    if capture == 1:
        i = pieces.index(coords[end_coord])
        captured_piece_name = piece_values[i][1:].capitalize()
    if promotion == 0:
        coords[edc] = piece
    if promotion == 1:
        coords[edc] = new_piece    
    coords[stc] = empty      
def ghost_move(move):
    stc = move[:2]
    edc = move[2:]
    global previous1, previous2
    previous1 = coords[stc]
    previous2 = coords[edc]
    coords[edc] = piece
    coords[stc] = empty

#prints
def show_board():
    print(f"""{default_color}
        ────────────────
    8 | {tile1}{coords['a8']} {tile2}{coords['b8']} {tile1}{coords['c8']} {tile2}{coords['d8']} {tile1}{coords['e8']} {tile2}{coords['f8']} {tile1}{coords['g8']} {tile2}{coords['h8']} {reset}{default_color} |
    7 | {tile2}{coords['a7']} {tile1}{coords['b7']} {tile2}{coords['c7']} {tile1}{coords['d7']} {tile2}{coords['e7']} {tile1}{coords['f7']} {tile2}{coords['g7']} {tile1}{coords['h7']} {reset}{default_color} |
    6 | {tile1}{coords['a6']} {tile2}{coords['b6']} {tile1}{coords['c6']} {tile2}{coords['d6']} {tile1}{coords['e6']} {tile2}{coords['f6']} {tile1}{coords['g6']} {tile2}{coords['h6']} {reset}{default_color} |
    5 | {tile2}{coords['a5']} {tile1}{coords['b5']} {tile2}{coords['c5']} {tile1}{coords['d5']} {tile2}{coords['e5']} {tile1}{coords['f5']} {tile2}{coords['g5']} {tile1}{coords['h5']} {reset}{default_color} |
    4 | {tile1}{coords['a4']} {tile2}{coords['b4']} {tile1}{coords['c4']} {tile2}{coords['d4']} {tile1}{coords['e4']} {tile2}{coords['f4']} {tile1}{coords['g4']} {tile2}{coords['h4']} {reset}{default_color} |
    3 | {tile2}{coords['a3']} {tile1}{coords['b3']} {tile2}{coords['c3']} {tile1}{coords['d3']} {tile2}{coords['e3']} {tile1}{coords['f3']} {tile2}{coords['g3']} {tile1}{coords['h3']} {reset}{default_color} |
    2 | {tile1}{coords['a2']} {tile2}{coords['b2']} {tile1}{coords['c2']} {tile2}{coords['d2']} {tile1}{coords['e2']} {tile2}{coords['f2']} {tile1}{coords['g2']} {tile2}{coords['h2']} {reset}{default_color} |
    1 | {tile2}{coords['a1']} {tile1}{coords['b1']} {tile2}{coords['c1']} {tile1}{coords['d1']} {tile2}{coords['e1']} {tile1}{coords['f1']} {tile2}{coords['g1']} {tile1}{coords['h1']} {reset}{default_color} |
        ────────────────
        A B C D E F G H{default_color}\n""")
def move_summary():
    if capture == 0: 
        print(f"- {player} plays [{piece_name}] to [{end_coord}].\n")
    elif capture == 1:
        print(f"- {player} plays [{piece_name}] to [{end_coord}] and captures the [{captured_piece_name}]!\n")
    if promotion == 1: 
        print(f"- The {player} [{piece_name}] has been promoted to [{chosen_piece.capitalize()}]!\n")           

#after turn reset
def afterturn_reset():
    global check, capture, checkmate, stalemate, promotion
    check = 0
    capture = 0
    checkmate = 0
    stalemate = 0 
    promotion = 0  

#checks
def capture_check(end_coord):  
    global capture  
    if coords[end_coord] != empty:
        capture = 1
    else:
        capture = 0
    return capture
def promotion_check(start_coord, end_coord):
    global chosen_piece, new_piece
    promotion = 0
    if (coords[start_coord] == wpawn and end_coord[1] == "8") or (coords[start_coord] == bpawn and end_coord[1] == "1"):
        promotion = 1
        chosen_piece = input("Promote [Pawn] to: ")
        chosen_piece = chosen_piece.lower()
        while chosen_piece != "queen" and chosen_piece != "bishop" and chosen_piece != "rook" and chosen_piece != "knight":
            chosen_piece = input("Please enter a valid piece name (queen/rook/bishop/knight): ").strip().lower()
        if coords[start_coord] == wpawn:
            color = "w"
        if coords[start_coord] == bpawn:
            color = "b"
        i = piece_values.index(color + chosen_piece)
        new_piece = pieces[i]
    return promotion
def check_check(print_msg):
    global horizontal_change, vertical_change, change

    #get king coordinate
    for i in coords:
        if coords[i] == own_pieces[0]:
            king_cd = i
            break

    #get covered cds
    covered_cds = []
    for s in coords:
        piece = coords[s]
        if piece != empty:
            for e in coords:
                if s != e and e not in covered_cds:
                    if piece == opponent_pieces[0]: #king
                        if abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) <= 1 and abs(coords_ver.index(s[1]) - coords_ver.index(e[1])) <= 1:
                            if coords[e] not in opponent_pieces:
                                covered_cds.append(e)
                    if piece == opponent_pieces[1]: #bishop
                        horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                        vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                        if abs(horizontal_change) == abs(vertical_change):
                            change = abs(horizontal_change)
                            collisions = diagonal_collision_check(s, e)
                            if collisions <= 1:
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)
                    if piece == opponent_pieces[2]: #pawn
                        if (coords_ver.index(e[1]) - coords_ver.index(s[1])) == 1 * -1 * direction and abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) == 1:
                            if coords[e] not in opponent_pieces:
                                covered_cds.append(e)
                    if piece == opponent_pieces[3]: #knight
                        if abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) == 1 and abs(coords_ver.index(s[1]) - coords_ver.index(e[1])) == 2:
                            covered_cds.append(e)
                        elif abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) == 2 and abs(coords_ver.index(s[1]) - coords_ver.index(e[1])) == 1:    
                            covered_cds.append(e)
                    if piece == opponent_pieces[4]: #rook
                        if s[0] == e[0] or s[1] == e[1]:
                            horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                            vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                            collisions = collision_check(s, e)  
                            if collisions <= 1:
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)
                    if piece == opponent_pieces[5]: #queen
                        horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                        vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                        if s[0] == e[0] or s[1] == e[1]:
                            collisions = collision_check(s, e)  
                            if collisions <= 1:
                                if coords[e] not in opponent_pieces:
                                    covered_cds.append(e)
                        elif abs(horizontal_change) == abs(vertical_change):
                            change = abs(horizontal_change)
                            collisions = diagonal_collision_check(s, e)
                            if collisions <= 1:        
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
def find_viable_moves():
    global horizontal_change, vertical_change, change, piece
    #find playable moves
    playable = []
    for s in coords:
        piece = coords[s]
        if piece in own_pieces:
            for e in coords:
                if s != e and e not in playable and coords[e] not in own_pieces:
                    if piece == own_pieces[0]: #king
                        if abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) <= 1 and abs(coords_ver.index(s[1]) - coords_ver.index(e[1])) <= 1:
                            playable.append(s+e)
                    if piece == own_pieces[1]: #bishop
                        horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                        vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                        if abs(horizontal_change) == abs(vertical_change):
                            change = abs(horizontal_change)
                            collisions = diagonal_collision_check(s, e)
                            if collisions <= 1:
                                playable.append(s+e)
                    if piece == own_pieces[2]: #pawn
                        if coords[e] == empty and s[0] == e[0] and (coords_ver.index(e[1]) - coords_ver.index(s[1])) == 1 * direction:
                            playable.append(s+e)
                        if coords[e] == empty and s[0] == e[0] and coords_ver.index(s[1]) == 4.5 - (2.5 * direction) and (coords_ver.index(e[1]) - coords_ver.index(s[1])) == 2 * direction and coords[f"{e[0]}{int(e[1]) + (-1 * direction)}"] == empty:
                            playable.append(s+e)
                        if (coords_ver.index(e[1]) - coords_ver.index(s[1])) == 1 * direction and abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) == 1 and coords[e] != empty:
                            playable.append(s+e) 
                    if piece == own_pieces[3]: #knight
                        if abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) == 1 and abs(coords_ver.index(s[1]) - coords_ver.index(e[1])) == 2:
                            playable.append(s+e)
                        elif abs(coords_hor.index(s[0]) - coords_hor.index(e[0])) == 2 and abs(coords_ver.index(s[1]) - coords_ver.index(e[1])) == 1:    
                            playable.append(s+e)
                    if piece == own_pieces[4]: #rook
                        if s[0] == e[0] or s[1] == e[1]:
                            horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                            vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                            collisions = collision_check(s, e)  
                            if collisions <= 1:
                                playable.append(s+e)
                    if piece == own_pieces[5]: #queen
                        horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                        vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                        if s[0] == e[0] or s[1] == e[1]:
                            collisions = collision_check(s, e)  
                            if collisions <= 1:
                                playable.append(s+e)
                        elif abs(horizontal_change) == abs(vertical_change):
                            change = abs(horizontal_change)
                            collisions = diagonal_collision_check(s, e)
                            if collisions <= 1:        
                                playable.append(s+e)  
    viable = []
    for move in playable:
        #save previous state
        stc_p = coords[move[:2]]
        edc_p = coords[move[2:]]
        #check if move escapes check
        piece = stc_p
        ghost_move(move)
        check = check_check(0)
        if check == 0:
            viable.append(move)
        #revert move
        coords[move[:2]] = stc_p
        coords[move[2:]] = edc_p
    return viable

#game operations
def save_game():
    saved = 0
    while saved == 0:
        file_name = input("\nSave file name: ")
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
                print(f"""\nGame state successfully saved to [{file_name}.txt]. You can enter {highlight_color}exit{default_color} to exit.\n""")
        except FileExistsError:
            print(f"\n[{file_name}.txt] already exists, please enter another name.")
            continue  
def quit_game():
    print("")
    exit()
def restart_game():
    print("\nRestarting...")
    game()                  
def save_current_state():
    with open(rf"{current_folder}\move{moves}.txt", "x") as file:
        file.write(f"turn={turn}\nmoves={moves}")
        for coord in coords:
            coord_piece = coords[coord]
            i = pieces.index(coord_piece)
            piece_name = piece_values[i]
            line = coord + "=" + piece_name
            file.write(f"\n{line}")

#move flow
def move_flow():
    global move, turn, moves, piece, player, direction, own_pieces, opponent_pieces
    global horizontal_change, vertical_change, change, start_coord, end_coord, piece_name
    #load turn data
    player_data = PlayerData[turn]
    player = player_data["name"]
    opponent = player_data["opponent"]
    own_pieces = player_data["pieces"]
    opponent_pieces = player_data["opponent_pieces"]
    direction = player_data["direction"]

    #check if there's a check
    check = check_check(1)

    #checkmate / stalemate
    viable_moves = find_viable_moves()
    if len(viable_moves) == 0:
        if check == 0:
            print(f"It's a stalemate! [{player}] has no moves to play.\n") 
        elif check == 1:
            print(f"Checkmate! [{opponent}] wins the game.\n")
        choice = input("Do you want to play again? (yes/no): ").lower().strip()
        if choice == "yes":
            restart_game()
        if choice == "no":
            quit_game()
        else:
            quit_game()

    #move string
    move = str(input(f"{moves+1}) {player}'s turn: "))
    move = move.lower()

    #operation commands
    if move == "save":
        save_game()
        return
    if move == "quit" or move == "exit":
        quit_game()
        return
    if move == "restart":
        restart_game()
        return
    if move == "undo":
        file_exists = 0
        for file in os.listdir(current_game_path):
            if file == f"move{moves-1}.txt":
                file_exists = 1
                load_data(current_folder, file)
                show_board()
                break
        if file_exists == 0:
            print("\nPrevious game state does not exist.\n")
        else:
            file = f"move{moves+1}.txt"
            file_path = os.path.join(current_game_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return
    if move == "viable":
        viable_string = ""
        for i in range(len(viable_moves)):
            if i + 1 == len(viable_moves):
                viable_string = viable_string + (f"{highlight_color}{viable_moves[i]}{default_color}.")
            else:
                viable_string = viable_string + (f"{highlight_color}{viable_moves[i]}{default_color}, ")
        print(f"\nViable moves are;\n{viable_string}\n")
        return

    #check for validity
    if len(move) != 4:
        proper_form()
        return
    start_coord = f"{move[0]}{move[1]}"
    end_coord = f"{move[2]}{move[3]}"

    if start_coord == end_coord:
        not_viable()
        return
    if start_coord in coords:
        piece = coords[start_coord]
    else:
        proper_form()
        return
    if piece not in own_pieces:
        no_piece()
        return
    if end_coord in coords:
        end_coord_piece = coords[end_coord]
        if end_coord_piece in own_pieces:
            not_viable()
            return
        
        #piece rules
        else:
            #king rules
            if piece == wking or piece == bking:
                piece_name = "King"
                if abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) <= 1 and abs(coords_ver.index(start_coord[1]) - coords_ver.index(end_coord[1])) <= 1:
                    play_move(move)
                else:
                    not_viable()
                    return

            #bishop rules
            if piece == wbishop or piece == bbishop:
                piece_name = "Bishop"
                horizontal_change = coords_hor.index(end_coord[0]) - coords_hor.index(start_coord[0])
                vertical_change = coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])
                if abs(horizontal_change) == abs(vertical_change):
                    change = abs(horizontal_change)
                    collisions = diagonal_collision_check(start_coord, end_coord)
                    if collisions <= 1:        
                        play_move(move)
                    else:
                        not_viable() 
                        return  
                else:
                    not_viable()
                    return 
            #pawn rules
            if piece == wpawn or piece == bpawn:
                piece_name = "Pawn"
                if coords[end_coord] == empty and start_coord[0] == end_coord[0] and (coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])) == 1 * direction:
                    play_move(move)
                elif coords[end_coord] == empty and start_coord[0] == end_coord[0] and coords_ver.index(start_coord[1]) == 4.5 - (2.5 * direction) and (coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])) == 2 * direction and coords[f"{end_coord[0]}{int(end_coord[1]) + (-1 * direction)}"] == empty:
                    play_move(move)
                elif (coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])) == 1 * direction and abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) == 1 and coords[end_coord] != empty:
                    play_move(move)   
                else:
                    not_viable()
                    return  
            #knight rules
            if piece == wknight or piece == bknight:
                piece_name = "Knight"
                if abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) == 1 and abs(coords_ver.index(start_coord[1]) - coords_ver.index(end_coord[1])) == 2:
                    play_move(move)
                elif abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) == 2 and abs(coords_ver.index(start_coord[1]) - coords_ver.index(end_coord[1])) == 1:    
                    play_move(move)
                else:
                    not_viable()
                    return
            #rook rules    
            if piece == wrook or piece == brook:  
                piece_name = "Rook"
                if start_coord[0] == end_coord[0] or start_coord[1] == end_coord[1]:
                    horizontal_change = coords_hor.index(end_coord[0]) - coords_hor.index(start_coord[0])
                    vertical_change = coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])
                    collisions = collision_check(start_coord, end_coord)  
                    if collisions <= 1:
                        play_move(move)
                    else:
                        not_viable()
                        return    
                else:
                    not_viable()
                    return    
            #queen rules
            if piece == wqueen or piece == bqueen:
                piece_name = "Queen"
                horizontal_change = coords_hor.index(end_coord[0]) - coords_hor.index(start_coord[0])
                vertical_change = coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])
                if start_coord[0] == end_coord[0] or start_coord[1] == end_coord[1]:
                    collisions = collision_check(start_coord, end_coord)  
                    if collisions <= 1:
                        play_move(move)
                    else:
                        not_viable()
                        return
                elif abs(horizontal_change) == abs(vertical_change):
                    change = abs(horizontal_change)
                    collisions = diagonal_collision_check(start_coord, end_coord)
                    if collisions <= 1:        
                        play_move(move)
                    else:
                        not_viable()   
                        return
                else:
                    not_viable()
                    return    
    else: 
        proper_form()
        return

    #check if move escapes check, otherwise revert
    check = check_check(0)
    if check == 1:
        coords[start_coord] = previous1
        coords[end_coord] = previous2
        not_viable()
        return

    moves = moves + 1
    save_current_state()
    show_board()
    move_summary()
    afterturn_reset()
    turn = PlayerData[turn]["next"]

#game
def game():
    #create current folder if doesnt exist
    if not os.path.exists(current_folder):
        os.makedirs(current_folder)

    #clear current folder
    global current_game_path
    current_game_path = rf"{cwd}\{current_folder}"
    for file in os.listdir(current_game_path):
        file_path = os.path.join(current_game_path, file)
        if os.path.isfile(file_path) and file[:4] == "move":
            os.remove(file_path)

    #ask for game data    
    save_file = input("\nPress ENTER to start or enter save file name: ")
    save_file = save_file.lower().strip()
    if save_file[-4:] != ".txt":
        save_file = save_file + ".txt"

    #load game data
    global coords, moves, turn
    default_coords = load_data("saves", "default.txt")
    try: 
        coords = load_data(save_folder, save_file)
        if coords != default_coords:
            print(f"\n[{save_file}] LOADED SUCCESSFULLY, STARTING GAME...")
    except FileNotFoundError:
        if save_file != ".txt":   
            print("\nGAME STATE FILE COULD NOT BE FOUND, STARTING DEFAULT GAME...")
        coords = default_coords
        turn = 1
        moves = 0
    except:
        print("\nGAME STATE FILE IS CORRUPTED, STARTING DEFAULT GAME...")
        coords = default_coords
        turn = 1
        moves = 0
    
    #reset variables & show the board
    afterturn_reset()
    show_board()
    save_current_state()

    #move flow
    while True:
        move_flow()

#run
game_info()
game()      