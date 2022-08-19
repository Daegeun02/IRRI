from Rocket.rocket             import Rocket
from Rocket.rocket_component   import *

import json



def load_rocket_data():
    with open('Rocket_Simulator/Rocket/rocket_data.json', 'r') as data:
        rocket_data = json.load(data)

    return rocket_data



class BuildRocket:

    ## constructor
    components = {
        "nosecone": NoseCone, 
        "bodytube": BodyTube,
        "fins"    : Fins,
        "motor"   : Motor
    }

    ## recipe
    rocket_data = load_rocket_data()

    num_stage   = len(rocket_data.keys())

###########################################################

    @staticmethod
    def build():
        if BuildRocket.num_stage == 1:
            BuildRocket.build_single_stage_rocket()

        else:
            # BuildRocket.build_multi_stage_rocket()
            pass

###########################################################

    @classmethod
    def build_single_stage_rocket(cls):
        Rocket.stage["stage1"] = Rocket()

        BuildRocket.build_stage(Rocket.stage["stage1"], BuildRocket.rocket_data['stage1'])

        print(Rocket.stage["stage1"])

###########################################################

    @classmethod
    def build_stage(cls, rocket, recipe):

        for component, data in reversed(recipe.items()):
            part = BuildRocket.components[component](data)


            rocket + part
