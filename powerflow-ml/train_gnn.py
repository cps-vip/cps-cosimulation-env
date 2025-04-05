from torch.utils.data import random_split
from torch_geometric.loader import DataLoader
from preprocessing import generate_dataset

full_dataset = generate_dataset('case9', num_samples=5)

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

    print(f"Epoch {epoch:02d} | Loss: {total_loss / len(train_loader):.6f}")
