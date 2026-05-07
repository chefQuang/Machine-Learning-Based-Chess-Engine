import chess
import random
import torch
import numpy as np
from model import ChessFNN

from processing import board_to_tensor

class RandomAgent:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        """Pick a random legal move"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        return random.choice(legal_moves)
    
class MLAgent:
    def __init__(self, color, model_path, skill_level = 10):
        self.color = color
        self.skill_level = skill_level
        self.model = ChessFNN()
        try:
            self.model.load_state_dict(torch.load(model_path))
            self.model.eval() #Set to evaluation mode, turns off learning rate
            print(f"[{'White' if color else 'Black'} MLAgent] Loaded model successfully. Skill: {skill_level}/10")
        except FileNotFoundError:
            print("\033[31mThe model was not found\033[0m")

    def evaluate_board(self, board):
        """Converts board to a tensor and get the evaluations"""
        board_array = board_to_tensor(board)
        board_tensor = torch.tensor(board_array, dtype = torch.float32).unsqueeze(0) #Convert numpy array to tensor and batch dimension

        with torch.no_grad():
            score = self.model(board_tensor).item()

        return score
    
    def get_move(self, board):
        """Evaluates all legal moves and picks the best one based on skill level"""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        error_chance = (10 - self.skill_level) * 0.10
        if random.random() < error_chance:
            return random.choice(legal_moves)
        
        best_move = None
        best_score = -float('inf') if self.color == chess.WHITE else float('inf') #if white, it want highest positive score, if black, it want lowest negative score
        for move in legal_moves:
            board.push(move)
            if board.is_checkmate():
                board.pop()
                return move
            score = self.evaluate_board(board)
            score += random.uniform(-0.0001, 0.0001)
            board.pop()
            if self.color == chess.WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        
        if best_move is None:
            return random.choice(legal_moves)
        
        return best_move