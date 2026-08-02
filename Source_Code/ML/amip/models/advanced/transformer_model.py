import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import Dict, Union, Tuple
import os
import math
from ..base_model import BaseModel

class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.pe[:x.size(0)]
        return x

class TimeSeriesTransformer(nn.Module):
    def __init__(self, input_dim: int, d_model: int = 64, nhead: int = 4, num_layers: int = 2, output_dim: int = 2, dropout: float = 0.1):
        super().__init__()
        self.input_linear = nn.Linear(input_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        
        encoder_layers = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward=d_model*4, dropout=dropout, batch_first=True)
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        
        self.fc_direction = nn.Linear(d_model, output_dim)
        self.fc_return = nn.Linear(d_model, 1)
        
    def forward(self, x):
        # x shape: (batch, seq_len, input_dim)
        x = self.input_linear(x)
        # transpose for positional encoding: (seq_len, batch, d_model)
        x = x.transpose(0, 1)
        x = self.pos_encoder(x)
        # back to batch_first
        x = x.transpose(0, 1)
        
        output = self.transformer_encoder(x)
        # Pooling: take last step
        last_out = output[:, -1, :]
        
        direction_logits = self.fc_direction(last_out)
        expected_return = self.fc_return(last_out)
        
        return direction_logits, expected_return

class TransformerModel(BaseModel):
    def __init__(self, model_name: str = "transformer", input_dim: int = 10, d_model: int = 64, 
                 num_layers: int = 2, output_dim: int = 2, seq_length: int = 20, lr: float = 1e-3, **kwargs):
        super().__init__(model_name, **kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.seq_length = seq_length
        self.model = TimeSeriesTransformer(input_dim, d_model=d_model, num_layers=num_layers, output_dim=output_dim).to(self.device)
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
        
        X_seq, y_seq = self._create_sequences(X_train, y_train)
        y_ret = np.zeros_like(y_seq, dtype=np.float32) 
        
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
