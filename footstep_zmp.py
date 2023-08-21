from zmp import zmp

from inverseKinematics import inverseKinematics
import numpy as np

import time
#import hiwonder.Board as Board

z = zmp(hip_width = 94, sway = 85, stand_height = 170)
ik = inverseKinematics(70)

size = 20
hsize = int(size/2)

leg_position = z.gen_footsteps_simple(period = 0.5, stride = 50, lift_height = 40, repeat_N = 1, period_res = 10)

angles = np.zeros((size,10))

leg_position[:,0] = leg_position[:,0] - 5
leg_position[:,1] = leg_position[:,1] + 15

print(leg_position)

angles[:,:5] = ik.points2angles(leg_position, False)

leg_position[:,0] = -leg_position[:,0] - 10
leg_position[:,1] = leg_position[:,1] - 30

temp = 0.9999*leg_position[:hsize,2]

leg_position[:hsize,2] = leg_position[hsize:,2]
leg_position[hsize:,2] = temp

print(leg_position)

angles[:,5:] = ik.points2angles(leg_position, True)

print(angles)

values = ik.angles2values(angles)

print(values)

i = 0

#ik.run_angles(np.array([values[0,:]]), 1000)

while i < 10:
   # ik.run_angles(values, 50)
    i = i + 1

#ik.stand()

