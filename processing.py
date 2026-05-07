import chess.pgn
import numpy as np
import os

def board_to_tensor(board):
    """Convert a chess board object to 8x8x12 numerical tensor"""
    tensor = np.zeros((8,8,12), dtype = np.float32)
    piece_id = {chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2, chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5}
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color_offset = 0 if piece.color == chess.WHITE else 6
            channel = piece_id[piece.piece_type] + color_offset
            row = square // 8
            col = square % 8
            tensor[row][col][channel] = 1.0
    return tensor

def get_elo(game, color_key):
    elo_str = game.headers.get(color_key, "0")
    try:
        return int(elo_str)
    except ValueError:
        return 0
    
def process_dataset(pgn_filepath, max_games):
    """Reads PGN, filters by ELO, converts to tensors, saves to disk"""
    try:
        pgn_file = open(pgn_filepath, "r", encoding = "utf8")
        print("\033[32mSuccessfully opened\033[0m")
    except FileNotFoundError:
        print("\033[31mThe file was not found\033[0m")
        return
    except Exception as e:
        print("\033[31mUnexpected Error\033[0m")
        return
    
    x_data = []
    y_data = []
    games_processed = 0
    games_skipped = 0
    print("\033[33mProcessing...\033[0m")

    while True:
        game = chess.pgn.read_game(pgn_file)
        if game is None:
            break
        white_elo = get_elo(game, "WhiteElo")
        black_elo = get_elo(game, "BlackElo")
        if white_elo < 1200 or black_elo < 1200:
            games_skipped += 1
            continue
        result = game.headers.get("Result", "*")
        if result == "1-0":
            outcome = 1.0
        elif result == "0-1":
            outcome = -1.0
        else:
            outcome = 0.0
        board = game.board()

        for move in game.mainline_moves():
            x_data.append(board_to_tensor(board))
            y_data.append(outcome)
            board.push(move)

        games_processed += 1
        
        if games_processed % 100 == 0:
            print(f"Processed {games_processed} games... (Skipped {games_skipped})")
        if games_processed >= max_games:
            print(f"\nReached max_games limit ({max_games}). Stopping extraction.")
            break

    pgn_file.close()
    print("\033[33m\nConverting lists to NumPy arrays...\033[0m")
    x_array = np.array(x_data, dtype = np.float32)
    y_array = np.array(y_data, dtype = np.float32)
    print(f"\033[33mFinal Tensor Shape: X: {x_array.shape}, y: {y_array.shape}\033[0m")
    print(f"Successfully processed {games_processed} games.")
    print(f"Skipped {games_skipped} games due to Elo filter.")
    print(f"Generated {len(x_data)} board tensors for training.")
    
    os.makedirs("dataset", exist_ok = True)
    np.save("dataset/x_features.npy", x_array)
    np.save("dataset/y_labels.npy", y_array)

if __name__ == "__main__":
    FILE_PATH = "dataset/lichess_db_standard_rated_2014-08.pgn"
    process_dataset(FILE_PATH, 1000)
