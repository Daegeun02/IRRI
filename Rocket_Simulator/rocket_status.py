## structure
from Rocket.rocket              import Rocket
from Rocket.rocket_component    import *
from Rocket.make_rocket         import BuildRocket

## dynamic
from Dynamic.rocket_dynamic     import Dynamic, Translation, Rotation
from Dynamic.rocket_aerodynamic import AeroDynamic

## coordinate
from transformer                import Transformer

import numpy as np

from math import acos



class RealTimeRocket:

    BuildRocket.build()

    ## stage information
    stage = "stage1"

    ## position, velocity
    linear_state = np.zeros((6,1))      # m/s

    ## angular status
    angular_state = np.zeros((6,1))

    ## orientation
    orientation = np.array([1,0,0]).reshape(3,1)

    ## angle of attack
    aoa = 0.0   # rad

    ## real time
    t = 0.0     # s

    ## real time thrust
    thrust = np.zeros((3,1))

    ## real time drag
    drag = np.zeros((3,1))

    ## ready to flight: body coordinate to ground coordinate
    Rocket.inertia = Transformer.body_to_ground.dot(Rocket.inertia)

############################################################

    def __init__(self):
        pass

############################################################

    @staticmethod
    def set_launch_angle(launch_data):
        launch_angle = launch_data['launch_angle']
        for direction, theta in launch_angle.items():
            if direction == "roll":
                RealTimeRocket.angular_state[2] = np.deg2rad(theta)

            elif direction == "pitch":
                RealTimeRocket.angular_state[0] = np.deg2rad(theta)

            elif direction == "yaw":
                RealTimeRocket.angular_state[1] = np.deg2rad(theta)

            else:
                return ValueError()

############################################################
############################################################
############################################################

    @staticmethod
    def realtime_status_update():

        ## aerodynamic properties
        RealTimeRocket.aerodynamic_update()

        ## time click
        RealTimeRocket.t += Dynamic.dt

        ## update orientation
        RealTimeRocket.realtime_orientation()

        ## update mass
        RealTimeRocket.realtime_rocket_mass()

        ## update angle of attack
        RealTimeRocket.realtime_aoa()

        ## check rocket's thrust
        RealTimeRocket.realtime_thrust()

        ## translation
        Translation.state_transition(Rocket, RealTimeRocket)

        ## rotation
        Rotation.state_transition(Rocket, RealTimeRocket)
    
############################################################
############################################################
############################################################

    @classmethod
    def aerodynamic_update(cls):
        velocity = RealTimeRocket.linear_state[3:]

        ## center of pressure
        Rocket.CP = AeroDynamic.center_of_pressure(Rocket)

        ## skin friction coefficient
        Rocket.Cf = AeroDynamic.friction_Reynolds_model(velocity, Rocket)

        ## drag coefficient
        Rocket.Cd = AeroDynamic.zero_angle_of_attack_Cd(Rocket)

        ## drag: D
        RealTimeRocket.drag = AeroDynamic.drag_effect(Rocket, RealTimeRocket)

############################################################

    @classmethod
    def realtime_orientation(cls):
        ## orientation update
        orientation = Transformer.euler_to_orientation(RealTimeRocket.angular_state[:3])

        RealTimeRocket.orientation = orientation

############################################################

    @classmethod
    def realtime_rocket_mass(cls):
        propellant_mass = Rocket.propellant['mass']
        mass_flow_rate  = Rocket.propellant['mass_flow_rate']

        if propellant_mass > 0:
            propellant_mass -= mass_flow_rate * Dynamic.dt

        else:
            ## call stage seperation
            propellant_mass = 0.0

        Rocket.propellant['mass'] = propellant_mass

############################################################

    @classmethod
    def realtime_aoa(cls):

        ## velocity
        velocity = RealTimeRocket.linear_state[3:].reshape(3,)
        speed    = np.linalg.norm(velocity)

        ## orientation
        orientation = RealTimeRocket.orientation

        if speed == 0:
            RealTimeRocket.aoa = 0.0

        else:
            RealTimeRocket.aoa = acos(np.round(np.dot(velocity, orientation) / (speed), 8))

############################################################

    @classmethod
    def realtime_thrust(cls):
        propellant_mass = Rocket.propellant['mass']

        g   = Dynamic.g
        Isp = Rocket.propellant['Isp']
        exhaust_velocity = g * Isp

        mdot = (-1) * Rocket.propellant['mass_flow_rate']

        if propellant_mass > 0:
            ## thrust orientation: it's parallel to body roll axis
            thrust = exhaust_velocity * mdot

            RealTimeRocket.thrust = thrust * RealTimeRocket.orientation

        else:
            RealTimeRocket.thrust = np.zeros((3,1))

############################################################

    def rocket_stats() -> None:
        RealTimeRocket.aerodynamic_update()
        RealTimeRocket.realtime_thrust()

        rocket_stat = f"""
===========================================================

        1. Structure Data                                     \n
        mass    : {Rocket.mass}                               \n
        length  : {Rocket.length}                             \n
        diameter: {Rocket.diameter}                           \n
        inertia : {Rocket.inertia.reshape(3,)}                \n

        2. AeroDynamic Property                               \n
        center of gravity : {Rocket.CG}                       \n
        center of pressure: {Rocket.CP}                       \n

        3. Motor Performance                                  \n
        Isp           : {Rocket.propellant['Isp']}            \n
        mass flow rate: {Rocket.propellant['mass_flow_rate']} \n
        thrust        : {RealTimeRocket.thrust.reshape(3,)}   \n
===========================================================
        """

        print(rocket_stat)
