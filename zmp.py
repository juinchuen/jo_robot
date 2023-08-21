import numpy as np
#from inverseKinematics import inverseKinematics

class zmp:

    def __init__(self, hip_width, sway, stand_height):
        self.hips = hip_width
        self.sway = sway
        self.z = stand_height
        self.k = np.sqrt(9810/self.z)
        #self.ik = inverseKinematics(70)

    def gen_footsteps(self, period, stride, lift_height, repeat_N, period_res):

        leg_position = np.zeros((period_res * 2 * repeat_N, 3))

        t = np.linspace(-period/2, period/2, period_res + 1)

        leg_position[:period_res,1] = -(self.offset((self.hips/2/np.cosh(period*self.k/2))*np.cosh(self.k*t[:-1])) - self.hips/2)
        leg_position[period_res:2*period_res,1] = -leg_position[:period_res,1]

        A = stride*0.5*(1+np.exp(-self.k*period))/(np.exp(self.k*period) + np.exp(-self.k*period))
        B = -stride/2-A

        t = t + period/2

        leg_position[:period_res,0] = A * np.exp(self.k*t[:-1]) + B*np.exp(-self.k*t[:-1])
        
        leg_position[period_res:2*period_res,0] = -leg_position[:period_res,0]

        leg_position[:period_res,2] = -self.z + lift_height*np.sin(t[:-1]/period*3.1415)

        leg_position[period_res:2*period_res,2] = -self.z

        return leg_position

    def gen_footsteps_simple(self, period, stride, lift_height, repeat_N, period_res):

        leg_position = self.gen_footsteps(period, stride, lift_height, repeat_N, period_res)

        leg_position_simple = np.zeros((2*period_res, 3))

        amplitude = np.max(leg_position[:,1])

        leg_position_simple[:period_res, 0] = np.linspace(-stride/2, stride/2, period_res+1)[:-1]

        leg_position_simple[period_res:, 0] = np.linspace(stride/2, -stride/2, period_res+1)[:-1]

        leg_position_simple[:,1] = amplitude * np.sin(np.linspace(0, 2*3.1415, period_res * 2 + 1)[:-1])

        leg_position_simple[:,2] = leg_position[:,2]

        return leg_position_simple

    def offset(self, com):

        a = (1 + (2 * self.sway - self.hips)/self.hips)
        b = self.hips/2 - self.sway

        return a*com + b
        #return com