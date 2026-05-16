
# File chứa Thuật toán Minimax + Alpha-Beta



import chess
import math
import time
from evaluation import evaluate_board

def order_moves(board):
    # Tối ưu hóa: Đưa các nước ăn quân lên xét trước để Alpha-Beta cắt tỉa nhanh hơn
    legal_moves = list(board.legal_moves)
    captures = []
    quiets = []
    for move in legal_moves:
        if board.is_capture(move):
            captures.append(move)
        else:
            quiets.append(move)
    return captures + quiets

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    ordered_moves = order_moves(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in ordered_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break # Cắt tỉa Beta
        return max_eval
    else:
        min_eval = math.inf
        for move in ordered_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break # Cắt tỉa Alpha
        return min_eval

def get_best_move(board, depth):
    start_time = time.time()
    best_move = None
    
    maximizing_player = (board.turn == chess.WHITE)
    alpha = -math.inf
    beta = math.inf
    
    if maximizing_player:
        max_eval = -math.inf
        for move in order_moves(board):
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
                alpha = max(alpha, eval)
    else:
        min_eval = math.inf
        for move in order_moves(board):
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            if eval < min_eval:
                min_eval = eval
                best_move = move
                beta = min(beta, eval)
                
    end_time = time.time()
    
    # In ra thời gian chạy để bạn ghi nhận số liệu cho phần Báo cáo (Yêu cầu 4)
    print(f"[Search Engine] Depth: {depth} | Time: {end_time - start_time:.3f}s | Eval Score: {max_eval if maximizing_player else min_eval}")
    return best_move