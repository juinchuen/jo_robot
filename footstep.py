from inverseKinematics import inverseKinematics
import numpy as np

import time
import hiwonder.Board as Board

ik = inverseKinematics(70)

pi = 3.1415

leg_position = np.zeros((32,3))

angles1 = np.zeros((32,10))

rest_height = 180

t = np.linspace(0,pi,17)
t = t[:-1]

# left leg positions
leg_position[:,0] = xy
leg_position[:,2] = xy
#leg_position[:13,1] = leg_position[:13,1]

angles1[:,:5] = ik.points2angles(leg_position, False)

leg_position[:,0] = [-stride]

angles1[:,5:] = ik.points2angles(leg_position, True)


## right leg positions
#leg_position[:,0] = [0, 0, 30, 60, 30, 0]
#leg_position[:,1] = [-10, -70, -70, -70, -10, 50]
#leg_position[:,2] = [-170, -170, -140, -170, -170, -170]

values = ik.angles2values(angles1)

servo_index = np.array([5, 4, 3, 2, 1, 13, 12, 11, 10, 9]).astype(int)

#while True:
#  ik.run_angles(values, 300)

ik.run_angles(values, 1000)
