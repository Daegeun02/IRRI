from Rocket_Simulator.Rocket.rocket_backup        import Rocket
from Rocket_Simulator.rocket_status import RealTimeRocket



class FSM:
    def __init__(self):
        ## states
        self.mission_list = {}
        self.mission_list["Takeoff"]         = Takeoff()
        self.mission_list["stage speration"] = StageSperation()
        self.mission_list["hovering"]        = Hovering()
        self.mission_list["eject parashute"] = EjectParashute()

    def transition(self):
        self.on_going_mission = self.mission_list[State.state]
        self.on_going_mission.transition()
        



class State:

    state = "NO ON GOING MISSION"

    def __init__(self):
        pass

    def transition(self):
        return NotImplementedError()



class Takeoff(State):
    def __init__(self):
        super().__init__()

    def transition(self):
        if RealTimeRocket.t < Rocket.burnout_time:
            pass



class StageSperation(State):
    def __init__(self):
        super().__init__()

    def transition(self):
        pass



class Hovering(State):
    def __init__(self):
        super().__init__()

    def transition(self):
        pass



class EjectParashute(State):
    def __init__(self):
        super().__init__()

    def transition(self):
        pass