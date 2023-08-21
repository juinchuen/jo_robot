from inverseKinematics import inverseKinematics
import numpy as np

import time
#import hiwonder.Board as Board

ik = inverseKinematics(70)

values = ik.angles2values(np.zeros((1,10)))

#ik.run_angles(values, 1000)

print(values)


