from zmp import zmp
import matplotlib.pyplot as plt
import numpy as np

z = zmp(hip_width = 94, sway = 70, stand_height = 180)
#ik = inverseKinematics(70)

period = 0.5 # seconds
stride = 50 # millimeters
lift_height = 40 # millimeters
repeat_N = 1
period_res = 10

leg_position = z.gen_footsteps(period, stride, lift_height, repeat_N, period_res)

leg_position_simple = z.gen_footsteps_simple(period, stride, lift_height, repeat_N, period_res)

#leg_position[:,0] = leg_position[:,0] - 5
#leg_position[:,1] = leg_position[:,1] + 15

t = np.linspace(0,1,21)
t = t[:-1]

#plt.plot(t, leg_position[:,0], c = "blue")

#plt.plot(t, leg_position[:,1], c = "blue")

#plt.plot(t, 48.4*np.sin(2*3.1415*t), c='red')

#plt.plot(t[:10], 100*t[:10]-25, c='red')

#plt.plot(t[10:], -100*t[10:]+75, c='red')

#plt.plot(t, leg_position[:,2], c = 'blue')

leg_position_repeat = np.zeros((40, 3))
leg_position_repeat[:20, :] = leg_position
leg_position_repeat[20:, :] = leg_position

leg_position_simple_repeat = np.zeros((40, 3))
leg_position_simple_repeat[:20, :] = leg_position_simple
leg_position_simple_repeat[20:, :] = leg_position_simple

t = np.linspace(0,2,40)

plt.plot(t, leg_position_repeat, c = 'blue')
plt.plot(t, leg_position_simple_repeat, c = 'red')

print(np.max(leg_position[:,1]))

plt.show()

