from inverseKinematics import inverseKinematics
import numpy as np
import walkGenerator

import time
#import hiwonder.Board as Board

def run_angles(angles, period):

  num_steps = np.size(angles, 0)

  for i in range(num_steps):

    for j in range(10):


       #Board.setBusServoPulse(servo_index[j], angles[i, j], period)
       #print(servo_index[j], angles[i, j], period)

     time.sleep(period/1000)

ik = inverseKinematics(70)

leg_position = np.zeros((1,3))

angles1 = np.zeros((1,10))

rest_height = 160

# hip width is 65mm
sway = 40

leg_position[:,0] = 0
leg_position[:,1] = 0
leg_position[:,2] = -rest_height

angles1[:,:5] = ik.points2angles(leg_position, False)

leg_position[:,0] = 0
leg_position[:,1] = 0
leg_position[:,2] = -rest_height

angles1[:,5:] = ik.points2angles(leg_position, True)

values = ik.angles2values(angles1)

servo_index = np.array([5, 4, 3, 2, 1, 13, 12, 11, 10, 9]).astype(int)

#run_angles(values, 1000)

print (values)

