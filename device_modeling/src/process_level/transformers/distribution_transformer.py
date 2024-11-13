from transformer_device import Transformer

class DistributionTransformer(Transformer):
    def __init__(self, name: str, protocol: str, capacity: float):
        super().__init__(name, protocol, transformer_type="Distribution Transformer")
        self.capacity = capacity

    def get_capacity(self) -> float:
        return self.capacity