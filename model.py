import torch
import torch.nn as nn

class ChessFNN(nn.Module):
    def __init__(self):
        super(ChessFNN, self).__init__()
        self.fc1 = nn.Linear(in_features = 768, out_features = 256)
        self.fc2 = nn.Linear(in_features = 256, out_features = 128)
        self.fc3 = nn.Linear(in_features = 128, out_features = 64)
        self.fc4 = nn.Linear(in_features = 64, out_features = 1)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.tanh(self.fc4(x))
        return x
    
if __name__ == "__main__":
    dummy_boards = torch.randn(5,8,8,12)
    model = ChessFNN()
    predictions = model(dummy_boards)
    print("Model initialized successfully!")
    print(f"Input shape: {dummy_boards.shape}")
    print(f"Output shape: {predictions.shape}")
    print(f"Sample predictions:\n{predictions.detach().numpy()}")
