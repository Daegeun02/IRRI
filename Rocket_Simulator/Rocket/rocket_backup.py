import numpy as np



class Rocket:

    ## position, velocity
    linear_state = np.zeros((6,1))

    ## angular status
    angular_state = np.zeros((6,1))

    ## orientation
    orientation = np.array([1,0,0]).reshape(3,1)

    ## Hz
    dt = 0.1

    ## structure data
    structure_mass = 3      # kg
    fuel_mass      = 0.4    # kg
    structure_CG   = 1.0    # m
    fuel_CG        = 0.5    # m
    length         = 1.5    # m
    diameter       = 0.11   # m
    burnout_time   = 3      # s
    thrust         = 100    # N
    
    burning_ratio  = 0      # kg/s
    total_mass     = 3.4    # kg
    CG             = 0      # m

    ## inertia
    inertia = np.zeros((3,1))    # kg*m^2
    
    ## drag coeffcient
    drag = 0    # N*s/m
    Cd   = 0.3  # 

    ## angle of attack
    aoa  = 0    # rad

    def __init__(self, data):
        ## structure data
        ## mass
        self.structure_mass = data[0]   # kg
        self.fuel_mass      = data[1]   # kg

        ## center of gravity
        self.structure_CG   = data[2]   # m
        self.fuel_CG        = data[3]   # m

        ## shape
        self.length         = data[4]   # m
        self.diameter       = data[5]   # m

        ## stage variable
        self.burnout_time   = data[6]   # s
        self.thrust         = data[7]   # N

        self.burning_ratio   = self.fuel_mass / self.burnout_time

    ## stage fusion...
    def __add__(self, other):
        ## mass
        Rocket.structure_mass = self.structure_mass + other.structure_mass
        Rocket.fuel_mass      = self.fuel_mass      + other.fuel_mass

        ## center of gravity
        Rocket.structure_CG   = self.structure_CG   + other.structure_CG
        Rocket.fuel_CG        = self.fuel_CG        + other.fuel_CG

        ## shape
        Rocket.length         = self.length         + other.length
        Rocket.diameter       = self.diameter
        
        ## stage variable
        Rocket.burnout_time   = self.burnout_time
        Rocket.stage2_burnout = other.burnout_time

        Rocket.burning_ratio  = self.burning_ratio
        Rocket.stage2_burning = other.burning_ratio

        Rocket.thrust         = self.thrust
        Rocket.stage2_thrust  = other.thrust

    ## stage speration
    def __del__(self):
        ## stage speration
        Rocket.structure_mass -= self.structure_mass
        Rocket.length         -= self.length

        ## stage variable update
        # Rocket.burnout_time   = Rocket.stage2_burnout
        # Rocket.burning_ratio  = Rocket.stage2_burning
        # Rocket.thrust         = Rocket.stage2_thrust

# data_stage1 = np.array([1,1,1,1,1,1,1,1])
# data_stage2 = np.array([2,2,2,2,2,2,2,2])

# stage1 = Rocket(data_stage1)
# stage2 = Rocket(data_stage2)

# stage1 + stage2

# print(Rocket.structure_CG)

# del(stage1, stage2)

# print(Rocket.structure_CG)
