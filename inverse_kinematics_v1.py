import numpy as np

class inverseKinematics:

    def __init__(self, val):
        self.test = val

    def set_ft_dist(self, height):

        angles = np.zeros((5,np.size(height)))

        angles[2,:] = np.arccos((height * height - 59.8 * 59.8 - 59.3 * 59.3) / 2 / 59.8 / 59.3)

        angles[1,:] = np.arctan(59.8 * np.sin(angles[2,:]) / (59.8 * np.cos(angles[2,:]) + 59.3))

        angles[3,:] = angles[1,:] - angles[2,:]

        return angles

    def angles2values(self, angles):
        angles[1,:] = angles[1,:] + 0.3788
        angles[2,:] = angles[2,:] - 0.7382

        r_values = np.zeros((10,np.size(angles,1)))

        angles = angles / np.pi * 180 / 0.237

        # left leg values
        r_values[0,:] = 500;
        r_values[1,:] = 500 + angles[1];
        r_values[2,:] = 500 + angles[2];
        r_values[3,:] = 500 + angles[3];
        r_values[4,:] = 500;
    
        # right leg values
        r_values[5,:] = 500;
        r_values[6,:] = 500 - angles[1];
        r_values[7,:] = 500 - angles[2];
        r_values[8,:] = 500 - angles[3];
        r_values[9,:] = 500;

        r_values = np.around(r_values, decimals = 0).astype(int)

        return r_values

