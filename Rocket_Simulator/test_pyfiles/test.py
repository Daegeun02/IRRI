from transformer import Transformer
from rocket      import Rocket
from rocket_status import RealTimeRocket

import numpy             as np
import matplotlib.pyplot as plt

## roll > yaw   > pitch
## yaw  > pitch > roll
Rocket.angular_state[:3] = np.deg2rad(np.array([10,0,0])).reshape(3,1)
Rocket.linear_state[3:] = np.array([[0, 0, 80]]).reshape(3,1)

Rocket.orientation = Transformer.euler_to_orientation(Rocket.angular_state[:3])

# print(Rocket.orientation)

# RealTimeRocket.realtime_status_update()

# moment = np.cross(Rocket.orientation.reshape(3,), Rocket.linear_state[3:].reshape(3,)).reshape(3,1)

# print(Rocket.inertia)
# print(moment / Rocket.inertia)

# print("Fantasitic!!")

"""
ax = plt.figure(figsize=(3,3)).add_subplot(projection="3d")

ax.quiver(0,0,0,1,0,0, length=0.05, color="r")
ax.quiver(0,0,0,0,1,0, length=0.05, color="g")
ax.quiver(0,0,0,0,0,1, length=0.05, color="b")

ax.quiver(0,0,0,orientation[0], orientation[1], orientation[2], length=0.05, color="black")

plt.xlabel("x")
plt.ylabel("y")

plt.show()
"""