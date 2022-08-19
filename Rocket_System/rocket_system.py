import numpy as np
import matplotlib.pyplot as plt



class RocketSystem:
    def __init__(self, datahub):
        self.datahub = datahub

    def transition(self):
        pass



class State:
    def __init__(self, datahub):
        self.datahub = datahub

    def transition(self):
        return NotImplementedError()



class Ready(State):
    def __init__(self, datahub):
        super().__init__(datahub)

    def transition(self):
        pass



class Takeoff(State):
    def __init__(self, datahub):
        super().__init__(datahub)

    def transition(self):
        pass



class Staging(State):
    def __init__(self, datahub):
        super().__init__(datahub)

    def transition(self):
        pass



class Hovering(State):
    def __init__(self, datahub):
        super().__init__(datahub)

    def transition(self):
        pass