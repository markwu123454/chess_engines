# Import Modules & Libraries
import pygame, chess

# Display Window
ID_TECH_TITLE = "iD Tech: Python Chess"
ID_TECH_LOGO = pygame.image.load('logos/idtech_logo_ipc.png')

# Board Colors
LIGHT_COLOR = pygame.Color('#EEEED5')
DARK_COLOR = pygame.Color('#7D945D')
LABEL_COLOR = pygame.Color('#A6A695')
BORDER_COLOR = pygame.Color('#53534A')
L_SELECT_COLOR = pygame.Color(196, 97, 109)
D_SELECT_COLOR = pygame.Color(110, 153, 192)
LINE_COLOR = pygame.Color('#53534A')
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

# Board Constants
TILE_COUNT = 8
LABEL_SIZE = 25
BOARD_SIZE = 735
BORDER_SIZE = 2
LINE_SIZE = -1
PIECE_SCALE = 0.9
SELECT_SCALE = 0.8
MOVE_SCALE = 0.5

# Board Calculations
TILE_SIZE = BOARD_SIZE / TILE_COUNT
TILE_DIMENSIONS = (TILE_SIZE, TILE_SIZE)
BOARD_DIMENSIONS = (BOARD_SIZE, BOARD_SIZE)
BOARD = chess.Board(chess.STARTING_FEN)

# Screen Settings
FLAGS = pygame.RESIZABLE | pygame.SCALED
SCREEN_SIZE = BOARD_SIZE + LABEL_SIZE
SCREEN_DIMENSIONS = (SCREEN_SIZE, SCREEN_SIZE)
SCREEN = pygame.display.set_mode(SCREEN_DIMENSIONS, FLAGS)
CLOCK = pygame.time.Clock()

# Piece Type Positional Values
pawn_score = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knight_score = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishop_score = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rook_score = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queen_score = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

king_score = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]




pawn_score1 = [
    0, 0, 0, 0, 0, 0, 0, 0,
    78, 83, 86, 73, 102, 82, 85, 90,
    7, 29, 21, 44, 40, 31, 44, 7,
    -17, 16, -2, 15, 14, 0, 15, -13,
    -26, 3, 10, 9, 6, 1, 0, -23,
    -22, 9, 5, -11, -10, -2, 3, -19,
    -31, 8, -7, -37, -36, -14, 3, -31,
    0, 0, 0, 0, 0, 0, 0, 0]

knight_score1 = [
    -66, -53, -75, -75, -10, -55, -58, -70,
    -3, -6, 100, -36, 4, 62, -4, -14,
    10, 67, 1, 74, 73, 27, 62, -2,
    24, 24, 45, 37, 33, 41, 25, 17,
    -1, 5, 31, 21, 22, 35, 2, 0,
    -18, 10, 13, 22, 18, 15, 11, -14,
    -23, -15, 2, 0, 2, 0, -23, -20,
    -74, -23, -26, -24, -19, -35, -22, -69]

bishop_score1 = [
    -59, -78, -82, -76, -23, -107, -37, -50,
    -11, 20, 35, -42, -39, 31, 2, -22,
    -9, 39, -32, 41, 52, -10, 28, -14,
    25, 17, 20, 34, 26, 25, 15, 10,
    13, 10, 17, 23, 17, 16, 0, 7,
    14, 25, 24, 15, 8, 25, 20, 15,
    19, 20, 11, 6, 7, 6, 20, 16,
    -7, 2, -15, -12, -14, -15, -10, -10]

rook_score1 = [
    35, 29, 33, 4, 37, 33, 56, 50,
    55, 29, 56, 67, 55, 62, 34, 60,
    19, 35, 28, 33, 45, 27, 25, 15,
    0, 5, 16, 13, 18, -4, -9, -6,
    -28, -35, -16, -21, -13, -29, -46, -30,
    -42, -28, -42, -25, -25, -35, -26, -46,
    -53, -38, -31, -26, -29, -43, -44, -53,
    -30, -24, -18, 5, -2, -18, -31, -32]

queen_score1 = [
    6, 1, -8, -104, 69, 24, 88, 26,
    14, 32, 60, -10, 20, 76, 57, 24,
    -2, 43, 32, 60, 72, 63, 43, 2,
    1, -16, 22, 17, 25, 20, -13, -6,
    -14, -15, -2, -5, -1, -10, -20, -22,
    -30, -6, -13, -11, -16, -11, -16, -27,
    -36, -18, 0, -19, -15, -15, -21, -38,
    -39, -30, -31, -13, -31, -36, -34, -42]

king_score1 = [
    4, 54, 47, -99, -99, 60, 83, -62,
    -32, 10, 55, 56, 56, 55, 10, 3,
    -62, 12, -57, 44, -67, 28, 37, -31,
    -55, 50, 11, -4, -19, 13, 0, -49,
    -55, -43, -52, -28, -51, -47, -8, -50,
    -47, -42, -43, -79, -64, -32, -29, -32,
    -4, 3, -14, -50, -57, -18, 13, 4,
    17, 30, -3, -14, 6, -1, 40, 18]
