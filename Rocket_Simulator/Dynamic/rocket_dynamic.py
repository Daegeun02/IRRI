import numpy as np



class Dynamic:

    dt = 0.125

    g = -9.81

    gravity = np.array([[          0],
                        [          0],
                        [0.5*g*dt*dt],
                        [          0],
                        [          0],
                        [       g*dt]])

    state_matrix = np.array([[ 1, 0, 0,dt, 0, 0],
                             [ 0, 1, 0, 0,dt, 0],
                             [ 0, 0, 1, 0, 0,dt],
                             [ 0, 0, 0, 1, 0, 0],
                             [ 0, 0, 0, 0, 1, 0],
                             [ 0, 0, 0, 0, 0, 1]])

    input_matrix = np.array([[0.5*dt*dt,        0,        0],
                             [        0,0.5*dt*dt,        0],
                             [        0,        0,0.5*dt*dt],
                             [       dt,        0,        0],
                             [        0,       dt,        0],
                             [        0,        0,       dt]])

###########################################################

    def __init__(self):
        pass

    def state_transition(self):
        return NotImplementedError()

    def input(self):
        return NotImplementedError()

###########################################################
###########################################################
###########################################################

class Translation(Dynamic):
    
    def __init__(self):
        pass

###########################################################

    @staticmethod
    def state_transition(rocket, realtimerocket):
        linear_state = realtimerocket.linear_state

        acceleration = Translation.input(rocket, realtimerocket)

        state = Dynamic.state_matrix.dot(linear_state) + \
                Dynamic.input_matrix.dot(acceleration) + \
                Dynamic.gravity

        realtimerocket.linear_state = state

###########################################################

    @classmethod
    def input(cls, rocket, realtimerocket):
        F = realtimerocket.thrust + realtimerocket.drag

        m = rocket.mass

        acceleration = F / m

        return acceleration

###########################################################
###########################################################
###########################################################

class Rotation(Dynamic):
    
    def __init__(self):
        pass

###########################################################

    @staticmethod
    def state_transition(rocket, realtimerocket):
        angular_state = realtimerocket.angular_state

        acceleration = Rotation.input(rocket, realtimerocket)

        state = Dynamic.state_matrix.dot(angular_state) + \
                Dynamic.input_matrix.dot(acceleration)

        realtimerocket.angular_state = state

###########################################################

    @classmethod
    def input(cls, rocket, realtimerocket):
        ## moment
        F = realtimerocket.drag
        r = (rocket.CP - rocket.CG) * realtimerocket.orientation

        ## Euler
        I = rocket.inertia
        w = realtimerocket.angular_state[3:]

        moment = np.zeros((3,1))
        moment[0] = r[1]*F[2] - r[2]*F[1]
        moment[1] = r[2]*F[0] - r[0]*F[2]
        moment[2] = r[0]*F[1] - r[1]*F[0]

        Euler = np.zeros((3,1))
        Euler[0] = (I[1]-I[2])*w[1]*w[2]
        Euler[1] = (I[2]-I[0])*w[2]*w[0]
        Euler[2] = (I[0]-I[1])*w[0]*w[1]

        acceleration = (moment + Euler) / I

        return acceleration
