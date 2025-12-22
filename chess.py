#folder names
save_folder_name = "saves"
current_folder_name = "current"

#create saves folder
import os
cwd = os.getcwd()
print(f"\n{cwd}")
save_path = rf"{cwd}\{save_folder_name}"
if not os.path.exists(save_path):
    os.makedirs(save_path)

#reset color
reset = u"\u001b[0m"

#foreground colors
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

#pieces and their colors
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

#default game coords
default_coords = {
    "a1" : wrook,
    "b1" : wknight,
    "c1" : wbishop,
    "d1" : wqueen,
    "e1" : wking,
    "f1" : wbishop,
    "g1" : wknight,
    "h1" : wrook,

    "a2" : wpawn,
    "b2" : wpawn,
    "c2" : wpawn,
    "d2" : wpawn,
    "e2" : wpawn,
    "f2" : wpawn,
    "g2" : wpawn,
    "h2" : wpawn,

    "a3" : empty,
    "b3" : empty,
    "c3" : empty,
    "d3" : empty,
    "e3" : empty,
    "f3" : empty,
    "g3" : empty,
    "h3" : empty,

    "a4" : empty,
    "b4" : empty,
    "c4" : empty,
    "d4" : empty,
    "e4" : empty,
    "f4" : empty,
    "g4" : empty,
    "h4" : empty, 

    "a5" : empty,
    "b5" : empty,
    "c5" : empty,
    "d5" : empty,
    "e5" : empty,
    "f5" : empty,
    "g5" : empty,
    "h5" : empty,   

    "a6" : empty,
    "b6" : empty,
    "c6" : empty,
    "d6" : empty,
    "e6" : empty,
    "f6" : empty,
    "g6" : empty,
    "h6" : empty,    
               
    "a7" : bpawn,
    "b7" : bpawn,
    "c7" : bpawn,
    "d7" : bpawn,
    "e7" : bpawn,
    "f7" : bpawn,
    "g7" : bpawn,
    "h7" : bpawn,

    "a8" : brook,
    "b8" : bknight,
    "c8" : bbishop,
    "d8" : bqueen,
    "e8" : bking,
    "f8" : bbishop,
    "g8" : bknight,
    "h8" : brook,           
}

coords_hor = ["0","a", "b", "c", "d", "e", "f", "g", "h"]
coords_ver = ["0","1", "2", "3", "4", "5", "6", "7", "8"]

TURN_DATA = {
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

#game start functions
def game_info():
    print(f"""{highlight_color}\nCHESS {default_color}in {highlight_color}TERMINAL{default_color}\n\nHOW TO PLAY\n
Moves should be 4 characters. (2 coordinates)
The first two characters should be the coordinate of the piece you want to move.
The last two characters should be the coordinate that you want to move the piece to.
Example: {highlight_color}e2e4{default_color}\n
Enter {highlight_color}exit{default_color} to exit or {highlight_color}restart{default_color} to restart.
Enter {highlight_color}save{default_color} to save the game state.
Enter {highlight_color}undo{default_color} to undo move.""")
    
def reset_everything():
    global turn, moves, collisions, piece, new_piece
    turn = 1
    moves = 0
    collisions = 0
    piece = ""
    new_piece = ""

def game():
    #create current folder if doesnt exist
    if not os.path.exists(current_folder_name):
        os.makedirs(current_folder_name)

    #clear current folder
    current_game_path = rf"{cwd}\{current_folder_name}"
    for file in os.listdir(current_game_path):
        file_path = os.path.join(current_game_path, file)
        if os.path.isfile(file_path) and file[:4] == "move":
            os.remove(file_path)

    #important global variables
    global turn, moves, coords

    #ask for game data    
    game_state_file = input("\nPress ENTER to start or enter save file name: ")
    game_state_file = game_state_file.lower().strip()

    if game_state_file[-4:] != ".txt":
        game_state_file = game_state_file + ".txt"

    #loader
    def load_data(folder, file):
        global coords, moves, turn
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
                if coord == "empty":
                    coords_list[n] = empty
                if coord == "wrook":
                    coords_list[n] = wrook
                if coord == "wknight":
                    coords_list[n] = wknight
                if coord == "wbishop":
                    coords_list[n] = wbishop
                if coord == "wqueen":
                    coords_list[n] = wqueen
                if coord == "wking":
                    coords_list[n] = wking
                if coord == "wpawn":
                    coords_list[n] = wpawn 
                if coord == "brook":
                    coords_list[n] = brook
                if coord == "bknight":
                    coords_list[n] = bknight
                if coord == "bbishop":
                    coords_list[n] = bbishop
                if coord == "bqueen":
                    coords_list[n] = bqueen
                if coord == "bking":
                    coords_list[n] = bking
                if coord == "bpawn":
                    coords_list[n] = bpawn                                 
            coords_list.insert(0, "GROUND ZERO")

        coords = {
        "a1" : coords_list[1],
        "b1" : coords_list[2],
        "c1" : coords_list[3],
        "d1" : coords_list[4],
        "e1" : coords_list[5],
        "f1" : coords_list[6],
        "g1" : coords_list[7],
        "h1" : coords_list[8],

        "a2" : coords_list[9],
        "b2" : coords_list[10],
        "c2" : coords_list[11],
        "d2" : coords_list[12],
        "e2" : coords_list[13],
        "f2" : coords_list[14],
        "g2" : coords_list[15],
        "h2" : coords_list[16],

        "a3" : coords_list[17],
        "b3" : coords_list[18],
        "c3" : coords_list[19],
        "d3" : coords_list[20],
        "e3" : coords_list[21],
        "f3" : coords_list[22],
        "g3" : coords_list[23],
        "h3" : coords_list[24],

        "a4" : coords_list[25],
        "b4" : coords_list[26],
        "c4" : coords_list[27],
        "d4" : coords_list[28],
        "e4" : coords_list[29],
        "f4" : coords_list[30],
        "g4" : coords_list[31],
        "h4" : coords_list[32], 

        "a5" : coords_list[33],
        "b5" : coords_list[34],
        "c5" : coords_list[35],
        "d5" : coords_list[36],
        "e5" : coords_list[37],
        "f5" : coords_list[38],
        "g5" : coords_list[39],
        "h5" : coords_list[40],   

        "a6" : coords_list[41],
        "b6" : coords_list[42],
        "c6" : coords_list[43],
        "d6" : coords_list[44],
        "e6" : coords_list[45],
        "f6" : coords_list[46],
        "g6" : coords_list[47],
        "h6" : coords_list[48],    
                
        "a7" : coords_list[49],
        "b7" : coords_list[50],
        "c7" : coords_list[51],
        "d7" : coords_list[52],
        "e7" : coords_list[53],
        "f7" : coords_list[54],
        "g7" : coords_list[55],
        "h7" : coords_list[56],

        "a8" : coords_list[57],
        "b8" : coords_list[58],
        "c8" : coords_list[59],
        "d8" : coords_list[60],
        "e8" : coords_list[61],
        "f8" : coords_list[62],
        "g8" : coords_list[63],
        "h8" : coords_list[64],           
    }

    #load game data
    try: 
        load_data(save_folder_name, game_state_file)
        if coords != default_coords:
            print(f"\n[{game_state_file}] LOADED SUCCESSFULLY, STARTING GAME...")
    except FileNotFoundError:
        if game_state_file != ".txt":   
            print("\nGAME STATE FILE COULD NOT BE FOUND, STARTING DEFAULT GAME...")
        coords = default_coords
        turn = 1
        moves = 0
    except:
        print("\nGAME STATE FILE IS CORRUPTED, STARTING DEFAULT GAME...")
        coords = default_coords
        turn = 1
        moves = 0

    #show board
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

    #invalid move msgs
    def proper_form():
        print(f"\nPlease enter a move in proper form. \nExample: {highlight_color}a1b1{default_color}\n")     
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

    #handle move
    def play_move():
        global moves, previous1, previous2
        previous1 = coords[start_coord]
        previous2 = coords[end_coord]
        coords[start_coord] = empty
        capture = 0
        promotion = 0
        capture_check()
        promotion_check()
        if capture == 1:
            get_captured_piece_name()
        if promotion == 0:
            coords[end_coord] = piece
        if promotion == 1:
            coords[end_coord] = new_piece          

    def move_summary():
        if capture == 0: 
            print(f"- {player} plays [{piece_name}] to [{end_coord}].\n")
        elif capture == 1:
            print(f"- {player} plays [{piece_name}] to [{end_coord}] and captures the [{captured_piece_name}]!\n")
        if promotion == 1: 
            print(f"- The {player} [{piece_name}] has been promoted to [{chosen_piece}]!\n")           

    #get piece names
    def get_captured_piece_name():
        global captured_piece_name
        if coords[end_coord] == wpawn or coords[end_coord] == bpawn:
            captured_piece_name = "Pawn"
        if coords[end_coord] == wrook or coords[end_coord] == brook:
            captured_piece_name = "Rook"
        if coords[end_coord] == wknight or coords[end_coord] == bknight:
            captured_piece_name = "Knight"
        if coords[end_coord] == wbishop or coords[end_coord] == bbishop:
            captured_piece_name = "Bishop"
        if coords[end_coord] == wqueen or coords[end_coord] == bqueen:
            captured_piece_name = "Queen" 
        if coords[end_coord] == wking or coords[end_coord] == bking:
            captured_piece_name = "King" 
        return captured_piece_name         
    def get_chosen_piece_white():
        global new_piece
        if chosen_piece == "queen":
            new_piece = wqueen
        if chosen_piece == "rook":
            new_piece = wrook
        if chosen_piece == "bishop":
            new_piece = wbishop
        if chosen_piece == "knight":
            new_piece = wknight
    def get_chosen_piece_black():
        global new_piece
        if chosen_piece == "queen":
            new_piece = bqueen
        if chosen_piece == "rook":
            new_piece = brook
        if chosen_piece == "bishop":
            new_piece = bbishop
        if chosen_piece == "knight":
            new_piece = bknight   

    #save game state
    def save_game_state():
        with open(rf"{current_folder_name}\move{moves}.txt", "x") as file:
            file.write(f"turn={turn}\nmoves={moves}")
            for coord in coords:
                coord_piece = coords[coord]
                if coord_piece == empty:
                    piece_name = "empty"
                if coord_piece == wrook:
                    piece_name = "wrook"
                if coord_piece == wknight:
                    piece_name = "wknight"
                if coord_piece == wbishop:
                    piece_name = "wbishop"
                if coord_piece == wqueen:
                    piece_name = "wqueen"
                if coord_piece == wking:
                    piece_name = "wking"
                if coord_piece == wpawn:
                    piece_name = "wpawn" 
                if coord_piece == brook:
                    piece_name = "brook"
                if coord_piece == bknight:
                    piece_name = "bknight"
                if coord_piece == bbishop:
                    piece_name = "bbishop"
                if coord_piece == bqueen:
                    piece_name = "bqueen"
                if coord_piece == bking:
                    piece_name = "bking"
                if coord_piece == bpawn:
                    piece_name = "bpawn"
                line = coord + "=" + piece_name
                file.write(f"\n{line}")

    #capture check
    def capture_check():  
        global capture  
        if coords[end_coord] != empty:
            capture = 1

    #promotion check
    def promotion_check():
        global promotion, chosen_piece
        if coords[start_coord] == wpawn and end_coord[1] == "8":
            promotion = 1
            chosen_piece = input("Promote [Pawn] to: ")
            chosen_piece = chosen_piece.lower()
            while chosen_piece != "queen" and chosen_piece != "bishop" and chosen_piece != "rook" and chosen_piece != "knight":
                chosen_piece = input("Please enter a valid piece name (queen/rook/bishop/knight): ")
                chosen_piece = chosen_piece.lower()
            get_chosen_piece_white()
            chosen_piece = chosen_piece.capitalize()  
        if coords[start_coord] == bpawn and end_coord[1] == "1":
            promotion = 1
            chosen_piece = input("Promote [Pawn] to: ")
            chosen_piece = chosen_piece.lower()
            while chosen_piece != "queen" and chosen_piece != "bishop" and chosen_piece != "rook" and chosen_piece != "knight":
                chosen_piece = input("Please enter a valid piece name (queen/rook/bishop/knight): ")
                chosen_piece = chosen_piece.lower()
            get_chosen_piece_black() 
            chosen_piece = chosen_piece.capitalize()     

    #check for check
    def check_check():
        global collisions, piece
        nonlocal horizontal_change, vertical_change, change

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
                                collisions = 0
                                diagonal_collision_check(s, e)
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
                                collisions = 0
                                collision_check(s, e)  
                                if collisions <= 1:
                                    if coords[e] not in opponent_pieces:
                                        covered_cds.append(e)
                        if piece == opponent_pieces[5]: #queen
                            horizontal_change = coords_hor.index(e[0]) - coords_hor.index(s[0])
                            vertical_change = coords_ver.index(e[1]) - coords_ver.index(s[1])
                            if s[0] == e[0] or s[1] == e[1]:
                                collisions = 0
                                collision_check(s, e)  
                                if collisions <= 1:
                                    if coords[e] not in opponent_pieces:
                                        covered_cds.append(e)
                            elif abs(horizontal_change) == abs(vertical_change):
                                change = abs(horizontal_change)
                                collisions = 0
                                diagonal_collision_check(s, e)
                                if collisions <= 1:        
                                    if coords[e] not in opponent_pieces:
                                        covered_cds.append(e)    

        #check detection
        global check
        check = 0
        if king_cd in covered_cds:
            check = 1
            if first_time == 1:
                print(f"The {player} [King] is in check!")
        else:
            check = 0
        return check

    #reset checks, captures, promotions
    def reset_afterturnchecks():
        global check, capture, checkmate, stalemate, promotion
        check = 0
        capture = 0
        checkmate = 0
        stalemate = 0 
        promotion = 0  

    #game operations
    def save_game():
        saved = 0
        while saved == 0:
            file_name = input("\nSave file name: ")
            try:
                with open(rf"{save_folder_name}\{file_name}.txt", "x") as file:
                    file.write(f"turn={turn}\nmoves={moves}")
                    for coord in coords:
                        coord_piece = coords[coord]
                        if coord_piece == empty:
                            piece_name = "empty"
                        if coord_piece == wrook:
                            piece_name = "wrook"
                        if coord_piece == wknight:
                            piece_name = "wknight"
                        if coord_piece == wbishop:
                            piece_name = "wbishop"
                        if coord_piece == wqueen:
                            piece_name = "wqueen"
                        if coord_piece == wking:
                            piece_name = "wking"
                        if coord_piece == wpawn:
                            piece_name = "wpawn" 
                        if coord_piece == brook:
                            piece_name = "brook"
                        if coord_piece == bknight:
                            piece_name = "bknight"
                        if coord_piece == bbishop:
                            piece_name = "bbishop"
                        if coord_piece == bqueen:
                            piece_name = "bqueen"
                        if coord_piece == bking:
                            piece_name = "bking"
                        if coord_piece == bpawn:
                            piece_name = "bpawn"
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
        reset_everything()
        game()                  

    #reset variables and show the board first time
    reset_afterturnchecks()
    show_board()
    save_game_state()

    #game flow
    while True:

        #load turn data
        player_data = TURN_DATA[turn]
        player = player_data["name"]
        opponent = player_data["opponent"]
        own_pieces = player_data["pieces"]
        opponent_pieces = player_data["opponent_pieces"]
        direction = player_data["direction"]

        #check if there's a check
        first_time = 1
        check_check()

        #move string
        move = str(input(f"{moves+1}) {player}'s turn: "))
        move = move.lower()

        #operation commands
        if move == "save":
            save_game()
            continue
        if move == "quit" or move == "exit":
            quit_game()
            continue
        if move == "restart":
            restart_game()
            continue
        if move == "undo":
            file_exists = 0
            for file in os.listdir(current_game_path):
                if file == f"move{moves-1}.txt":
                    file_exists = 1
                    load_data(current_folder_name, file)
                    show_board()
                    break
            if file_exists == 0:
                print("\nPrevious game state does not exist.\n")
            continue
        
        #check for validity
        if len(move) != 4:
            proper_form()
            continue
        start_coord = f"{move[0]}{move[1]}"
        end_coord = f"{move[2]}{move[3]}"

        if start_coord == end_coord:
            not_viable()
            continue
        if start_coord in coords:
            piece = coords[start_coord]
        else:
            proper_form()
            continue
        if piece not in own_pieces:
            no_piece()
            continue
        if end_coord in coords:
            end_coord_piece = coords[end_coord]
            if end_coord_piece in own_pieces:
                not_viable()
                continue
            
            #piece rules
            else:

                #king rules
                if piece == wking or piece == bking:
                    piece_name = "King"
                    if abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) <= 1 and abs(coords_ver.index(start_coord[1]) - coords_ver.index(end_coord[1])) <= 1:
                        play_move()
                    else:
                        not_viable()
                        continue

                #bishop rules
                if piece == wbishop or piece == bbishop:
                    piece_name = "Bishop"
                    horizontal_change = coords_hor.index(end_coord[0]) - coords_hor.index(start_coord[0])
                    vertical_change = coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])
                    if abs(horizontal_change) == abs(vertical_change):
                        change = abs(horizontal_change)
                        collisions = diagonal_collision_check(start_coord, end_coord)
                        if collisions <= 1:        
                            play_move()
                        else:
                            not_viable() 
                            continue  
                    else:
                        not_viable()
                        continue 

                #pawn rules
                if piece == wpawn or piece == bpawn:
                    piece_name = "Pawn"
                    if coords[end_coord] == empty and start_coord[0] == end_coord[0] and (coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])) == 1 * direction:
                        play_move()
                    elif coords[end_coord] == empty and start_coord[0] == end_coord[0] and coords_ver.index(start_coord[1]) == 4.5 - (2.5 * direction) and (coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])) == 2 * direction and coords[f"{end_coord[0]}{int(end_coord[1]) + (-1 * direction)}"] == empty:
                        play_move()
                    elif (coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])) == 1 * direction and abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) == 1 and coords[end_coord] != empty:
                        play_move()   
                    else:
                        not_viable()
                        continue  

                #knight rules
                if piece == wknight or piece == bknight:
                    piece_name = "Knight"
                    if abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) == 1 and abs(coords_ver.index(start_coord[1]) - coords_ver.index(end_coord[1])) == 2:
                        play_move()
                    elif abs(coords_hor.index(start_coord[0]) - coords_hor.index(end_coord[0])) == 2 and abs(coords_ver.index(start_coord[1]) - coords_ver.index(end_coord[1])) == 1:    
                        play_move()
                    else:
                        not_viable()
                        continue

                #rook rules    
                if piece == wrook or piece == brook:  
                    piece_name = "Rook"
                    if start_coord[0] == end_coord[0] or start_coord[1] == end_coord[1]:
                        horizontal_change = coords_hor.index(end_coord[0]) - coords_hor.index(start_coord[0])
                        vertical_change = coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])
                        collisions = collision_check(start_coord, end_coord)  
                        if collisions <= 1:
                            play_move()
                        else:
                            not_viable()
                            continue    
                    else:
                        not_viable()
                        continue    

                #queen rules
                if piece == wqueen or piece == bqueen:
                    piece_name = "Queen"
                    horizontal_change = coords_hor.index(end_coord[0]) - coords_hor.index(start_coord[0])
                    vertical_change = coords_ver.index(end_coord[1]) - coords_ver.index(start_coord[1])
                    if start_coord[0] == end_coord[0] or start_coord[1] == end_coord[1]:
                        collisions = collision_check(start_coord, end_coord)  
                        if collisions <= 1:
                            play_move()
                        else:
                            not_viable()
                            continue
                    elif abs(horizontal_change) == abs(vertical_change):
                        change = abs(horizontal_change)
                        collisions = diagonal_collision_check(start_coord, end_coord)
                        if collisions <= 1:        
                            play_move()
                        else:
                            not_viable()   
                            continue
                    else:
                        not_viable()
                        continue    
        else: 
            proper_form()
            continue

        #check if move escapes check, otherwise revert
        first_time = 0
        check_check()
        if check == 1:
            coords[start_coord] = previous1
            coords[end_coord] = previous2
            not_viable()
            continue

        moves = moves + 1
        save_game_state()
        show_board()
        move_summary()
        reset_afterturnchecks()
        turn = TURN_DATA[turn]["next"]

#start
game_info()
reset_everything()
game()      