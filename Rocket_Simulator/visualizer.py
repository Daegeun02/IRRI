from Rocket.rocket      import Rocket
from rocket_status      import RealTimeRocket

import matplotlib.pyplot as plt
import numpy as np

from mpl_toolkits.mplot3d import axes3d
from math                 import pi



class Visualizer:

    DOF  = 6
    axis = 3

    position    = {0: "position_x", 
                   1: "position_y",
                   2: "position_z", 
                   3: "velocity_x",
                   4: "velocity_y", 
                   5: "velocity_z"}

    orientation = {0: "orientation_x",
                   1: "orientation_y",
                   2: "orientation_z"}
                   
    drag        = {0: "drag_x",
                   1: "drag_y",
                   2: "drag_z"}

    limit       = {0: (-100,100),
                   1: (-100,100),
                   2: (-200,200),
                   3: ( -20, 20),
                   4: ( -20, 20),
                   5: ( -50, 50)}

    mode = None

###########################################################

    def __init__(self, mode="monitoring"):
        Visualizer.mode = mode

        if Visualizer.mode == "monitoring":
            plt.subplot(1,1,1, projection="3d")

            plt.gca().set_xlim(-15,15)
            plt.gca().set_ylim(-15,15)
            plt.gca().set_zlim(-10,10)

            plt.quiver(0,0,0,1,0,0,length=5,color='red')
            plt.quiver(0,0,0,0,1,0,length=5,color='green')
            plt.quiver(0,0,0,0,0,1,length=5,color='blue')

        else:
            pass

###########################################################

    def position_data(self, mission_time):

        t = RealTimeRocket.t

        ## position
        for idx in range(Visualizer.axis):
            data = Rocket.linear_state[idx]

            plt.subplot(2,3,idx+1)
            plt.title(Visualizer.position[idx])
            plt.xlabel("MISSION TIME (s)")
            plt.ylabel("m")

            plt.xlim(0,mission_time)
            plt.ylim(Visualizer.limit[idx])

            plt.grid()

            plt.scatter(t,data)

        ## velocity
        for idx in range(Visualizer.axis):
            data = Rocket.linear_state[idx+3]

            plt.subplot(2,3,idx+4)
            plt.title(Visualizer.position[idx+3])
            plt.xlabel("MISSION TIME (s)")
            plt.ylabel("m/s")

            plt.xlim(0,mission_time)
            plt.ylim(Visualizer.limit[idx+3])

            plt.scatter(t,data)


        plt.pause(0.125)

###########################################################

    def drag_data(self, mission_time):

        t = RealTimeRocket.t

        ## position
        for idx in range(Visualizer.axis):
            data = RealTimeRocket.drag[idx]

            plt.subplot(2,3,idx+1)
            plt.title(Visualizer.drag[idx])
            plt.xlabel("MISSION TIME (s)")
            plt.ylabel("N")

            plt.xlim(0,mission_time)
            plt.ylim(Visualizer.limit[idx])

            plt.grid()

            plt.scatter(t,data)

        ## velocity
        for idx in range(Visualizer.axis):
            data = RealTimeRocket.linear_state[idx+3]

            plt.subplot(2,3,idx+4)
            plt.title(Visualizer.position[idx+3])
            plt.xlabel("MISSION TIME (s)")
            plt.ylabel("m/s")

            plt.xlim(0,mission_time)
            plt.ylim(Visualizer.limit[idx+3])

            plt.scatter(t,data)


        # plt.pause(0.125)

###########################################################

    def orientation_data(self, mission_time):

        t = RealTimeRocket.t

        for i in range(Visualizer.axis):
            data = RealTimeRocket.orientation[i]

            plt.subplot(1,3,i+1)
            plt.title(Visualizer.orientation[i])
            plt.xlabel("MISSION TIME (s)")

            plt.xlim(0,mission_time)
            plt.ylim(-1.0,1.0)
            
            plt.scatter(t, data)

        # plt.pause(0.125)

###########################################################

    def angle_of_attack_data(self, mission_time):

        t = RealTimeRocket.t

        data = RealTimeRocket.aoa

        plt.subplot(1,1,1)

        plt.title("angle_of_attack")
        plt.xlabel("MISSION TIME (s)")

        plt.xlim(0,mission_time)
        plt.ylim(-pi, pi)

        plt.scatter(t, data)

################################################

    def monitoring(self):
        position    = RealTimeRocket.linear_state[:3]
        orientation = RealTimeRocket.orientation

        thrust = RealTimeRocket.thrust

        plt.cla()
        plt.gca().set_xlim( -50, 50)
        plt.gca().set_ylim( -50, 50)
        plt.gca().set_zlim(   0,100)

        plt.quiver(position[0], position[1], position[2],\
                   orientation[0], orientation[1], orientation[2],\
                   length=7, linewidth=2.0, arrow_length_ratio=0.0, color='black')
        
        plt.quiver(position[0], position[1], position[2],\
                   -thrust[0], -thrust[1], -thrust[2],\
                   length=0.05, linewidth=1.5, arrow_length_ratio=0.0, color='red')

        plt.pause(0.125)