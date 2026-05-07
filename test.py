import os
import time

# Import the core functions from your individual modules
from processing import process_dataset
from train import train
from evaluate import run_evaluation_suite

def main():
    print("="*40)
    print(" AUTOMATED CHESS AI PIPELINE ")
    print("="*40 + "\n")

    # --- STEP 1: DATA PROCESSING ---
    dataset_x_path = "dataset/x_features.npy"
    dataset_y_path = "dataset/y_labels.npy"
    pgn_path = "dataset/lichess_db_standard_rated_2014-08.pgn"

    print("--- Phase 1: Data Preparation ---")
    if os.path.exists(dataset_x_path) and os.path.exists(dataset_y_path):
        print("[SKIP] Processed dataset found. Skipping PGN extraction.")
    else:
        process_dataset(pgn_path, max_games=3000)

    # --- STEP 2: MODEL TRAINING ---
    model_path = "save_models/chess_model_v1.pth"

    print("\n--- Phase 2: Model Training ---")
    if os.path.exists(model_path):
        print(f"[SKIP] Trained model found at '{model_path}'. Skipping training.")
    else:
        train()

    # --- STEP 3: EVALUATION ---
    print("\n--- Phase 3: Evaluation Suite ---")
    time.sleep(1)
    run_evaluation_suite()
    
    print("\n" + "="*40)
    print(" PIPELINE FINISHED ")
    print("="*40)

if __name__ == "__main__":
    main()