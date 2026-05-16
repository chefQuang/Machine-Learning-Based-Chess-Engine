import chess
from engine import get_best_move

def print_board(board):
    print("\n-------------------------")
    print(board)
    print("-------------------------\n")

def play_game():
    board = chess.Board()
    
    print("=== ĐỒ ÁN AI CỜ VUA (SEARCH AGENT) ===")
    print("1. Level Dễ (Depth = 2)")
    print("2. Level Trung Bình (Depth = 3)")
    print("3. Level Khó (Depth = 4)")
    
    choice = input("Chọn độ khó cho AI (1-3): ")
    depth = 2
    if choice == '2': depth = 3
    if choice == '3': depth = 4
    
    player_color = input("Bạn muốn cầm quân Trắng (w) hay Đen (b)? ").lower()
    player_is_white = (player_color == 'w')
    
    while not board.is_game_over():
        print_board(board)
        
        # Xác định lượt của ai
        is_player_turn = (board.turn == chess.WHITE and player_is_white) or \
                         (board.turn == chess.BLACK and not player_is_white)
                         
        if is_player_turn:
            # Lượt của bạn
            move_str = input("Nhập nước đi của bạn (VD: e2e4): ")
            try:
                move = chess.Move.from_uci(move_str)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Nước đi không hợp lệ theo luật cờ vua!")
            except ValueError:
                print("Lỗi định dạng! Vui lòng nhập chuẩn UCI (VD: g1f3).")
        else:
            # Lượt của AI
            print("AI đang tính toán nước đi...")
            best_move = get_best_move(board, depth)
            print(f">>> AI quyết định đi: {best_move}")
            board.push(best_move)
            
    print("\n=== TRẬN ĐẤU KẾT THÚC ===")
    print(f"Kết quả: {board.result()}")

if __name__ == "__main__":
    play_game()