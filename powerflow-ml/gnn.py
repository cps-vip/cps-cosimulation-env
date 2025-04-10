import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

# Define a Graph Convolutional Network layer
class PowerFlowGCN(torch.nn.Module):
    def __init__(self):
        super(PowerFlowGCN, self).__init__()
        self.conv1 = GCNConv(1, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x

if (__name__ == "__main__"):
    # --- Step 1: Preprocess IEEE case9 ---
    x, edge_index = preprocess_matpower_case('case9')

    # --- Step 2: Run through the GCN ---
    model = PowerFlowGCN()
    output = model(x, edge_index)

    print("GCN output:\n", output)
