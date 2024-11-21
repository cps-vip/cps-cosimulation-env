import torch
import torch.nn as nn

class HELFNet(nn.Module):
    def __init__(self, n_buses):
        """
        Initialize the HELF network.
        
        Args:
            n_buses: Number of buses in the power grid.
        """
        super(HELFNet, self).__init__()
        self.n_buses = n_buses

    def forward(self, y_bus, s, v_slack):
        """
        Perform the forward propagation using the HELF method.
        
        Args:
            y_bus: Complex-valued admittance matrix (Y-bus).
            s: Complex power injections (P - jQ).
            v_slack: Slack bus voltage (complex scalar).

        Returns:
            Complex-valued voltage solutions for all buses.
        """
        # Step 1: Initialize
        n = self.n_buses
        v = torch.zeros((n,), dtype=torch.cfloat)  # Initialize complex voltages
        v[0] = v_slack  # Set the slack bus voltage

        # Initialize holomorphic coefficients
        v_h = torch.zeros((n, n), dtype=torch.cfloat)  # Holomorphic voltage expansion
        v_h[:, 0] = v  # Base case: voltage coefficients

        # Step 2: Iteratively compute holomorphic coefficients
        for k in range(1, n):
            for i in range(1, n):  # Skip slack bus
                sum_term = torch.sum(y_bus[i, :] * v_h[:, k - 1])
                if torch.abs(v_h[i, k - 1]) < 1e-8:
                    v_h[i, k - 1] = 1e-8  # Small epsilon to avoid NaN
                v_h[i, k] = -s[i] / v_h[i, k - 1] - sum_term

        # Step 3: Analytic continuation to approximate voltages
        indices = torch.arange(1, n + 1, dtype=torch.float)  # Use real-valued arange
        indices = indices.to(torch.cfloat)  # Cast to complex
        for i in range(1, n):
            v[i] = torch.sum(v_h[i, :] / indices)

        return v


# Example Usage
if __name__ == "__main__":
    # Example Y-bus matrix (Admittance matrix)
    y_bus = torch.tensor(
        [[10+5j, -5j, 0, 0, 0],
         [-5j, 10+5j, -5j, 0, 0],
         [0, -5j, 10+5j, -5j, 0],
         [0, 0, -5j, 10+5j, -5j],
         [0, 0, 0, -5j, 10+5j]], 
        dtype=torch.cfloat
    )

    # Example power injections (complex P - jQ)
    s = torch.tensor([0+0j, -1-0.5j, -2-1j, -1.5-0.8j, -1-0.4j], dtype=torch.cfloat)

    # Slack bus voltage
    v_slack = torch.tensor(1.0 + 0j, dtype=torch.cfloat)

    # Initialize and run HELFNet
    helf_net = HELFNet(n_buses=5)
    voltages = helf_net(y_bus, s, v_slack)

    print("Voltage Solution for all Buses:\n", voltages)
