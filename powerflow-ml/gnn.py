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
    # Define a simple electrical grid as a graph
    # In this example, let's consider a small grid with 4 nodes (buses) and 4 edges (power lines)
    edge_index = torch.tensor([[0, 1, 1, 2, 2, 3, 3, 0], [1, 0, 2, 1, 3, 2, 0, 3]], dtype=torch.long)
    num_nodes = 4

    # Define initial node features (voltage magnitudes)
    initial_voltage = torch.tensor([1.0, 1.0, 1.0, 1.0], dtype=torch.float).view(-1, 1)
    x = initial_voltage.clone()

    # Instantiate the GCN model
    gcn_model = PowerFlowGCN()

    # Set the number of iterations for solving power flow equations
    num_iterations = 10

    # Simulate power flow iterations
    for _ in range(num_iterations):
        # Forward pass through the GCN model
        x = gcn_model(x, edge_index)
        
        # Clamp voltage magnitudes to ensure they remain positive
        x = F.relu(x)

    # Display the final voltage magnitudes
    print("Final Voltage Magnitudes:")
    print(x)
