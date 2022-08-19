import numpy as np

from math import sqrt



class AeroDynamic:

    tempreture = 0      # K
    pressure   = 0

    zero_aoa_Cd = 0

    ## viscous
    viscousity  = 1.7854 * 1e-5     # kg s / m

    ## density
    rho = 1.225                     # kg / m^3

    ## Critical Reynold's number
    RN_cr = 500000

###########################################################

    @classmethod
    def air_pressure(cls, altitude) -> None:
        P = (1 - ((altitude / 1000) / 145.45))
        pass

###########################################################

    @classmethod
    def air_density(cls, altitude) -> None:

        AeroDynamic.rho = 1.225 * (1-2.256e-5*altitude)**5.256


###########################################################

    ## update Reynold's number
    @classmethod
    def aero_situation(cls, velocity, length) -> int:
        speed = np.linalg.norm(velocity)

        ## rho * v * l / mu
        RN = int(AeroDynamic.rho * speed * length / AeroDynamic.viscousity)

        return RN

###########################################################

    @classmethod
    def friction_Reynolds_model(cls, velocity, rocket) -> float:
        l     = rocket.length
        speed = np.linalg.norm(velocity)

        Cf = 0.0

        ## not in any layer
        if speed == 0:
            return Cf

        ## at least in any layer
        else:
            x_cr = (AeroDynamic.RN_cr * AeroDynamic.viscousity) / (AeroDynamic.rho * speed)
        
        ## no transition, only laminar flow layer
        if l < x_cr:
            RN_L = AeroDynamic.aero_situation(speed, l)

            Cf = 1.328 / RN_L ** (1/2)

        ## transition exist
        else:
            RN_T = AeroDynamic.aero_situation(speed,    l)
            RN_L = AeroDynamic.aero_situation(speed, x_cr)

            Cf_T = 0.074 / RN_T ** (1/5)
            Cf_L = 1.328 / RN_L ** (1/2)

            Cf = Cf_T - Cf_T * (x_cr/l) + Cf_L * (x_cr/l)

        return Cf

###########################################################

    @staticmethod
    def zero_angle_of_attack_Cd(rocket) -> float:
        propellant_mass = rocket.propellant['mass']

        Cd_nc = rocket.aerodynamic['Cd']['nosecone']
        Cd_bt = rocket.aerodynamic['Cd']['bodytube']
        Cd_b  = rocket.aerodynamic['Cd']['motor']

        crs_a = rocket.aerodynamic['crs_area']

        Sw_nc = rocket.aerodynamic['wet_area']['nosecone']
        Sw_bt = rocket.aerodynamic['wet_area']['bodytube']

        Ld = rocket.length / rocket.diameter

        Cd_ncbt   = 1.02 * rocket.Cf * (1+1.5/Ld**1.5) * (Sw_nc+Sw_bt) / crs_a

        if propellant_mass > 0:
            Cd_m = 0
        else:
            Cd_m = 0.029 / sqrt(Cd_ncbt)

        Cd_ = Cd_ncbt + Cd_m

        AeroDynamic.zero_aoa_Cd = Cd_

        return Cd_

###########################################################

    @staticmethod
    def center_of_pressure(rocket) -> float:
        aerodynamic = rocket.aerodynamic

        CP       = aerodynamic['CP']
        wet_area = aerodynamic['wet_area']

        CP_ = 0
        Sw_ = 0

        for component in CP.keys():
            Cp = CP[component]
            Sw = wet_area[component]

            CP_ += Cp * Sw
            Sw_ += Sw

        return CP_ / Sw_

###########################################################

    @staticmethod
    def drag_coefficient(motor, Cd) -> float:
        Cd_ = AeroDynamic.zero_aoa_Cd

        return Cd_

###########################################################

    @staticmethod
    def drag_effect(rocket, realtimerocket):
        Sw_bt = rocket.aerodynamic["wet_area"]["bodytube"]

        velocity = realtimerocket.linear_state[3:]
        speed = np.linalg.norm(velocity)

        drag = (-1) * (1/2) * AeroDynamic.rho * rocket.Cd * speed * Sw_bt * velocity

        return drag
