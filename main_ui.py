import pygame
import chess
import sys
import os
import json
from agent import MLAgent, RandomAgent

# --- CONSTANTS & SETTINGS (Chess.com Style) ---
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8

# Colors
LIGHT_SQUARE = (235, 236, 208)
DARK_SQUARE = (115, 149, 82)
HIGHLIGHT_COLOR = (246, 246, 105)
MENU_BG = (48, 46, 43)
TEXT_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Machine Learning Chess Engine")
font = pygame.font.SysFont("Arial", 32, bold=True)
small_font = pygame.font.SysFont("Arial", 20)

# --- LOAD ASSETS ---
IMAGES = {}
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    try:
        for piece in pieces:
            # Load and scale images to fit the squares perfectly
            img = pygame.image.load(os.path.join('assets', f'{piece}.png'))
            IMAGES[piece] = pygame.transform.smoothscale(img, (SQUARE_SIZE, SQUARE_SIZE))
    except FileNotFoundError:
        print("WARNING: Could not find piece images in the 'assets' folder.")
        print("Please ensure you have wP.png, bP.png, etc., saved in an 'assets' directory.")
        sys.exit()

# --- STATISTICS TRACKER ---
STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"ML_Wins": 0, "Random_Wins": 0, "Draws": 0, "Human_Wins": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=4)

# --- DRAWING FUNCTIONS ---
def draw_board(screen, board, selected_square):
    colors = [LIGHT_SQUARE, DARK_SQUARE]
    for row in range(8):
        for col in range(8):
            color = colors[((row + col) % 2)]
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)
            
    # Highlight selected square
    if selected_square is not None:
        row, col = 7 - (selected_square // 8), selected_square % 8
        rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect)

def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # chess.py sets A1=0 at bottom-left. Pygame sets 0,0 at top-left.
            # We must invert the row for visual rendering.
            row = 7 - (square // 8)
            col = square % 8
            
            symbol = piece.symbol()
            color_prefix = 'w' if piece.color == chess.WHITE else 'b'
            piece_name = f"{color_prefix}{symbol.upper()}"
            
            screen.blit(IMAGES[piece_name], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_text_centered(text, y_offset, font_to_use, color=TEXT_COLOR):
    rendered = font_to_use.render(text, True, color)
    rect = rendered.get_rect(center=(WIDTH//2, y_offset))
    WIN.blit(rendered, rect)
    return rect

# --- MAIN LOGIC ---
def main():
    load_images()
    stats = load_stats()
    
    # Initialize Agents
    model_path = "saved_models/chess_model_v1.pth"
    ml_agent = MLAgent(color=chess.WHITE, model_path=model_path, skill_level=10)
    random_agent = RandomAgent(color=chess.BLACK)
    
    board = chess.Board()
    state = "MENU" # States: MENU, PLAYING, GAME_OVER
    mode = None    # Modes: H_VS_ML, ML_VS_RND
    selected_square = None
    winner_text = ""

    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(30) # 30 FPS is plenty for chess
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # --- MENU INTERACTION ---
            if state == "MENU" and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 250 <= y <= 290:
                    mode = "H_VS_ML"
                    ml_agent.color = chess.BLACK
                    board.reset()
                    state = "PLAYING"
                elif 320 <= y <= 360:
                    mode = "ML_VS_RND"
                    ml_agent.color = chess.WHITE
                    random_agent.color = chess.BLACK
                    board.reset()
                    state = "PLAYING"
                    
            # --- HUMAN PLAYING INTERACTION ---
            elif state == "PLAYING" and mode == "H_VS_ML" and board.turn == chess.WHITE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    col, row = x // SQUARE_SIZE, y // SQUARE_SIZE
                    clicked_square = (7 - row) * 8 + col
                    
                    if selected_square is None:
                        # Select a piece
                        if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == chess.WHITE:
                            selected_square = clicked_square
                    else:
                        # Attempt to move
                        move = chess.Move(selected_square, clicked_square)
                        # Handle pawn promotion to Queen automatically for simplicity
                        if board.piece_at(selected_square) and board.piece_at(selected_square).piece_type == chess.PAWN and (7 - row) == 7:
                            move = chess.Move(selected_square, clicked_square, promotion=chess.QUEEN)
                            
                        if move in board.legal_moves:
                            board.push(move)
                        selected_square = None
                        
            # --- GAME OVER INTERACTION ---
            elif state == "GAME_OVER" and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 400 <= y <= 450: # Play Again button area
                    state = "MENU"

        # --- DRAWING & AI LOGIC ---
        WIN.fill(MENU_BG)
        
        if state == "MENU":
            draw_text_centered("CHESS ENGINE", 150, font)
            
            # Buttons
            pygame.draw.rect(WIN, DARK_SQUARE, (WIDTH//4, 250, WIDTH//2, 40), border_radius=5)
            draw_text_centered("Play vs ML Agent", 270, small_font)
            
            pygame.draw.rect(WIN, DARK_SQUARE, (WIDTH//4, 320, WIDTH//2, 40), border_radius=5)
            draw_text_centered("Watch ML vs Random", 340, small_font)
            
            # Stats
            draw_text_centered(f"ML Wins: {stats['ML_Wins']} | Random Wins: {stats['Random_Wins']} | Draws: {stats['Draws']}", 450, small_font)
            
        elif state == "PLAYING":
            draw_board(WIN, board, selected_square)
            draw_pieces(WIN, board)
            pygame.display.flip() # Force immediate screen update
            
            # AI Moves
            if not board.is_game_over():
                if mode == "H_VS_ML" and board.turn == chess.BLACK:
                    pygame.time.wait(200) # Tiny delay so human sees the turn change
                    move = ml_agent.get_move(board)
                    board.push(move)
                    
                elif mode == "ML_VS_RND":
                    pygame.time.wait(300) # 0.3 second delay to watch the simulation
                    if board.turn == chess.WHITE:
                        move = ml_agent.get_move(board)
                    else:
                        move = random_agent.get_move(board)
                    board.push(move)
            else:
                # Game is over, determine result
                result = board.result()
                if result == "1-0":
                    winner_text = "White (ML) Wins!" if mode == "ML_VS_RND" else "Human Wins!"
                    if mode == "ML_VS_RND": stats["ML_Wins"] += 1
                    else: stats["Human_Wins"] += 1
                elif result == "0-1":
                    winner_text = "Black (Random) Wins!" if mode == "ML_VS_RND" else "ML Agent Wins!"
                    if mode == "ML_VS_RND": stats["Random_Wins"] += 1
                    else: stats["ML_Wins"] += 1
                else:
                    winner_text = "Draw!"
                    stats["Draws"] += 1
                    
                save_stats(stats)
                state = "GAME_OVER"

        elif state == "GAME_OVER":
            draw_board(WIN, board, None) # Draw final board state in background
            draw_pieces(WIN, board)
            
            # Overlay
            s = pygame.Surface((WIDTH, HEIGHT))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            WIN.blit(s, (0,0))
            
            draw_text_centered("GAME OVER", 200, font, HIGHLIGHT_COLOR)
            draw_text_centered(winner_text, 280, font)
            
            pygame.draw.rect(WIN, DARK_SQUARE, (WIDTH//4, 400, WIDTH//2, 50), border_radius=5)
            draw_text_centered("Play Again / Menu", 425, small_font)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()