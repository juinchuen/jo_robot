import numpy as np
from nn_approx import nn_approx
from inverseKinematics import inverseKinematics
#import matplotlib.pyplot as plt
from zmp import zmp

a_max = np.array([603, 822, 803, 386, 603])
a_min = np.array([456, 662, 630, 227, 456])

nn = nn_approx(a_max, a_min)
z = zmp(hip_width = 94, sway = 70, stand_height = 180)
ik = inverseKinematics(70)

theta = nn.read_weights("weights.txt")

size = 20
hsize = int(size/2)

leg_position = z.gen_footsteps(period = 0.5, stride = 50, lift_height = 40, repeat_N = 1, period_res = 10)

leg_position[:,0] = leg_position[:,0] - 5
leg_position[:,1] = leg_position[:,1] + 15

[leg_position,_,_] = nn.squish_nonneg(leg_position)

leg_position = np.round(leg_position * 16).astype(int)

angles = nn.ff_nn_q(leg_position, theta)

#print(angles)

#plt.plot(angles)
#plt.plot(leg_position)

angles_offset = nn.unsquish(angles/16, a_max, a_min)

angles_offset = angles_offset.astype(int)

#print(angles_offset)

#plt.plot(angles_offset)

#plt.show()

angles_run = np.zeros((20,10))

angles_run[:,:5] = angles_offset

angles_run[:,5:] = angles_offset

angles_run[:,5:] = 1000 - angles_offset[:,:]

temp = np.zeros((10, 6))

temp[:,:-1] = angles_run[:10,5:]

angles_run[:10,5:] = angles_run[10:,5:]

angles_run[10:,5:] = temp[:,:-1]

angles_run = angles_run.astype(int)

while True:
    ik.run_angles(angles_run, 50)

#print(angles_run)