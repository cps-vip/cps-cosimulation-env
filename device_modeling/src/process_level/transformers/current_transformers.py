from .transformer_device import Transformer

class CurrentTransformer(Transformer):
    def __init__(self, name: str , primary_winding: int, secondary_winding: int):
        self.name = name
        self.transformer_type = "Current Transformer"
        self.primary_current: float = 0.0 #input current
        self.primary_winding: int  = primary_winding
        self.secodnary_winding: int =  secondary_winding
        self.secondary_current: float = 0.0 #output current
        self.isMulti_ratio: bool= False
        self.multi_ratio: float= 1.0

    def set_primary_current(self, current: float) -> None:
        if current <= 0:
            raise ValueError("current need to set other than zero")
        self.primary_current = current
        self._set_secondary_current

    def get_primary_current(self) -> float:
        return self.primary_current

    def enable_multi_ratio(self, ratio:float) -> None:
        if ratio <= 1.0:
            raise ValueError("ratio value must be less than 1")
        self.isMulti_ratio = True
        set

    def disable_multi_ratio(self) -> None:
        self.isMulti_ratio = False
        self.multi_ratio = 1.0

    def isMulti_ratio(self) -> bool:
        return self.isMulti_ratio

    def set_multi_ratio(self, ratio:float) -> None:
        self.multi_ratio = ratio
        
    def get_multi_ratio(self) -> float:
        return self.multi_ratio

    def _set_secondary_current(self) -> None:
        if self.primary_current == 0.0:
            raise ValueError("Primary current is not set.")

        # Calculate the secondary current using primary and current ratio
        secondary_current = self.primary_current * (self.primary_winding/ self.secodnary_winding) * self.multi_ratio

        # Set the calculated secondary current
        self.secondary_current = secondary_current

    def get_secondary_current(self) -> float:
        return self.secondary_current


    def set_state(self, primary_current: float,  isMulti_ratio: bool, multi_ratio: float) -> None:
        if isMulti_ratio == True:
            self.set_multi_ratio(self, multi_ratio)
        else :self.set_multi_ratio(self)

        self.set_primary_current(self, primary_current)
        
    def get_output_current(self) -> float:
        return self.secondary_current()

