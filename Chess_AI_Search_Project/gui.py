import pygame
import chess
import sys
from engine import get_best_move

# Khởi tạo thông số màn hình
WIDTH = HEIGHT = 512
DIMENSION = 8  # Bàn cờ 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

# Màu sắc bàn cờ
COLOR_LIGHT = pygame.Color(240, 217, 181)
COLOR_DARK = pygame.Color(181, 136, 99)

IMAGES = {}

def load_images():
    """Tải hình ảnh quân cờ từ thư mục images vào bộ nhớ"""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        # Chữ hoa chữ thường của python-chess hơi khác, ta map lại cho dễ
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"images/{piece.lower()}.png"), (SQ_SIZE, SQ_SIZE)
        )

def draw_board(screen):
    """Vẽ các ô vuông sáng/tối"""
    colors = [COLOR_LIGHT, COLOR_DARK]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    """Vẽ quân cờ lên bàn dựa vào trạng thái hiện tại của python-chess"""
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # python-chess dùng index từ 0 (A1) đến 63 (H8)
            # Pygame vẽ từ góc trên bên trái (A8), nên cần lật lại tọa độ Y
            square_index = (7 - row) * 8 + col
            piece = board.piece_at(square_index)
            if piece:
                color = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol().lower()
                # Định dạng tên theo dictionary IMAGES
                image_key = color + piece_type.upper() if piece_type.lower() != 'p' else color + 'p'
                
                screen.blit(IMAGES[image_key], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AI Cờ Vua - Search & Machine Learning")
    clock = pygame.time.Clock()
    
    board = chess.Board()
    load_images()
    
    running = True
    square_selected = () # Tọa độ (row, col) người dùng vừa click
    player_clicks = []   # Lưu 2 click: [(row1, col1), (row2, col2)]
    
    # Cài đặt độ khó AI
    AI_DEPTH = 3 
    player_is_white = True # Đổi thành False nếu bạn muốn cầm quân Đen
    
    while running:
        is_human_turn = (board.turn == chess.WHITE and player_is_white) or \
                        (board.turn == chess.BLACK and not player_is_white)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                
            # Xử lý click chuột của người chơi
            elif e.type == pygame.MOUSEBUTTONDOWN and is_human_turn and not board.is_game_over():
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                
                if square_selected == (row, col): # Click lại ô cũ -> Hủy chọn
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                
                if len(player_clicks) == 2: # Đã chọn điểm đi và điểm đến
                    start_sq = (7 - player_clicks[0][0]) * 8 + player_clicks[0][1]
                    end_sq = (7 - player_clicks[1][0]) * 8 + player_clicks[1][1]
                    
                    move = chess.Move(start_sq, end_sq)
                    
                    # Xử lý phong cấp (mặc định lên Hậu)
                    if board.piece_at(start_sq) and board.piece_at(start_sq).piece_type == chess.PAWN:
                        if (board.turn == chess.WHITE and player_clicks[1][0] == 0) or \
                           (board.turn == chess.BLACK and player_clicks[1][0] == 7):
                            move = chess.Move(start_sq, end_sq, promotion=chess.QUEEN)

                    if move in board.legal_moves:
                        board.push(move)
                        square_selected = ()
                        player_clicks = []
                    else:
                        # Click không hợp lệ, lưu click thứ 2 làm click đầu tiên cho lượt sau
                        player_clicks = [square_selected]

        # Vẽ bàn cờ
        draw_board(screen)
        
        # Highlight ô được chọn
        if square_selected != ():
            r, c = square_selected
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Độ trong suốt
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            
        draw_pieces(screen, board)
        pygame.display.flip()
        
        # Xử lý lượt của AI
        if not is_human_turn and not board.is_game_over():
            pygame.time.wait(100) # Nghỉ một chút để vẽ xong bàn cờ trước khi AI nghĩ
            best_move = get_best_move(board, AI_DEPTH)
            if best_move:
                board.push(best_move)

        clock.tick(MAX_FPS)
        
        if board.is_game_over():
            print(f"Trận đấu kết thúc! Kết quả: {board.result()}")

if __name__ == "__main__":
    main()