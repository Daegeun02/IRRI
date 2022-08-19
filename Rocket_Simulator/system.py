from visualizer 			import Visualizer
from Rocket.rocket       	import Rocket
from rocket_status 			import RealTimeRocket

import numpy as np
import matplotlib.pyplot as plt
import json

def load_launch_data():
	with open('Rocket_Simulator/launch_data.json') as data:
		launch_data = json.load(data)
	
	return launch_data



class System:

	MISSION_TIME = 10

	launch_data = load_launch_data()
	
	def __init__(self):

		## initialize intime
		RealTimeRocket.t = 0

		## set launch angle
		RealTimeRocket.set_launch_angle(System.launch_data)

		## visualize
		self.visualize = Visualizer()
	

############################################################

	def launch(self):
		## status update
		RealTimeRocket.realtime_status_update()

		# ## real time
		# print(f"=====ON AIR=====")
		# print(f"MISSION TIME: {round(RealTimeRocket.t, 4)} s")

		# ## position
		# print(f"position: {np.round(RealTimeRocket.linear_state[:3].reshape(3,), 3)}")

		# ## orientation
		# print(f"orientation: {np.round(RealTimeRocket.orientation.reshape(3,), 3)}")

		# print("\n")

		# self.visualize.position_data(System.MISSION_TIME)
		# self.visualize.drag_data(System.MISSION_TIME)
		# self.visualize.orientation_data(System.MISSION_TIME)
		# self.visualize.angle_of_attack_data(System.MISSION_TIME)
		self.visualize.monitoring()



if __name__ == "__main__":
	rocket = System()

	RealTimeRocket.rocket_stats()


	# while RealTimeRocket.t < System.MISSION_TIME:

	# 	rocket.launch()

	# ## real time
	# print(f"=====ON AIR=====")
	# print(f"MISSION TIME: {round(RealTimeRocket.t, 4)} s")

	# ## position
	# print(f"position: {np.round(RealTimeRocket.linear_state[:3].reshape(3,), 3)}")

	# ## orientation
	# print(f"orientation: {np.round(RealTimeRocket.orientation.reshape(3,), 3)}")

	# print("\n")
	# plt.show()
