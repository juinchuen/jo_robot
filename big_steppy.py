from zmp import zmp

from inverseKinematics import inverseKinematics
import numpy as np
#import matplotlib.pyplot as plt
import time

z = zmp(hip_width = 94, sway = 85, stand_height = 170)
ik = inverseKinematics(70)

S = 140
D = 94
E = 33.5
g = 9810
z = 180
k = np.sqrt(g/z)

leg_share = 1;

t = np.linspace(-0.5, 0.5, 41)
t = t[:-1]

leg_position = np.zeros((40, 3))

leg_position[:20,0] = -S/2*np.exp( k*t[:20])
leg_position[20:,0] = -S/2*np.exp(-k*t[20:])

s2s = np.zeros(40)
s2s[:20] =  D/2*np.exp( k*t[:20])
s2s[20:] = -D/2*np.exp(-k*t[20:]) + D

leg_position[:,1] = s2s + 2 * E / D * (s2s - D/2) - 32

leg_position[:(20 + leg_share),2] = -z

leg_position[(20 + leg_share):,2] = -z

#################################################################

angles = np.zeros((40, 10))

angles[:,:5] = ik.points2angles(leg_position, False)

leg_position[:,0] = -leg_position[:,0]

leg_position[:,1] = leg_position[:,1] - 30

leg_position[:(20 - leg_share),2] = -z

leg_position[(20 - leg_share):,2] = -z

angles[:,5:] = ik.points2angles(leg_position, True)

values = ik.angles2values(angles)

#print(values)

#################################################################

ik.run_angles(np.array([values[0,:]]), 1000)

ik.run_angles(values, 1000)

ik.run_angles(np.array([values[-1,:]]), 1000)

ik.stand()

