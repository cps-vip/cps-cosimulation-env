import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv

class PowerFlowGAT(torch.nn.Module):
    def __init__(self):
        super(PowerFlowGAT, self).__init__()
        self.conv1 = GATConv(1, 16, heads=4, dropout=0.5)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        return x


if (__name__ == "__main__"):
    # Define a simple electrical grid as a graph
    edge_index = torch.tensor([[0, 1, 1, 2, 2, 3, 3, 0], [1, 0, 2, 1, 3, 2, 0, 3]], dtype=torch.long)
    num_nodes = 4

    # Define initial node features (voltage magnitudes)
    initial_voltage = torch.tensor([1.0, 1.0, 1.0, 1.0], dtype=torch.float).view(-1, 1)
    x = initial_voltage.clone()

    # Instantiate the GAT model
    gat_model = PowerFlowGAT()

    # Set the number of iterations for solving power flow equations
    num_iterations = 10

    # Simulate power flow iterations
    for _ in range(num_iterations):
        # Forward pass through the GAT model
        x = gat_model(x, edge_index)
        
        # Clamp voltage magnitudes to ensure they remain positive
        x = torch.relu(x)

    # Display the final voltage magnitudes
    print("Final Voltage Magnitudes (GAT):")
    print(x)
