import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from typing import Dict, Union, Tuple
import os

class AutoencoderModel(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, latent_dim: int):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, latent_dim)
        )
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return encoded, decoded

class EmbeddingEngine:
    def __init__(self, input_dim: int, hidden_dim: int = 64, latent_dim: int = 16, lr: float = 1e-3):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = AutoencoderModel(input_dim, hidden_dim, latent_dim).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def train(self, X_train: np.ndarray, epochs: int = 50, batch_size: int = 64) -> Dict[str, float]:
        self.model.train()
        dataset = torch.utils.data.TensorDataset(torch.FloatTensor(X_train))
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        total_loss = 0
        for epoch in range(epochs):
            epoch_loss = 0
            for (batch_x,) in dataloader:
                batch_x = batch_x.to(self.device)
                self.optimizer.zero_grad()
                
                _, decoded = self.model(batch_x)
                loss = self.criterion(decoded, batch_x)
                
                loss.backward()
                self.optimizer.step()
                epoch_loss += loss.item()
            total_loss = epoch_loss / len(dataloader)
            
        return {"loss": total_loss}

    def get_embeddings(self, X: np.ndarray) -> np.ndarray:
        self.model.eval()
        with torch.no_grad():
            x_tensor = torch.FloatTensor(X).to(self.device)
            encoded, _ = self.model(x_tensor)
            return encoded.cpu().numpy()
            
    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        torch.save(self.model.state_dict(), filepath)
        
    def load(self, filepath: str) -> None:
        self.model.load_state_dict(torch.load(filepath, map_location=self.device))
        
    def export_onnx(self, filepath: str, input_shape: tuple) -> None:
        self.model.eval()
        dummy_input = torch.randn(1, input_shape[1]).to(self.device)
        torch.onnx.export(self.model.encoder, dummy_input, filepath, 
                          input_names=['input'], output_names=['embedding'], 
                          dynamic_axes={'input': {0: 'batch_size'}, 'embedding': {0: 'batch_size'}})
