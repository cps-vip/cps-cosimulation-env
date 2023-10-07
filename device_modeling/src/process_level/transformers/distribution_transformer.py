from src.process_level.transformers import Transformer

class DistributionTransformer(Transformer):
    def __init__(self, name: str, communication_protocol: str, capacity: float):
        super().__init__(name, communication_protocol, transformer_type="Distribution Transformer")
        self.capacity = capacity

    def get_capacity(self) -> float:
        return self.capacity