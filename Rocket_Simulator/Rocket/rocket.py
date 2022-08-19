from Rocket.rocket_component   import *

import numpy as np



class Rocket:

    ## structure data
    CG             = 0      # m
    mass           = 3      # kg
    length         = 1.5    # m
    diameter       = 0.11   # m
    inertia = np.zeros((3,1))    # kg*m^2
    
    ## aerodynamic data
    aerodynamic    = {"CP"      : 0,
                      "wet_area": 0,
                      "Cd"      : 0,
                      "crs_area": 0}
    CP = 0
    Cd = 0
    Cf = 0.0045

    ## motor's performance
    propellant = {"name"          : "propellant1",
                  "mass"          : 0.45,
                  "mass_flow_rate": 0.15,
                  "Isp"           : 120}

    thrust         = 100    # N

    ## stage
    stage = {}

    ## generate stage
    def __init__(self):

        ## structure data
        self.CG       = 0
        self.mass     = 0
        self.diameter = 0
        self.length   = 0
        self.inertia = np.zeros((3,1))

        ## aerodynamic data
        self.CP       = {}
        self.wet_area = {}
        self.Cd       = {}
        self.crs_area = 0

        ## motor's performance
        self.propellant    = {}
        self.thrust        = 0

###########################################################

    ## stage fusion
    def __add__(self, other):

        ## structure data
        self.CG       = RocketComponents.center_of_gravity(self, other)
        self.mass    += other.data['mass']
        self.length  += other.data['length']
        self.diameter = other.data['diameter']
        self.inertia  = RocketComponents.inertia(self)

        ## aerodynamic data
        self.CP[other.part_name]       = other.data["CP"]
        self.wet_area[other.part_name] = other.wet_area()
        self.Cd[other.part_name]       = other.data["Cd"]

        if isinstance(other, BodyTube):
            self.crs_area = RocketComponents.cross_section_area(other)

        elif isinstance(other, Motor):
            ## motor's performance
            self.propellant     = other.data['propellant']
            self.thrust         = other.data['thrust']

        elif isinstance(other, Fins):
            pass

        else:
            pass

###########################################################

    ## stage seperation
    def __sub__(self):
        pass

###########################################################

    ## represent
    def __str__(self) -> str:
        ## structure data
        Rocket.CG       = self.CG
        Rocket.mass     = self.mass
        Rocket.length   = self.length
        Rocket.diameter = self.diameter
        Rocket.inertia  = self.inertia

        ## aerodynamic data
        Rocket.aerodynamic['CP']       = self.CP
        Rocket.aerodynamic['wet_area'] = self.wet_area
        Rocket.aerodynamic['Cd']       = self.Cd
        Rocket.aerodynamic['crs_area'] = self.crs_area

        ## motor's performance
        Rocket.propellant = self.propellant
        Rocket.thrust     = self.thrust

        return "stage is successfully constructed"
