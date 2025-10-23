import numpy as np
from torch_geometric.data import Data
from matpower import Matpower
import multiprocessing
import torch
import tqdm

def perturb_case_loads(case, load_scale_range=(0.5, 1.5)):
    """
    Modifies Pd and Qd values in a MATPOWER case to simulate varying loads.
    """
    new_case = case.copy()
    Pd = new_case['bus'][:, 2]  # Pd column
    Qd = new_case['bus'][:, 3]  # Qd column

    # Apply random scaling factors
    scale = np.random.uniform(*load_scale_range, size=Pd.shape)
    new_case['bus'][:, 2] = Pd * scale
    new_case['bus'][:, 3] = Qd * scale

    return new_case

def get_datapoint(case_name, dataset, i):
    with Matpower(engine='matlab') as m:  # run as context manager
        mpc = m.eval(case_name, verbose=False)
        mpc = m.rundcpf(mpc, verbose=False)
        perturbed = perturb_case_loads(mpc)
        solved = m.runpf(perturbed, verbose=False)
    
    x = torch.tensor(perturbed['bus'][:, 7], dtype=torch.float32).unsqueeze(1)
    y = torch.tensor(solved['bus'][:, 7], dtype=torch.float32).unsqueeze(1)
    
    from_bus = solved['branch'][:, 0].astype(int) - 1
    to_bus = solved['branch'][:, 1].astype(int) - 1
    edge_index = torch.tensor(
        np.array([np.concatenate([from_bus, to_bus]),
                  np.concatenate([to_bus, from_bus])]),
        dtype=torch.long
    )
    
    data = Data(x=x, edge_index=edge_index, y=y)
    dataset[i] = data
    return data

def generate_dataset(case_name='case9', num_samples=500):
    with multiprocessing.Manager() as manager:
        # Construct shared data object
        dataset = manager.list([0] * num_samples)

        # Format arguments for allocation to worker pool        
        arg_list = [0] * num_samples
        for i in range(num_samples):
            arg_list[i] = (case_name, dataset, i)

        # Construct worker pool and allocate datapoint generation
        with multiprocessing.Pool(20) as pool:
            results = tqdm.tqdm(pool.imap(get_datapoint_imap, arg_list), total=num_samples)

            # imap is lazily evaluated, explicitly pull results
            for result in results:
                pass
        
        results = list(dataset)

    return results

# Simple wrapper to arrange input methods for multiprocessing.pool.imap() calls
def get_datapoint_imap(input_args):
    (case_name, dataset, i) = input_args
    return get_datapoint(case_name, dataset, i)
