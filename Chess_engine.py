import chess
import chess.svg
import random as r
from IPython.display import SVG, display, clear_output
 
def is_endgame(board): 
    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
    minor_major = (len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK)) +
                   len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK)) +
                   len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK)))
    return queens == 0 or (queens <= 2 and minor_major <= 2)
 
pawn_table = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
 
knight_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]
 
bishop_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]
 
rook_table = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0
]
 
queen_table = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]
 
king_table_middlegame = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     40, 50, 10,  0,  0, 10, 50, 40
]
 
king_table_endgame = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]
 
pst_tables = {
    chess.PAWN: pawn_table,
    chess.KNIGHT: knight_table,
    chess.BISHOP: bishop_table,
    chess.ROOK: rook_table,
    chess.QUEEN: queen_table,
    chess.KING: king_table_middlegame,
}
 
def get_pst_value(table, square, color):
    if color == chess.WHITE:
        return table[square ^ 56]
    else:
        return table[square]
 
 
values = {'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900}
def evaluate(board):
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    endgame = is_endgame(board)
    w_mat = 0
    b_mat = 0
    for square, piece in board.piece_map().items():
        value = values.get(piece.symbol().lower(), 0)
        if piece.piece_type == chess.KING:
            if endgame == True:
                table = king_table_endgame
            else:
                table = king_table_middlegame
        if piece.piece_type != chess.KING:
            table = pst_tables[piece.piece_type]
        pst_bonus = get_pst_value(table, square, piece.color)
        if piece.color == chess.WHITE:
            w_mat += value + pst_bonus
        else:
            b_mat += value + pst_bonus
            
    return b_mat - w_mat
 
def minimax(board, depth, maximizing, alpha, beta):
    if depth == 0 or board.is_game_over():
        return evaluate(board), None
 
    movess = list(board.legal_moves)
    lst_mov = []
    not_att = []
    for k in movess:
        if board.is_capture(k) == True:
            lst_mov.append(k)
        else:
            not_att.append(k)
 
    lst_mov = lst_mov + not_att
    best_move = lst_mov[0]
 
    if maximizing == True:
        best_score = float('-inf')
        for move in lst_mov:
            board.push(move)
            score, _ = minimax(board, depth - 1, False, alpha, beta)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
    else:
        best_score = float('inf')
        for move in lst_mov:
            board.push(move)
            score, _ = minimax(board, depth - 1, True, alpha, beta)
            board.pop()
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
            if alpha >= beta:
                break
 
    return best_score, best_move
 
board = chess.Board()
 
display(SVG(chess.svg.board(board, size=350)))
chessmove = "h"
while not board.is_game_over() and chessmove != "stopp":
    chessmove = str(input('Trekk: '))
    while chessmove != "stopp" and chessmove != "eval" and not (4 <= len(chessmove) <= 5):
        print("ugyldig lengde")
        chessmove = str(input('Trekk: '))
    if chessmove == "eval":
        eval = evaluate(board)
        print(eval)
        chessmove = str(input('Trekk: '))
    else:
        move = chess.Move.from_uci(chessmove)
        while move not in list(board.legal_moves):
            print("ulovlig")
            chessmove = str(input('Trekk: '))
            move = chess.Move.from_uci(chessmove)
        board.push(move)
 
        if not board.is_game_over():
            score, move = minimax(board, 6, True, float('-inf'), float('inf'))
            board.push(move)
 
        clear_output(wait=True)
        display(SVG(chess.svg.board(board, size=350)))
    
if board.is_checkmate():
    winner = "sort vant" if board.turn == chess.WHITE else "hvit vant"
    clear_output(wait=True)
    print(winner)
elif chessmove == "stopp":
    clear_output(wait=True)
    print("avbrutt")
else:
    clear_output(wait=True)
    print("remis")
display(SVG(chess.svg.board(board, size=350)))