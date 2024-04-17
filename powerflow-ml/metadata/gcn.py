import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

class PowerFlowGCN(torch.nn.Module):
    def __init__(self, metadata_dim):
        super(PowerFlowGCN, self).__init__()
        self.conv1 = GCNConv(1 + metadata_dim, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, x, edge_index, metadata):
        # Concatenate metadata with node features
        x = torch.cat([x, metadata], dim=1)
        
        # Pass through first GCN layer
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        
        # Pass through second GCN layer
        x = self.conv2(x, edge_index)
        return x

if (__name__ == "__main__"):
    # Define a simple electrical grid as a graph
    edge_index = torch.tensor([[0, 1, 1, 2, 2, 3, 3, 0], [1, 0, 2, 1, 3, 2, 0, 3]], dtype=torch.long)
    num_nodes = 4

    # Define initial node features (voltage magnitudes)
    initial_voltage = torch.tensor([1.0, 1.0, 1.0, 1.0], dtype=torch.float).view(-1, 1)
    x = initial_voltage.clone()

    # Define metadata features
    metadata_dim = 2
    metadata = torch.randn(num_nodes, metadata_dim)

    # Instantiate the GCN model with metadata
    gcn_model = PowerFlowGCN(metadata_dim)

    # Set the number of iterations for solving power flow equations
    num_iterations = 10

    # Simulate power flow iterations
    for _ in range(num_iterations):
        # Forward pass through the GCN model with metadata
        x = gcn_model(x, edge_index, metadata)
        
        # Clamp voltage magnitudes to ensure they remain positive
        x = torch.relu(x)

    # Display the final voltage magnitudes
    print("Final Voltage Magnitudes (GCN with Metadata):")
    print(x)
