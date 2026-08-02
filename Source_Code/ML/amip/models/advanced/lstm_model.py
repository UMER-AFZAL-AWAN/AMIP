import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import Dict, Union, Tuple
import os
from ..base_model import BaseModel

class LSTMNetwork(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, output_dim: int, dropout: float = 0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        
        # Attention
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim),
            nn.Tanh(),
            nn.Linear(hidden_dim, 1)
        )
        
        self.fc_direction = nn.Linear(hidden_dim, output_dim)
        self.fc_return = nn.Linear(hidden_dim, 1)
        
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        
        # Attention over time steps
        attn_weights = torch.softmax(self.attention(lstm_out), dim=1)
        context = torch.sum(attn_weights * lstm_out, dim=1)
        
        direction_logits = self.fc_direction(context)
        expected_return = self.fc_return(context)
        
        return direction_logits, expected_return

class LSTMModel(BaseModel):
    def __init__(self, model_name: str = "lstm", input_dim: int = 10, hidden_dim: int = 64, 
                 num_layers: int = 2, output_dim: int = 2, seq_length: int = 20, lr: float = 1e-3, **kwargs):
        super().__init__(model_name, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.seq_length = seq_length
        self.model = LSTMNetwork(input_dim, hidden_dim, num_layers, output_dim).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        self.criterion_cls = nn.CrossEntropyLoss()
        self.criterion_reg = nn.MSELoss()
        
    def _create_sequences(self, X: pd.DataFrame, y: Union[pd.Series, np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        X_vals = X.values
        y_vals = y.values if isinstance(y, pd.Series) else y
        
        seqs_X, seqs_y = [], []
        for i in range(len(X_vals) - self.seq_length + 1):
            seqs_X.append(X_vals[i:(i + self.seq_length)])
            if y_vals is not None:
                seqs_y.append(y_vals[i + self.seq_length - 1])
                
        return np.array(seqs_X), (np.array(seqs_y) if y_vals is not None else None)

    def train(self, X_train: pd.DataFrame, y_train: Union[pd.Series, np.ndarray],
              X_val: pd.DataFrame = None, y_val: Union[pd.Series, np.ndarray] = None, epochs: int = 10, batch_size: int = 32) -> Dict[str, float]:
        self.model.train()
        
        # Assuming y_train contains tuple of (direction, return)
        # For simplicity in BaseModel signature, assume y_train is direction, we spoof return as 0 for now.
        X_seq, y_seq = self._create_sequences(X_train, y_train)
        y_ret = np.zeros_like(y_seq, dtype=np.float32) # Dummy return
        
        dataset = torch.utils.data.TensorDataset(torch.FloatTensor(X_seq), torch.LongTensor(y_seq), torch.FloatTensor(y_ret))
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(epochs):
            for batch_x, batch_y_dir, batch_y_ret in dataloader:
                batch_x, batch_y_dir, batch_y_ret = batch_x.to(self.device), batch_y_dir.to(self.device), batch_y_ret.to(self.device)
                
                self.optimizer.zero_grad()
                out_dir, out_ret = self.model(batch_x)
                
                loss = self.criterion_cls(out_dir, batch_y_dir) + 0.1 * self.criterion_reg(out_ret.squeeze(), batch_y_ret)
                loss.backward()
                self.optimizer.step()
                
        return {"loss": loss.item()}

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)
        
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        self.model.eval()
        X_seq, _ = self._create_sequences(X)
        if len(X_seq) == 0:
            return np.array([])
            
        with torch.no_grad():
            x_tensor = torch.FloatTensor(X_seq).to(self.device)
            out_dir, _ = self.model(x_tensor)
            probs = torch.softmax(out_dir, dim=1).cpu().numpy()
            
        # Pad beginning to match original DataFrame size
        pad = np.zeros((self.seq_length - 1, probs.shape[1]))
        return np.vstack((pad, probs))
        
    def save(self, filepath: str) -> None:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        torch.save(self.model.state_dict(), filepath)
        
    def load(self, filepath: str) -> None:
        self.model.load_state_dict(torch.load(filepath, map_location=self.device))
        
    def export_onnx(self, filepath: str, input_shape: tuple) -> None:
        self.model.eval()
        dummy_input = torch.randn(1, self.seq_length, input_shape[1]).to(self.device)
        torch.onnx.export(self.model, dummy_input, filepath,
                          input_names=['input'], output_names=['direction', 'return'],
                          dynamic_axes={'input': {0: 'batch_size'}, 'direction': {0: 'batch_size'}, 'return': {0: 'batch_size'}})
