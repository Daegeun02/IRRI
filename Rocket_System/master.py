## all program do in coroutine...

import numpy as np
from rocket_system import RocketSystem
from controller import Controller



class master:
    def __init__(self, datahub):
        self.rocket = RocketSystem(datahub)
        self.controller = Controller(datahub)

    def run(self):
        pass