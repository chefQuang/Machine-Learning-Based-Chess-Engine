import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import os

from model import ChessFNN

def train():
    print("\033[33m1. Loading dataset...\033[0m")
    try:
        x_data = np.load("dataset/x_features.npy")
        y_data = np.load("dataset/y_labels.npy")
    except FileNotFoundError:
        print("\033[31mThe file was not found\033[0m")
        return
    
    x_tensor = torch.tensor(x_data, dtype = torch.float32)
    y_tensor = torch.tensor(y_data, dtype = torch.float32).view(-1, 1)

    dataset = TensorDataset(x_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size = 64, shuffle = True)

    print("\033[33m2. Initializing Model...\033[0m")
    model = ChessFNN()

    loss_function = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr = 0.001)

    epochs = 10
    print(f"\033[33m3. Starting Training for {epochs} Epochs...\033[0m")
    for epoch in range(epochs):
        total_loss = 0
        for batch_x, batch_y in dataloader:
            optimizer.zero_grad()
            predictions = model(batch_x)
            loss = loss_function(predictions, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        average_loss = total_loss / len(dataloader)
        print(f"Epoch [{epoch+1}/{epochs}] Completed | Average Error (Loss): {average_loss:.4f}")

    print("\033[33m\n4. Training Complete! Saving model weights...\033[0m")

    os.makedirs("save_models", exist_ok = True)
    save_path = "save_models/chess_model_v1.pth"
    torch.save(model.state_dict(), save_path)
    print("\033[32mModel successfully saved\033[0m")

if __name__ == "__main__":
    train()
