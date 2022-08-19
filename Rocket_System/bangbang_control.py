import numpy as np



class BangBangControl:
    def __init__(self, rocket, system):
        ## contains rocket's real time data
        self.rocket = rocket

        ## contains rocket's system
        self.system = system

        ## deadband: rad
        self.deadband = 5

        ## gain values
        self.alpha = 1

        ## rate feedback
        self.rate_feedback = 0

    def run(self):
        self.feedback()
        self.bangbang()

    def feedback(self):
        ## angular position
        theta_cur = self.rocket.state[1:3,0]

        ## angular velocity
        theta_dot = self.rocket.state[4:6,0]

        ## desired status
        theta_cmd = np.zeros((2,1))

        ## feedback
        self.rate_feedback = theta_cmd - theta_cur - self.alpha * theta_dot

    def bangbang(self):

        ## bang!
        rank1 = self.rate_feedback < self.deadband

        ## bang!
        rank2 = self.rate_feedback > self.deadband * -1

        ## bangbang !!
        rank = (rank1 * rank2) * (-1) + 1

        ## control 
        sgn   = np.sign(self.rate_feedback)

        ## control signal
        self.system.control_signal[2*sgn[0]]   = rank[0]
        self.system.control_signal[2*sgn[1]+1] = rank[1]
