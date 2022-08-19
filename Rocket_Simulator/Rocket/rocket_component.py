import numpy as np

from math import sqrt, pi



class RocketComponents:
    def __init__(self, data):
        self.data = data
        
###########################################################

    @staticmethod
    def center_of_gravity(stage, component) -> float:
        CG1     = stage.CG
        mass1   = stage.mass
        length1 = stage.length
        Ixdm1   = mass1 * CG1

        mass2   = component.data['mass']
        length2 = component.data['length']
        Ixdm2   = component.center_of_gravity()

        Ixdm = Ixdm1 + Ixdm2 * (2*length1/length2 + 1)
        CG   = Ixdm / (mass1 + mass2)

        return CG

###########################################################

    @staticmethod
    def inertia(rocket) -> float:
        inertia = np.zeros((3,1))

        r = rocket.diameter / 2
        l = rocket.length
        c = rocket.CG

        ## about rocket coordinate
        inertia1 = (1/4) * rocket.mass * r*r
        inertia2 = (1/3) * rocket.mass * (l*l - 3*c*l + 3*c*c)

        inertia[0] = inertia1 * 2
        inertia[1] = inertia1 + inertia2
        inertia[2] = inertia1 + inertia2

        return inertia

###########################################################

    @staticmethod
    def cross_section_area(component) -> float:
        r = component.data['diameter'] / 2

        crs_area = r * r * pi

        return crs_area

###########################################################
###########################################################
###########################################################

class NoseCone(RocketComponents):

    part_name = "nosecone"
    
    def __init__(self, data):
        super().__init__(data)

    def center_of_gravity(self) -> float:
        Ixdm = 3 * self.data['CG'] * self.data['mass']

        return Ixdm

    def wet_area(self) -> float:
        l = self.data['length']
        r = self.data['diameter'] / 2

        generatrix = sqrt(r*r + l*l)

        Sw = pi * r * generatrix

        return Sw

###########################################################

class BodyTube(RocketComponents):

    part_name = "bodytube"

    def __init__(self, data):
        super().__init__(data)

    def center_of_gravity(self) -> float:
        Ixdm = self.data['CG'] * self.data['mass']

        return Ixdm

    def wet_area(self) -> float:
        l = self.data['length']
        r = self.data['diameter'] / 2

        Sw = 2*pi*r * l

        return Sw

###########################################################

class Fins(RocketComponents):

    part_name = "fins"

    def __init__(self, data):
        super().__init__(data)

    def center_of_gravity(self) -> float:
        Ixdm = self.data['CG'] * self.data['mass']

        return Ixdm

    def wet_area(self) -> float:
        l = self.data['length']
        r = self.data['diameter'] / 2

        Sw = 2*pi*r * l

        return Sw

###########################################################

class Motor(RocketComponents):

    part_name = "motor"

    def __init__(self, data):
        super().__init__(data)
    
    def center_of_gravity(self) -> float:
        Ixdm = self.data['CG'] * self.data['mass']

        return Ixdm

    def wet_area(self) -> float:
        l = self.data['length']
        r = self.data['diameter'] / 2

        Sw = 2*pi*r * l

        return Sw
