from src.process_level.transformers import Transformer

class Transformer(Transformer):
    def __init__(self, name: str, communication_protocol: str, transformer_type: str):
        super().__init__(name, communication_protocol)
        self.transformer_type = transformer_type

    def get_transformer_type(self) -> str:
        return self.transformer_type
