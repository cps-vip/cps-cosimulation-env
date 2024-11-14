class Device:
    def __init__(self, name: str):
        self.name = name
        #refer to Class_Diagram.drawio
        '''
        self.protocol = protocol
        '''
        self.status = "Inactive"  # Default status

    def activate(self):
        self.status = "Active"

    def deactivate(self):
        self.status = "Inactive"

    def get_status(self) -> str:
        return self.status

    def get_device_name(self) -> str:
        return self.name

### Refer to class diagram. We are not using this method anymore;
'''
    def get_communication_protocol(self) -> str:
        return self.protocol
'''