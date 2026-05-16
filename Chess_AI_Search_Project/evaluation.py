

# File chứa Hàm lượng giá (Piece-Square Tables)



import chess

# Điểm vật chất cơ bản cho từng loại quân
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Bảng điểm vị trí (Piece-Square Table) cho quân Tốt (Trắng)
PAWN_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]

# Bảng điểm vị trí cho quân Mã (Trắng) - Thích đứng ở trung tâm
KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

def evaluate_board(board):
    # Kiểm tra chiếu bí
    if board.is_checkmate():
        return -99999 if board.turn == chess.WHITE else 99999
    
    # Kiểm tra hòa
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # 1. Tính điểm vật chất
            val = PIECE_VALUES.get(piece.piece_type, 0)
            
            # 2. Tính điểm vị trí (PST)
            pst_val = 0
            if piece.piece_type == chess.PAWN:
                pst_val = PAWN_PST[square] if piece.color == chess.WHITE else PAWN_PST[chess.square_mirror(square)]
            elif piece.piece_type == chess.KNIGHT:
                pst_val = KNIGHT_PST[square] if piece.color == chess.WHITE else KNIGHT_PST[chess.square_mirror(square)]
            
            score = val + pst_val
            
            # Cộng điểm cho Trắng, trừ điểm cho Đen
            if piece.color == chess.WHITE:
                evaluation += score
            else:
                evaluation -= score
                
    return evaluation