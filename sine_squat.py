from inverseKinematics import inverseKinematics as ik
import numpy as np

import hiwonder.Board as Board
import time

def run_angles(angles, period):

  num_steps = np.size(angles, 0)

  for i in range(num_steps):

    for j in range(10):

      Board.setBusServoPulse(servo_index[j], angles[i, j], period)

    time.sleep(period/1000)

t = np.linspace(0, 2 * np.pi, 20)

heights = 20 * np.cos(t) + 65

C = ik(69)

A = np.zeros((20,10))

A[:,:5] = C.angles2values(C.set_ft_dist(heights))
A[:,5:] = A[:,:5]

servo_index = np.array([5, 4, 3, 2, 1, 13, 12, 11, 10, 9]).astype(int)

print(servo_index[3])

#run_angles(C.angles2values(C.set_ft_dist(90)), 500)

run_angles(A, 50)
