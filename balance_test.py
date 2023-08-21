from inverseKinematics import inverseKinematics
import numpy as np

import time
import hiwonder.Board as Board

ik = inverseKinematics(70)

pi = 3.1415

angles = np.zeros((1,10))

leg_pos = np.zeros((1,3))

is_left_step = False

# hip width is 65mm
sway = 40
stride = 30
y_offset = 10
rest_height = 210
step_height = 40

leg_pos = np.array([[0,-40,-200]])

angles[:,5:] = ik.points2angles(leg_pos, True)
angles[:,:5] = ik.points2angles(leg_pos, False)

values = ik.angles2values(angles)
ik.run_angles(values, 1000)

time.sleep(1)

time.sleep(1)

ik.stand()

