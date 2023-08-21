from inverseKinematics import inverseKinematics
from zmp import zmp
import numpy as np

import time
import hiwonder.Board as Board

############################
# DOES NOT WORK DO NOT RUN #
############################

ik = inverseKinematics(70)
z = zmp(64, 70, 180)

pi = 3.1415

leg_position = np.zeros((4,3))

values = np.zeros((8,10))

angles_left = np.zeros((4,10))
angles_right = np.zeros((4,10))

arm_values = np.zeros((8,2))

arm_values[:4,0] = np.ones(4) * 120
arm_values[:4,1] = np.ones(4) * 500

arm_values[4:,0] = np.ones(4) * 500
arm_values[4:,1] = np.ones(4) * 880

arm_values = np.around(arm_values, decimals = 0).astype(int)

is_left_step = False

# hip width is 65mm
sway = 70
stride = 20
y_offset = 0
rest_height = 190
step_height = 40

# left leg positions
leg_position[:,0] = [stride,                  0,            0,            0]
leg_position[:,1] = [y_offset,            -sway,        -sway,        -sway]
leg_position[:,2] = [-rest_height, -rest_height, -rest_height, -rest_height]

angles_right[:,:5] = ik.points2angles(leg_position, False)
angles_left[:,5:] = ik.points2angles(leg_position, False)

# right leg positions
leg_position[:,0] = [-stride,          -2*stride,                        0,         2*stride]
leg_position[:,1] = [-y_offset, -sway-2*y_offset,         -sway-2*y_offset, -sway-2*y_offset]
leg_position[:,2] = [-rest_height,  -rest_height, -rest_height+step_height,     -rest_height]

angles_right[:,5:] = ik.points2angles(leg_position, True)
angles_left[:,:5] = ik.points2angles(leg_position, True)

values[:4,:] = ik.angles2values(angles_left)
values[4:,:] = ik.angles2values(angles_right)

values = np.around(values, decimals = 0).astype(int)

period = 1500

def sigmoid(x):
    return 1/(np.exp(-x))

def interpolate_run(angles_curr, angles_prev, period):

    res = 5

    angle_diff = angles_curr - angles_prev

    scale = sigmoid(np.linspace(-5, 5, res))

    Board.setBusServoPulse(ik.servo_index[j], values[i, j], period)

    



while True:

    for i in range(8):

      for j in range(10):

        Board.setBusServoPulse(ik.servo_index[j], values[i, j], period)
        #print(servo_index[j], angles[i, j], period)

      #Board.setBusServoPulse(7, arm_values[i,0], period)
      #Board.setBusServoPulse(15, arm_values[i,1], period)

      time.sleep(period/1000)


