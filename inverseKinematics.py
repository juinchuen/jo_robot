import numpy as np
import time
#import hiwonder.Board as Board

class inverseKinematics:

    def __init__(self, val):
        # constructor method
        # val can be anything you want
        self.test = val
        self.servo_index = np.array([5, 4, 3, 2, 1, 13, 12, 11, 10, 9]).astype(int)

    def set_ft_dist(self, height):
        # private helper function
        # sets the distance between hip and ankle

        angles = np.zeros((np.size(height),5))

        angles[:,2] = np.arccos((height * height - 59.8 * 59.8 - 59.3 * 59.3) / 2 / 59.8 / 59.3)

        angles[:,1] = np.arctan(59.8 * np.sin(angles[:,2]) / (59.8 * np.cos(angles[:,2]) + 59.3))

        angles[:,3] = angles[:,1] - angles[:,2]

        return angles

    def points2angles(self, points, is_right_leg):
        # takes in x y z position of foot and returns angles of motors

        # positive x is forwards
        # positive y points along left arm (fully extended)
        # positive z is upwards, but z = 0 is at hip level

        ### DO NOT USE Z > -120, IK WILL FAIL AND ROBOT WILL CONTORT ###

        # works with np arrays
        # calculates one leg at a time
        # to calculate both legs, call function twice and change
        # is_right_leg boolean

        x = points[:,0]
        y = points[:,1]
        z = points[:,2]

        if is_right_leg:
            y = -y

        # net rotation around the x-axis is 0.
        angle_h = -np.arctan(y/z);

        # calculate position of ankle. Foot rotation does not change x position
        # of ankle
        y_a = y - 45.8 * np.sin(angle_h);
        z_a = z + 45.8 * np.cos(angle_h);

        # similarly, calculate bottom of hip position. hip rotation also does not
        # change x position of hip bottom
        y_h = 45.8 * np.sin(angle_h);
        z_h = - 45.8 * np.cos(angle_h);

        ft_dist = np.sqrt(x*x + (y_a - y_h)*(y_a - y_h) + (z_a - z_h)*(z_a - z_h));

        angles = self.set_ft_dist(ft_dist);

        angles[:,0] = angle_h;
        angles[:,4] = -angle_h;

        angle_ft = np.arcsin(x/ft_dist);

        angles[:,1] = angles[:,1] + angle_ft;
        angles[:,3] = angles[:,3] + angle_ft;
        
        return angles

    def angles2values(self, angles):
        # converts calculated angles into values that can be
        # sent to the robot
        # works with np arrays

        offset = 0.05

        angles[:,1] = angles[:,1] + 0.3788 - offset
        angles[:,2] = angles[:,2] - 0.7382 - offset

        angles[:,6] = angles[:,6] + 0.3788 - offset
        angles[:,7] = angles[:,7] - 0.7382 - offset

        r_values = np.zeros((np.size(angles,0), 10))

        angles = angles / np.pi * 180 / 0.237

        # left leg values
        r_values[:,0] = np.maximum(500 + angles[:,0], 400)
        r_values[:,1] = 500 + angles[:,1]
        r_values[:,2] = 500 + angles[:,2]
        r_values[:,3] = 500 + angles[:,3]
        r_values[:,4] = 500 - angles[:,4]
    
        # right leg values
        r_values[:,5] = np.minimum(500 - angles[:,5], 600)
        r_values[:,6] = 500 - angles[:,6]
        r_values[:,7] = 500 - angles[:,7]
        r_values[:,8] = 500 - angles[:,8]
        r_values[:,9] = 500 + angles[:,9]

        r_values = np.around(r_values, decimals = 0).astype(int)

        return r_values

    def run_angles(self, angles, period):
        # sends the servo values to the servo motors
        # period is in ms
        # input argument angles is actually values calculated by
        # self.angles2values()

        num_steps = np.size(angles, 0)

        for i in range(num_steps):

          for j in range(10):

             Board.setBusServoPulse(self.servo_index[j], angles[i, j], period)
             #print(servo_index[j], angles[i, j], period)

          time.sleep(period/1000)

    def stand(self):
        # convenience function to stand straight
        self.run_angles(self.angles2values(np.zeros((1,10))), 1000)

    def run_angle_id(self, id, angle, period):
        # move specific servo specified by input arg id
        # period is in ms
        # angle is a number from 0 to 1000
        # angle limits are not set, servo may try to move to impossible locations
        Board.setBusServoPulse(id, angle, period)

    def run_angles_single(self, angles, period, is_right_leg):
        # run angles for a single leg
        ### NOT TESTED, DO NOT USE ###

        offset = 0

        if (is_right_leg):
            offset = 5

        num_steps = np.size(angles, 0)

        for i in range(num_steps):

          for j in range(5):

            Board.setBusServoPulse(self.servo_index[j + offset], angles[i, j], period)
            #print(servo_index[j], angles[i, j], period)

          time.sleep(period/1000)

