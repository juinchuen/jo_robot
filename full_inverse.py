from inverseKinematics import inverseKinematics as ik
import numpy as np

import time
import hiwonder.Board as Board

def run_angles(angles, period):

  num_steps = np.size(angles, 0)

  for i in range(num_steps):

    for j in range(10):

      Board.setBusServoPulse(servo_index[j], angles[i, j], period)
      #print(servo_index[j], angles[i, j], period)

    time.sleep(period/1000)

t = np.linspace(0, 2 * np.pi, 20)

points = np.zeros((20,3))

points[:,0] = 20 * np.cos(t) - 20
points[:,1] = 30 * np.sin(t) + 30
points[:,2] = t - t - 150

C = ik(69)

A = np.zeros((20,10))

extend = np.zeros((20,10))
extend[:,:5] = C.points2angles(points, False)
extend[:,5:] = C.points2angles(points, True)

A = C.angles2values(extend)

A = np.squeeze(A)

servo_index = np.array([5, 4, 3, 2, 1, 13, 12, 11, 10, 9]).astype(int)

initial_sit = np.zeros((1,10))
initial_sit[0,:5] = C.set_ft_dist(100)
initial_sit[0,5:] = C.set_ft_dist(100)

print(np.shape(A))

run_angles(np.array([A[0,:]]), 500)

run_angles(A, 200)
