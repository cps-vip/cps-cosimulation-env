from scipy.io import loadmat
import torch
from torch_geometric.data import Data
import numpy as np
from oct2py import Oct2Py
from matpower import Matpower

def preprocess_matpower_case(case_name):
    with Matpower(engine='octave') as m:  # run as context manager
        mpc = m.eval(case_name, verbose=False)
        mpc = m.runpf(mpc)
    # Extract bus and branch information
    bus = mpc.bus
    branch = mpc.branch

    # Extract number of buses
    num_buses = bus.shape[0]

    # Extract node features (e.g., voltage magnitude)
    voltage_magnitudes = torch.tensor(bus[:, 7], dtype=torch.float32).view(-1, 1)  # Column 7 = VM

    # Build edge_index for PyTorch Geometric (bidirectional edges)
    from_bus = branch[:, 0].astype(int) - 1  # Convert 1-based to 0-based
    to_bus = branch[:, 1].astype(int) - 1
    edge_index = torch.tensor(
        np.array([np.concatenate([from_bus, to_bus]),
                  np.concatenate([to_bus, from_bus])]),
        dtype=torch.long
    )

    # Return a PyTorch Geometric Data object
    return voltage_magnitudes, edge_index


if (__name__ == '__main__'):
    preprocess_matpower_case('case9')
    # preprocess_matpower_case("case10ba.m")