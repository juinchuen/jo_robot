from zmp import zmp

from inverseKinematics import inverseKinematics
import numpy as np
import matplotlib.pyplot as plt
import time

z = zmp(hip_width = 94, sway = 85, stand_height = 170)
ik = inverseKinematics(70)

S = 120
D = 94
E = 33.5
g = 9810
z = 180
k = np.sqrt(g/z)

over_lap = 0.025

lift = 30

t = np.linspace(-0.5, 0.5, 41)
t = t[:-1]

leg_position = np.zeros((40, 6))

#print(t)

leg_position[:20,0]   = -S/2*np.exp( k*t[:20])

leg_position[20:21,0] = S/2*np.exp(-k*t[20:21]) - S

leg_position[21:, 0] = S*(0.5*np.exp(-k*over_lap) - 1) * np.exp(-k*(t[21:] - over_lap))

#plt.plot(leg_position[:,0])

#plt.show()

s2s = np.zeros(40)
s2s[:20] =  D/2*np.exp( k*t[:20])
s2s[20:] = -D/2*np.exp(-k*t[20:]) + D

leg_position[:,1] = s2s + 2 * E / D * (s2s - D/2) - 32

leg_position[:20,2] = -z

leg_position[20:,2] = -z + lift

leg_position[21,2] = - z

##################################################################

angles = np.zeros((40, 10))

angles[:,:5] = ik.points2angles(leg_position[:,:3], False)

##################################################################

for i in range(40):
    leg_position[i,3] = -leg_position[39 - i,0]

leg_position[:,4] = leg_position[:,1] - 30

leg_position[:20,5] = -z + lift

leg_position[20:,5] = -z

angles[:,5:] = ik.points2angles(leg_position[:,3:], True)

values = ik.angles2values(angles)

#print(values)

##################################################################

ik.run_angles(np.array([values[0,:]]), 1000)

values[21,3] = values[21,3] + 200

ik.run_angles(values, 25)

#for i in range(10,35):

#    ik.run_angles(np.array([values[i,:]]), 200)
#    print(i)
#    time.sleep(2)

ik.run_angles(np.array([values[-1,:]]), 1000)

ik.stand()

