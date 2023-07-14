# iD Tech: Python Chess AI, 2022

# Import Modules & Libraries
import chess
import pygame
import sys
from stockfish import Stockfish
import ai_algorithms as ai
import display_gui as gui
import global_vars as G

# Game Settings
# <= -1: player, 0: no input, 1: random, 2: heat map, 3: predictive, 4: stockfish, 5: improvised sunfish engine with predictive
# second variable the difficulity, only avaliable for 3 and above
TEST_MODE = False
AI_DELAY = 0
B_DIFFICULTY = [5, 3]
W_DIFFICULTY = [4, 3]

# Difficulty Control Function
def difficulty_options(move, difficulty):
    if difficulty[0] == 0:
        move = chess.Move.null()
    elif difficulty[0] == 1:
        move = ai.select_random()
    elif difficulty[0] == 2:
        move = ai.select_positional()
    elif difficulty[0] == 3:
        move = ai.select_predictive(difficulty[1])
    elif difficulty[0] == 4:
        move = ai.stockfishtime(difficulty[1])
    elif difficulty[0] == 5:
        move = ai.select_predictive1(difficulty[1])
    if difficulty[0] >= 0:
        ai.make_ai_move(move, AI_DELAY)
    return move

# Board Setup
G.BOARD_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
G.BOARD.set_board_fen(G.BOARD_FEN)
gui.draw_board()
from_square = None
outcome = None
current_turn = 0
move = None

# Pygame Display Loop
while not outcome:
    #print(G.BOARD.turn == chess.WHITE, move)
    G.CLOCK.tick(60)
    move = None

    # Player Control Flow

    if G.BOARD.turn == chess.BLACK: 
        move = difficulty_options(move, B_DIFFICULTY)
    elif G.BOARD.turn == chess.WHITE:
        move = difficulty_options(move, W_DIFFICULTY)


    # Check Input Events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Reset Highlight on Any Click
            tile_num = gui.tile_pos_to_num(event.pos)
            gui.draw_board()

            # First Click on New Turn -> Select Square
            if from_square == None:
                from_square = gui.make_selection(tile_num)
            # Selected Square Clicked Again -> Unselect Square
            elif from_square == tile_num:
                gui.draw_board()
                from_square = None
            # Potential Move Clicked -> ...
            elif from_square != None:
                # ...If Valid, Highlight & Move Selected Piece
                for move in G.BOARD.legal_moves:
                    if move.from_square == from_square and move.to_square == tile_num:
                        gui.draw_select_square(move.from_square)
                        gui.draw_select_square(move.to_square)
                        #gui.print_san(move)
                        G.BOARD.push(move)
                        from_square = None
                # ...If Invalid, Only Select Square Instead
                if from_square != None:
                    from_square = gui.make_selection(tile_num)

        # Window Close -> End Program
        elif event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()


    #if move != None and ((G.BOARD.turn == chess.BLACK and W_DIFFICULTY == -1) or (G.BOARD.turn == chess.WHITE and B_DIFFICULTY == -1)):
    if move != None and move != chess.Move.from_uci("a2a4"):
        if G.BOARD.turn == chess.BLACK:
            current_turn += 1
            print()
            print(current_turn)
        print(move, end = "   ")
        stockfish = Stockfish(path="stockfish_engine.exe", parameters={"Threads": 2, "Minimum Thinking Time": 30})
        stockfish.set_fen_position(G.BOARD.fen())
        evalu = stockfish.get_evaluation()
        eval_string = ""
        if evalu["type"] == "mate":
            if evalu["value"] == 0:
                print("checkmate")
            else:
                print("mate in " + str(abs(evalu["value"])))
        elif evalu["value"] == 0.00:
            print("draw")
        else:
            print(str(evalu["value"]/100))


    # Draw All Pieces on Screen
    for piece_type in range(1, 7):
        w_piece_tiles = G.BOARD.pieces(piece_type, chess.WHITE)
        for tile_num in w_piece_tiles:
            gui.draw_piece(tile_num, piece_type, chess.WHITE)

        b_piece_tiles = G.BOARD.pieces(piece_type, chess.BLACK)
        for tile_num in b_piece_tiles:
            gui.draw_piece(tile_num, piece_type, chess.BLACK)

    # Check End Game Conditions
    outcome = G.BOARD.outcome()
    if not TEST_MODE and outcome:
        gui.determine_outcome(outcome)

    # Update the Display Screen
    pygame.display.update()

# Wait till Exit after Game Over
while True:
    G.CLOCK.tick(60)
    for event in pygame.event.get():
        # Window Close -> End Program
        if event.type == pygame.QUIT:
            outcome = True
            pygame.display.quit()
            pygame.quit()
            sys.exit()
