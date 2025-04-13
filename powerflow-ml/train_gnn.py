from torch.utils.data import random_split
from torch_geometric.loader import DataLoader
from preprocessing import generate_dataset
from gnn import PowerFlowGCN
import torch.nn.functional as F
import torch


if (__name__ == '__main__'):
    full_dataset = generate_dataset('case9', num_samples=500)

    # Split into train/val
    train_len = int(0.8 * len(full_dataset))
    train_dataset, val_dataset = random_split(full_dataset, [train_len, len(full_dataset) - train_len])

    train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=1)

    model = PowerFlowGCN()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(30):
        model.train()
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            out = model(batch.x, batch.edge_index)
            loss = F.mse_loss(out, batch.y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        # Validation phase
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                out = model(batch.x, batch.edge_index)
                loss = F.mse_loss(out, batch.y)
                val_loss += loss.item()
        
        avg_train_loss = total_loss / len(train_loader)
        avg_val_loss = val_loss / len(val_loader)
        print(f"Epoch {epoch:02d} | Train Loss: {avg_train_loss:.6f} | Val Loss: {avg_val_loss:.6f}")

        print(f"Epoch {epoch:02d} | Loss: {total_loss / len(train_loader):.6f}")
