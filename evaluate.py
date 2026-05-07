import chess
from agent import RandomAgent, MLAgent

def play_match(white_agent, black_agent, match_number, log_moves = True):
    """Simulates a single full game between 2 agents"""
    board = chess.Board()
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = white_agent.get_move(board)
        else:
            move = black_agent.get_move(board)
        board.push(move)
    
    result = board.result()

    if result == "1-0":
        winner = "White"
    elif result == "0-1":
        winner = "Black"
    else:
        winner = "Draw"

    print(f"Match {match_number}: {winner} wins! ({result}) - Moves played: {len(board.move_stack)}")

    """if log_moves:
        game = chess.pgn.Game.from_board(board)
        white_name = "MLAgent" if hasattr(white_agent, 'model') else "RandomAgent"
        black_name = "MLAgent" if hasattr(black_agent, 'model') else "RandomAgent"
        game.headers["Event"] = f"University AI Evaluation - Match {match_number}"
        game.headers["White"] = white_name
        game.headers["Black"] = black_name
        game.headers["Result"] = result
        print("\n--- Move Log (Copy/Paste to Lichess) ---")
        print(game)
        print("-" * 40)"""
    return result
    
def run_evaluation_suite():
    print("--- CHESS ENGINE EVALUATION SUITE ---")
    print("\033[33mLoading Agents...\n\033[0m")
    model_path = "save_models/chess_model_v1.pth"
    
    ml_agent_white = MLAgent(color = chess.WHITE, model_path = model_path, skill_level = 10)
    random_agent_black = RandomAgent(color = chess.BLACK)
    
    ml_agent_black = MLAgent(color = chess.BLACK, model_path = model_path, skill_level = 10)
    random_agent_white = RandomAgent(color = chess.WHITE)

    ml_wins = 0
    draws = 0
    total_matches = 10

    print("\nPhase 1: ML Agent plays as WHITE (5 Matches)")
    for i in range(1, 6):
        result = play_match(ml_agent_white, random_agent_black, i)
        if result == "1-0":
            ml_wins += 1
        elif result == "1/2-1/2":
            draws += 1
    
    print("\nPhase 2: ML Agent plays as BLACK (5 Matches)")
    for i in range(6, 11):
        result = play_match(random_agent_white, ml_agent_black, i)
        if result == "0-1":
            ml_wins += 1
        elif result == "1/2-1/2":
            draws += 1
    
    print("\033[32m\n---FINAL RESULT---\033[0m")
    print(f"Total Matches: {total_matches}")
    print(f"ML Agent Wins: {ml_wins}")
    print(f"Random Agent Wins: {total_matches - ml_wins - draws}")
    print(f"Draws: {draws}")

    if ml_wins == 10:
        print("\033[32m\nSUCCESS: The ML Agent defeated the Random Agent 10/10 times! Requirement met.\033[0m")
    else:
        print("\033[31m\nFAILED: The ML Agent did not achieve a 10/10 win rate.\033[0m")

if __name__ == "__main__":
    run_evaluation_suite()
