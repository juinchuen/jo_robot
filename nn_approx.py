import numpy as np
import csv

class nn_approx:

    def __init__(self, angles_max, angles_min):
        self.angles_max = angles_max
        self.angles_min = angles_min

    def read_weights(self, file_name):
        with open(file_name, newline='') as f:
            rows = list(csv.reader(f))

        hidden_read = []
        hidden_read.append(np.array(rows[:4]).astype(int))
        hidden_read.append(np.array(rows[4:13]).astype(int))
        final_read = np.array(rows[13:]).astype(int)

        theta_read = [hidden_read, final_read]

        return theta_read

    def leaky_relu_q(self, a, alpha):
    
        red_mask = a < 0
    
        a[red_mask] = a[red_mask] >> 2
    
        return a

    def ff_nn_q(self, x, theta):

        x = x.astype(int)
       
        a = theta[0][0][0] + (np.dot(x, theta[0][0][1:]) >> 4)
        a = self.leaky_relu_q(a, 0.25).T
        a = a << 0

        a = theta[0][1][0] + (np.dot(a.T, theta[0][1][1:]) >> 4)
        a = self.leaky_relu_q(a, 0.25).T
        a = a >> 0

        a = theta[1][0] + (np.dot(a.T, theta[1][1:]) >> 4)
        a = self.leaky_relu_q(a, 0.25).T
        return a.T

    def squish(self, x):

        x_max = np.max(x, 0)
        x_min = np.min(x, 0)

        x = x - x_min

        up = x_max - x_min

        up[up==0] = 1

        x = x / up
        x = x - 0.5
        x = x * 2

        return x, x_max, x_min

    def squish_nonneg(self, x):

        x_max = np.max(x, 0)
        x_min = np.min(x, 0)

        x = x - x_min

        up = x_max - x_min

        up[up==0] = 1

        x = x / up

        return x, x_max, x_min

    def unsquish(self, x, x_max, x_min):

        x = x/2 + 0.5
        x = x * (x_max - x_min)
        x = x + x_min

        return x.astype(int)

    def unsquish_nonneg(self, x, x_max, x_min):

        x = x * (x_max - x_min)
        x = x + x_min

        return x.astype(int)