# Contains the MassFlowController class and hardware-related logic
import random
from labjack import ljm


class LabJackInterface:
    def __init__(self, use_mock=False):
        self.use_mock = use_mock
        self.handle = None if use_mock else ljm.openS("ANY", "ANY", "ANY")

    def write_name(self, name, value):
        if self.use_mock:
            print(f"Mock write: {name} = {value}")
        else:
            ljm.eWriteName(self.handle, name, value)

    def read_name(self, name):
        return (
            random.uniform(0, 100)
            if self.use_mock
            else ljm.eReadName(self.handle, name)
        )

    def close(self):
        if not self.use_mock:
            ljm.close(self.handle)


class MassFlowController:
    def __init__(
        self, name, flow_set, flow_read, scale, offset, setpoint, labjack
    ):
        self.name = name
        self.flow_set = flow_set
        self.flow_read = flow_read
        self.scale = scale
        self.offset = offset
        self.setpoint = setpoint
        self.labjack = labjack

    def set_flow(self, setpoint):
        self.setpoint = setpoint
        self.labjack.write_name(
            self.flow_set, (setpoint - self.offset) / self.scale
        )

    def get_flow(self):
        return round(
            self.labjack.read_name(self.flow_read) * self.scale + self.offset
        )
