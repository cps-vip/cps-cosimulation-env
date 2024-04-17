import torch
import torch.nn.functional as F
from torch_geometric.nn import GINConv

class PowerFlowGIN(torch.nn.Module):
    def __init__(self):
        super(PowerFlowGIN, self).__init__()
        self.conv1 = GINConv(torch.nn.Sequential(torch.nn.Linear(1, 16), torch.nn.ReLU(), torch.nn.Linear(16, 16)))
        self.conv2 = GINConv(torch.nn.Sequential(torch.nn.Linear(16, 16), torch.nn.ReLU(), torch.nn.Linear(16, 1)))

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        return x


if (__name__ == "__main__"):

    # Define a simple electrical grid as a graph
    edge_index = torch.tensor([[0, 1, 1, 2, 2, 3, 3, 0], [1, 0, 2, 1, 3, 2, 0, 3]], dtype=torch.long)
    num_nodes = 4

    # Define initial node features (voltage magnitudes)
    initial_voltage = torch.tensor([1.0, 1.0, 1.0, 1.0], dtype=torch.float).view(-1, 1)
    x = initial_voltage.clone()

    # Instantiate the GIN model
    gin_model = PowerFlowGIN()

    # Set the number of iterations for solving power flow equations
    num_iterations = 10

    # Simulate power flow iterations
    for _ in range(num_iterations):
        # Forward pass through the GIN model
        x = gin_model(x, edge_index)
        
        # Clamp voltage magnitudes to ensure they remain positive
        x = torch.relu(x)

    # Display the final voltage magnitudes
    print("Final Voltage Magnitudes (GIN):")
    print(x)
