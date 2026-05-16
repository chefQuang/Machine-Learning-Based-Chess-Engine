# ♟️ Machine Learning-Based Chess Engine

This is the source code for the **Chess AI** project, developed as part of the Assignment for the **Introduction to Artificial Intelligence (CO3061)** course at Ho Chi Minh City University of Technology (HCMUT).

The project focuses on building a game-playing agent using **Machine Learning** methods, alongside developing an agent based on traditional **Search Algorithms** to evaluate and compare their performance.

## 🌟 Key Features

* **Graphical User Interface (UI):** Integrated with Pygame to provide an intuitive interactive experience (Human vs. AI).
* **Machine Learning Agent:** The core agent of the project, trained to make intelligent moves through board pattern recognition.
* **Search-based Agent (Baseline):** An agent utilizing the Minimax algorithm combined with Alpha-Beta Pruning and heuristic Piece-Square Tables.
* **Evaluation Mode:** Automated testing mode allowing the ML Agent to play against a Random Agent (to ensure a 10/10 win rate) or against human players.

## 📂 Project Structure

* `main_ui.py`: The main entry point, containing the User Interface logic (Pygame).
* `agent.py`: Contains the definitions and prediction logic for the Machine Learning Agent and the Random Agent.
* `engine.py` / `evaluation.py`: Contains the traditional search algorithms (Minimax) and the evaluation functions for baseline comparison.
* `download_assets.py`: A utility script to automatically fetch standard chess piece images.
* `assets/`: Directory for chess piece images (auto-generated when running the script).
* `saved_models/`: Directory for storing trained Machine Learning model files (e.g., `.pth`, `.h5`).

## ⚙️ Installation & Usage

**Step 1: Clone the repository**
```bash
git clone [https://github.com/chefQuang/Machine-Learning-Based-Chess-Engine.git](https://github.com/chefQuang/Machine-Learning-Based-Chess-Engine.git)
cd Machine-Learning-Based-Chess-Engine
****Bước 2: Cài đặt thư viện
pip install pygame chess
******** Để chạy trò chơi
python main_ui.py
