'''
by Einsbon (Sunbin Kim)
- GitHub: https://github.com/Einsbon
- Youtube:  https://www.youtube.com/channel/UCt7FZ-8uzV_jHJiKp3NlHvg
- Blog: https://blog.naver.com/einsbon



Robot's forward is direction X +
        left is Y+
        up is Z +
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import math


class WalkGenerator():
    def __init__(self):
        #                                      0   1   2   3   4   5 
        self._motorDirectionRight = np.array([+1, +1, +1, +1, +1, +1])
        self._motorDirectionLeft = np.array([+1, +1, +1, +1, +1, +1])
        '''
        self._walkPoint0 = 0  # double support. point of the landed foot
        self._walkPoint1 = 0  # single support. point of the supporting foot
        self._walkPoint2 = 0  # double support. point of the foot to lift.
        self._walkPoint3 = 0  # single support. point of the swinging foot
        '''
        '''
        self.walkPointStartRightstepRightLeg = 0  # 오른쪽 발을 먼저 내밈. 그때의 오른쪽 발.
        self.walkPointStartRightstepLeftLeg = 0  # 오른쪽 발을 먼저 내밈. 그때의 왼쪽 발.

        self.walkPointStartLeftstepRightLeg = 0  # 왼쪽 발을 먼저 내밈. 그때의 오른쪽 발.
        self.walkPointStartLeftstepLeftLeg = 0  # 왼쪽 발을 먼저 내밈. 그때의 왼쪽 발.

        self.walkPointEndRightstepRightLeg = 0  # 오른쪽 발을 디디면서 끝남. 그때의 오른쪽 발.
        self.walkPointEndLeftstepRightLeg = 0  # 오른쪽 발을 디디면서 끝남. 그때의 왼쪽 발.
        self.walkPointEndLeftstepLeftLeg = 0
        self.walkPointEndRightstepLeftLeg = 0
        
        self.walkPointRightStepRightLeg = 0
        self.walkPointLeftStepRightLeg = 0

        self.walkPointRightStepLeftLeg = 0
        self.walkPointLeftStepLeftLeg = 0

        self.walkAnglesWalkingRight = 0
        self.walkAnglesWalkingLeft = 0
        self.walkAnglesStartRight = 0  # 왼쪽으로 sway 했다가 오른발을 먼저 내밈.
        self.walkAnglesStartLeft = 0  # 오른쪽으로 sway 했다가 왼발을 먼저 내밈.
        self.walkAnglesEndRight = 0  # 오른발을 디디면서 끝남.
        self.walkAnglesEndLeft = 0  # 왼발을 디디면서 끝남.

        self.turnListUnfold = 0
        self.turnListFold = 0
        '''
        # 로봇의 길이 설정. 길이 단위: mm
        self._pelvic_interval = 70.5
        self._legUp_length = 110
        self._legDown_length = 110
        self._footJoint_to_bottom = 45
        '''
        self._bodyMovePoint = 0
        self._legMovePoint = 0
        self._h = 0
        self._l = 0
        self._sit = 0
        self._swayBody = 0
        self._swayFoot = 0
        self._swayShift = 0
        self._liftPush = 0
        self._landPull = 0
        self._stepTime = 0
        self._bodyPositionXPlus = 0
        self._damping = 0
        self._incline = incline
        '''

    def setRobotParameter(self, pelvic_interval, leg_up_length, leg_down_length, foot_to_grount, foot_to_heel, foot_to_toe):
        pass

    def setWalkParameter(self, bodyMovePoint, legMovePoint, height, stride, sit, swayBody, swayFoot, bodyPositionForwardPlus, swayShift, liftPush=0.4, landPull=0.6, timeStep=0.1, damping=0, incline=0):
        self._bodyMovePoint = bodyMovePoint # the number of point when two feet are landed
        self._legMovePoint = legMovePoint   # the number of point when lift one foot
        self._h = height                    # foot lift height
        self._l = stride                    # stride length
        self._sit = sit                     # sit height. increase this will make leg more fold. too high or too low makes an error
        self._swayBody = swayBody           # body sway length
        self._swayFoot = swayFoot           # foot sway length. 0 -> feet move straight forward. plus this make floating leg spread.(increase gap between feet)
        self._swayShift = swayShift         # start point of sway
        self._liftPush = liftPush           # push the lifting foot backward when lifting the foot to gains momentum.
        self._landPull = landPull           # Before put the foot down, go forward more and pull back when landing.
        self._timeStep = timeStep           # simulation timeStep
        self._bodyPositionXPlus = bodyPositionForwardPlus  # plus this makes the body forward
        self._damping = damping             # damping at the start and end of foot lift.
        self._incline = incline             # tangent angle of incline

        self._stepPoint = bodyMovePoint + legMovePoint

    def generate(self):
        walkPoint = self._bodyMovePoint * 2 + self._legMovePoint * 2
        trajectoryLength = self._l * (2 * self._bodyMovePoint + self._legMovePoint) / (self._bodyMovePoint + self._legMovePoint)

        walkPoint0 = np.zeros((3, self._bodyMovePoint))
        walkPoint1 = np.zeros((3, self._legMovePoint))
        walkPoint2 = np.zeros((3, self._bodyMovePoint))
        walkPoint3 = np.zeros((3, self._legMovePoint))

        self.walkPointStartRightstepRightLeg = np.zeros((3, self._bodyMovePoint + self._legMovePoint))
        self.walkPointStartLeftstepRightLeg = np.zeros((3, self._bodyMovePoint + self._legMovePoint))
        self.walkPointEndRightstepRightLeg = np.zeros((3, self._bodyMovePoint + self._legMovePoint))
        self.walkPointEndLeftstepRightLeg = np.zeros((3, self._bodyMovePoint + self._legMovePoint))

        # walking motion
        for i in range(self._bodyMovePoint):
            t = (i + 1) / (walkPoint - self._legMovePoint)
            walkPoint0[0][i] = -trajectoryLength * (t - 0.5)
            walkPoint0[2][i] = self._sit
            walkPoint0[1][i] = self._swayBody * math.sin(2 * math.pi * ((i + 1 - self._swayShift) / walkPoint))

        for i in range(self._legMovePoint):
            t = (i + 1 + self._bodyMovePoint) / (walkPoint - self._legMovePoint)
            walkPoint1[0][i] = -trajectoryLength * (t - 0.5)
            walkPoint1[2][i] = self._sit
            walkPoint1[1][i] = self._swayBody * math.sin(2 * math.pi * ((i + 1 + self._bodyMovePoint - self._swayShift) / walkPoint))

        for i in range(self._bodyMovePoint):
            t = (i + 1 + self._bodyMovePoint + self._legMovePoint) / (walkPoint - self._legMovePoint)
            walkPoint2[0][i] = -trajectoryLength * (t - 0.5)
            walkPoint2[2][i] = self._sit
            walkPoint2[1][i] = self._swayBody * math.sin(2 * math.pi * ((i + 1 + self._bodyMovePoint + self._legMovePoint - self._swayShift) / walkPoint))

        for i in range(self._legMovePoint):
            t = (i + 1) / self._legMovePoint
            sin_tpi = math.sin(t * math.pi)

            walkPoint3[0][i] = (2 * t - 1 + (1 - t) * self._liftPush * -sin_tpi + t * self._landPull * sin_tpi) * trajectoryLength / 2
            walkPoint3[2][i] = math.sin(t * math.pi) * self._h + self._sit
            walkPoint3[1][i] = math.sin(t * math.pi) * self._swayFoot + self._swayBody * math.sin(2 * math.pi * ((i + 1 + walkPoint - self._legMovePoint - self._swayShift) / walkPoint))

        # starting motion
        for i in range(self._bodyMovePoint - self._swayShift):
            t = (i + 1) / self._bodyMovePoint
            self.walkPointStartRightstepRightLeg[0][i] = 0
            self.walkPointStartRightstepRightLeg[2][i] = self._sit

            self.walkPointStartLeftstepRightLeg[0][i] = 0
            self.walkPointStartLeftstepRightLeg[2][i] = self._sit

        for i in range(self._legMovePoint):
            t = (i + 1) / self._legMovePoint
            t2 = (i + 1) / (self._legMovePoint + self._swayShift)
            sin_tpi = math.sin(t * math.pi)

            self.walkPointStartRightstepRightLeg[2][i + self._bodyMovePoint - self._swayShift] = math.sin(t * math.pi) * self._h + self._sit
            self.walkPointStartRightstepRightLeg[0][i + self._bodyMovePoint - self._swayShift] = (2 * t + (1 - t) * self._liftPush * -sin_tpi + t * self._landPull * sin_tpi) * trajectoryLength / 4
            self.walkPointStartLeftstepRightLeg[0][i + self._bodyMovePoint - self._swayShift] = (math.cos(t2 * math.pi / 2) - 1) * trajectoryLength * self._legMovePoint / (self._bodyMovePoint * 2 + self._legMovePoint) / 2
            self.walkPointStartLeftstepRightLeg[0][i + self._bodyMovePoint - self._swayShift] = (math.cos(t2 * math.pi / 2) - 1) * trajectoryLength * ((self._swayShift + self._bodyMovePoint + self._legMovePoint) / (self._bodyMovePoint * 2 + self._legMovePoint) - 0.5)

            self.walkPointStartLeftstepRightLeg[2][i + self._bodyMovePoint - self._swayShift] = self._sit

        for i in range(self._swayShift):
            t2 = (i + 1 + self._legMovePoint) / (self._legMovePoint + self._swayShift)

            self.walkPointStartRightstepRightLeg[0][i + self._legMovePoint + self._bodyMovePoint - self._swayShift] = -trajectoryLength * ((i + 1) / (walkPoint - self._legMovePoint) - 0.5)
            self.walkPointStartRightstepRightLeg[2][i + self._legMovePoint + self._bodyMovePoint - self._swayShift] = self._sit
            self.walkPointStartLeftstepRightLeg[0][i + self._legMovePoint + self._bodyMovePoint - self._swayShift] = -trajectoryLength * ((i + 1 + self._bodyMovePoint + self._legMovePoint) / (walkPoint - self._legMovePoint) - 0.5)
            self.walkPointStartLeftstepRightLeg[0][i + self._legMovePoint + self._bodyMovePoint - self._swayShift] = (math.cos(t2 * math.pi / 2) - 1) * trajectoryLength * ((self._swayShift + self._bodyMovePoint + self._legMovePoint) / (self._bodyMovePoint * 2 + self._legMovePoint) - 0.5)
            self.walkPointStartLeftstepRightLeg[2][i + self._legMovePoint + self._bodyMovePoint - self._swayShift] = self._sit

        for i in range(self._bodyMovePoint + self._legMovePoint):
            t = (i + 1) / (self._bodyMovePoint + self._legMovePoint)
            #self.walkPointStartRightstepRightLeg[1][i] = -self._swayBody * math.sin(t*math.pi) * math.sin(t*math.pi)
            #self.walkPointStartLeftstepRightLeg[1][i] = self._swayBody * math.sin(t*math.pi) * math.sin(t*math.pi)
            if t < 1 / 4:
                self.walkPointStartRightstepRightLeg[1][i] = -self._swayBody * (math.sin(t * math.pi) - (1 - math.sin(math.pi * 2 * t)) * (math.sin(4 * t * math.pi) / 4))
                self.walkPointStartLeftstepRightLeg[1][i] = self._swayBody * (math.sin(t * math.pi) - (1 - math.sin(math.pi * 2 * t)) * (math.sin(4 * t * math.pi) / 4))
            else:
                self.walkPointStartRightstepRightLeg[1][i] = -self._swayBody * math.sin(t * math.pi)
                self.walkPointStartLeftstepRightLeg[1][i] = self._swayBody * math.sin(t * math.pi)

        # ending motion. 마무리 동작. 왼발이 뜸. 그러나 둘다 오른쪽다리 기준
        for i in range(self._bodyMovePoint - self._swayShift):
            self.walkPointEndLeftstepRightLeg[0][i] = -trajectoryLength * \
                ((i+1+self._swayShift)/(walkPoint-self._legMovePoint)-0.5)
            self.walkPointEndLeftstepRightLeg[2][i] = self._sit

            self.walkPointEndRightstepRightLeg[0][i] = -trajectoryLength * \
                ((i + 1 + self._swayShift + self._bodyMovePoint+self._legMovePoint)/(walkPoint-self._legMovePoint)-0.5)
            self.walkPointEndRightstepRightLeg[2][i] = self._sit
        for i in range(self._legMovePoint):
            t = (i + 1) / self._legMovePoint
            sin_tpi = math.sin(t * math.pi)

            self.walkPointEndLeftstepRightLeg[0][i + self._bodyMovePoint - self._swayShift] = (math.sin(t * math.pi / 2) - 1) * trajectoryLength * ((self._bodyMovePoint) / (self._bodyMovePoint * 2 + self._legMovePoint) - 0.5)
            self.walkPointEndLeftstepRightLeg[2][i + self._bodyMovePoint - self._swayShift] = self._sit

            self.walkPointEndRightstepRightLeg[0][i + self._bodyMovePoint - self._swayShift] = (2 * t - 2 + (1 - t) * self._liftPush * -sin_tpi + t * self._landPull * sin_tpi) * trajectoryLength / 4
            self.walkPointEndRightstepRightLeg[2][i + self._bodyMovePoint - self._swayShift] = math.sin(t * math.pi) * self._h + self._sit
        for i in range(self._swayShift):
            self.walkPointEndLeftstepRightLeg[0][i + self._bodyMovePoint + self._legMovePoint - self._swayShift] = 0
            self.walkPointEndLeftstepRightLeg[2][i + self._bodyMovePoint + self._legMovePoint - self._swayShift] = self._sit

            self.walkPointEndRightstepRightLeg[0][i + self._bodyMovePoint + self._legMovePoint - self._swayShift] = 0
            self.walkPointEndRightstepRightLeg[2][i + self._bodyMovePoint + self._legMovePoint - self._swayShift] = self._sit

        # turn

        self.turnListUnfold = np.zeros((self._bodyMovePoint + self._legMovePoint, 12))
        self.turnListFold = np.zeros((self._bodyMovePoint + self._legMovePoint, 12))
        turnAngle = np.zeros(self._bodyMovePoint + self._legMovePoint)
        for i in range(self._legMovePoint):
            t = (i + 1) / self._legMovePoint
            turnAngle[self._bodyMovePoint - self._swayShift + i] = (1 - math.cos(math.pi * t)) / 4
        for i in range(self._swayShift):
            turnAngle[self._bodyMovePoint + self._legMovePoint - self._swayShift + i] = 1 / 2

        for i in range(self._bodyMovePoint + self._legMovePoint):
            self.turnListUnfold[i] = [-turnAngle[i], 0, 0, 0, 0, 0, +turnAngle[i], 0, 0, 0, 0, 0]
            self.turnListFold[i] = [-0.5 + turnAngle[i], 0, 0, 0, 0, 0, +0.5 - turnAngle[i], 0, 0, 0, 0, 0]

        for i in range(self._bodyMovePoint + self._legMovePoint):
            t = 1 - (i + 1) / (self._bodyMovePoint + self._legMovePoint)

            if t < 1 / 4:
                self.walkPointEndLeftstepRightLeg[1][i] = self._swayBody * (math.sin(t * math.pi) - (1 - math.sin(math.pi * 2 * t)) * (math.sin(4 * t * math.pi) / 4))
                self.walkPointEndRightstepRightLeg[1][i] = -self._swayBody * (math.sin(t * math.pi) - (1 - math.sin(math.pi * 2 * t)) * (math.sin(4 * t * math.pi) / 4))
            else:
                self.walkPointEndLeftstepRightLeg[1][i] = self._swayBody * math.sin(t * math.pi)
                self.walkPointEndRightstepRightLeg[1][i] = -self._swayBody * math.sin(t * math.pi)

        # 추가 파라미터의 조정

        if self._incline != 0:  # 기울기. 계단 등에서 사용.
            walkPoint0[2] = walkPoint0[2] + walkPoint0[0] * self._incline
            walkPoint1[2] = walkPoint1[2] + walkPoint1[0] * self._incline
            walkPoint2[2] = walkPoint2[2] + walkPoint2[0] * self._incline
            walkPoint3[2] = walkPoint3[2] + walkPoint3[0] * self._incline
            self.walkPointStartRightstepRightLeg[2] = self.walkPointStartRightstepRightLeg[2] + self.walkPointStartRightstepRightLeg[0] * self._incline
            self.walkPointStartLeftstepRightLeg[2] = self.walkPointStartLeftstepRightLeg[2] + self.walkPointStartLeftstepRightLeg[0] * self._incline
            self.walkPointEndLeftstepRightLeg[2] = self.walkPointEndLeftstepRightLeg[2] + self.walkPointEndLeftstepRightLeg[0] * self._incline
            self.walkPointEndRightstepRightLeg[2] = self.walkPointEndRightstepRightLeg[2] + self.walkPointEndRightstepRightLeg[0] * self._incline

        if self._bodyPositionXPlus != 0:  # 허리 앞뒤 위치 조절
            walkPoint0[0] = walkPoint0[0] - self._bodyPositionXPlus
            walkPoint1[0] = walkPoint1[0] - self._bodyPositionXPlus
            walkPoint2[0] = walkPoint2[0] - self._bodyPositionXPlus
            walkPoint3[0] = walkPoint3[0] - self._bodyPositionXPlus
            self.walkPointStartRightstepRightLeg[0] = self.walkPointStartRightstepRightLeg[0] - self._bodyPositionXPlus
            self.walkPointStartLeftstepRightLeg[0] = self.walkPointStartLeftstepRightLeg[0] - self._bodyPositionXPlus
            self.walkPointEndLeftstepRightLeg[0] = self.walkPointEndLeftstepRightLeg[0] - self._bodyPositionXPlus
            self.walkPointEndRightstepRightLeg[0] = self.walkPointEndRightstepRightLeg[0] - self._bodyPositionXPlus

        if self._damping != 0:  # 댐핑 조절
            dampHeight = (walkPoint3[2][-1] - walkPoint0[2][0]) / 2
            walkPoint0[2][0] = walkPoint0[2][0] + dampHeight * self._damping
            walkPoint2[2][0] = walkPoint2[2][0] - dampHeight * self._damping

        self._walkPoint0 = walkPoint0
        self._walkPoint1 = walkPoint1
        self._walkPoint2 = walkPoint2
        self._walkPoint3 = walkPoint3

        self.walkPointLeftStepRightLeg = np.column_stack([walkPoint0[:, self._swayShift:], walkPoint1, walkPoint2[:, :self._swayShift]])
        self.walkPointRightStepRightLeg = np.column_stack([walkPoint2[:, self._swayShift:], walkPoint3, walkPoint0[:, :self._swayShift]])

        self.walkPointLeftStepLeftLeg = self.walkPointRightStepRightLeg * np.array([[1], [-1], [1]])
        self.walkPointRightStepLeftLeg = self.walkPointLeftStepRightLeg * np.array([[1], [-1], [1]])

        self.walkPointStartRightstepLeftLeg = self.walkPointStartLeftstepRightLeg * np.array([[1], [-1], [1]])
        self.walkPointStartLeftstepLeftLeg = self.walkPointStartRightstepRightLeg * np.array([[1], [-1], [1]])

        self.walkPointEndLeftstepLeftLeg = self.walkPointEndRightstepRightLeg * np.array([[1], [-1], [1]])
        self.walkPointEndRightstepLeftLeg = self.walkPointEndLeftstepRightLeg * np.array([[1], [-1], [1]])

    def inverseKinematicsPoint(self, pointRight, pointLeft):
        # point list to angle list.
        l3 = self._legUp_length
        l4 = self._legDown_length

        fx = pointRight[0]
        fy = pointRight[1]
        fz = self._legUp_length + self._legDown_length - pointRight[2]

        a = math.sqrt(fx * fx + fy * fy + fz * fz)

        d1 = math.asin(fx / a)
        d2 = math.acos((l3 * l3 + a * a - l4 * l4) / (2 * l3 * a))
        #d3 = math.acos(fz/a)
        d4 = math.acos((l4 * l4 + a * a - l3 * l3) / (2 * l4 * a))
        d5 = math.pi - d2 - d4

        t1 = (math.atan2(fy, fz))
        t2 = d1 + d2
        t3 = math.pi - d5
        t4 = -t2 + t3
        t5 = -t1

        rightInverse = np.array([0, t1, -t2, t3, -t4, t5]) * self._motorDirectionRight

        fx = pointLeft[0]
        fy = pointLeft[1]
        fz = self._legUp_length + self._legDown_length - pointLeft[2]

        a = math.sqrt(fx * fx + fy * fy + fz * fz)

        d1 = math.asin(fx / a)
        d2 = math.acos((l3 * l3 + a * a - l4 * l4) / (2 * l3 * a))
        #d3 = math.acos(fz/a)
        d4 = math.acos((l4 * l4 + a * a - l3 * l3) / (2 * l4 * a))
        d5 = math.pi - d2 - d4

        t1 = (math.atan2(fy, fz))
        t2 = d1 + d2
        t3 = math.pi - d5
        t4 = -t2 + t3
        t5 = -t1

        leftInverse = np.array([0, t1, -t2, t3, -t4, t5]) * self._motorDirectionLeft
        #print(np.hstack([rightInverse, leftInverse]))
        return np.hstack([rightInverse, leftInverse])

    def inverseKinematicsList(self, point, isRightLeg):
        inverseAngle = np.zeros((point[0].size, 6))
        for i in range(point[0].size):
            l3 = self._legUp_length
            l4 = self._legDown_length

            fx = point[0][i]
            fy = point[1][i]
            fz = self._legUp_length + self._legDown_length - point[2][i]

            a = math.sqrt(fx * fx + fy * fy + fz * fz)

            d1 = math.asin(fx / a)
            d2 = math.acos((l3 * l3 + a * a - l4 * l4) / (2 * l3 * a))
            #d3 = math.acos(fz/a)
            d4 = math.acos((l4 * l4 + a * a - l3 * l3) / (2 * l4 * a))
            d5 = math.pi - d2 - d4

            t1 = (math.atan2(fy, fz))
            t2 = d1 + d2
            t3 = math.pi - d5
            t4 = -t2 + t3
            t5 = -t1

            if isRightLeg:
                inverseAngle[i] = np.array([0, t1, -t2, t3, -t4, t5]) * self._motorDirectionRight
            else:
                inverseAngle[i] = np.array([0, t1, -t2, t3, -t4, t5]) * self._motorDirectionLeft

        return inverseAngle

    def showGaitPoint2D(self):
        plt.plot(self._walkPoint0[0], self._walkPoint0[2], 'o-', c='red',  ms=7, lw=5)
        plt.plot(self._walkPoint1[0], self._walkPoint1[2], 'o-', c='blue', ms=7, lw=5)
        plt.plot(self._walkPoint2[0], self._walkPoint2[2], 'o-', c='red',  ms=7, lw=5)
        plt.plot(self._walkPoint3[0], self._walkPoint3[2], 'o-', c='blue', ms=7, lw=5)

        plt.plot(self.walkPointStartRightstepRightLeg[0], self.walkPointStartRightstepRightLeg[2], '*-')
        plt.plot(self.walkPointStartLeftstepRightLeg[0], self.walkPointStartLeftstepRightLeg[2],   '*-')
        plt.plot(self.walkPointEndRightstepRightLeg[0], self.walkPointEndRightstepRightLeg[2],     '*-')
        plt.plot(self.walkPointEndLeftstepRightLeg[0], self.walkPointEndLeftstepRightLeg[2],       '*-')

        plt.show()

    def showGaitPoint2DTop(self):
        plt.plot(self._walkPoint0[0], self._walkPoint0[1], 'o-')
        plt.plot(self._walkPoint1[0], self._walkPoint1[1], 'o-')
        plt.plot(self._walkPoint2[0], self._walkPoint2[1], 'o-')
        plt.plot(self._walkPoint3[0], self._walkPoint3[1], 'o-')

        plt.plot(self.walkPointStartRightstepRightLeg[0], self.walkPointStartRightstepRightLeg[1], '.-')
        plt.plot(self.walkPointStartLeftstepRightLeg[0], self.walkPointStartLeftstepRightLeg[1], '.-')

        plt.plot(self.walkPointEndRightstepRightLeg[0], self.walkPointEndRightstepRightLeg[1], '+-')
        plt.plot(self.walkPointEndLeftstepRightLeg[0], self.walkPointEndLeftstepRightLeg[1], '+-')

        plt.show()

    def showGaitPoint3D(self):
        fig = plt.figure(1)
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(self.walkPointRightStepRightLeg[0], self.walkPointRightStepRightLeg[1],
                self.walkPointRightStepRightLeg[2], 'co-', lw=10, ms=6, label='RSRL')
        ax.plot(self.walkPointLeftStepRightLeg[0], self.walkPointLeftStepRightLeg[1],
                self.walkPointLeftStepRightLeg[2], 'mo-', lw=10, ms=6, label='LSRL')

        ax.plot(self._walkPoint0[0], self._walkPoint0[1], self._walkPoint0[2], 'o', label='WP0')
        ax.plot(self._walkPoint1[0], self._walkPoint1[1], self._walkPoint1[2], 'o', label='WP1')
        ax.plot(self._walkPoint2[0], self._walkPoint2[1], self._walkPoint2[2], 'o', label='WP2')
        ax.plot(self._walkPoint3[0], self._walkPoint3[1], self._walkPoint3[2], 'o', label='WP3')

        ax.plot(self.walkPointStartRightstepRightLeg[0], self.walkPointStartRightstepRightLeg[1],
                self.walkPointStartRightstepRightLeg[2], '*-', label='WPS_RSRL')
        ax.plot(self.walkPointStartLeftstepRightLeg[0], self.walkPointStartLeftstepRightLeg[1],
                self.walkPointStartLeftstepRightLeg[2], '*-', label='WPS_LSRL')

        ax.plot(self.walkPointEndRightstepRightLeg[0], self.walkPointEndRightstepRightLeg[1],
                self.walkPointEndRightstepRightLeg[2], 'c-', label='WPE_RSRL')
        ax.plot(self.walkPointEndLeftstepRightLeg[0], self.walkPointEndLeftstepRightLeg[1],
                self.walkPointEndLeftstepRightLeg[2], '+-', label='WPE_LSRL')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.legend()
        plt.show()
        

    def inverseKinematicsAll(self):
        self.walkAnglesStartRight = np.column_stack(
            [self.inverseKinematicsList(self.walkPointStartRightstepRightLeg, True),
             self.inverseKinematicsList(self.walkPointStartRightstepLeftLeg, False)])
        self.walkAnglesStartLeft = np.column_stack(
            [self.inverseKinematicsList(self.walkPointStartLeftstepRightLeg, True),
             self.inverseKinematicsList(self.walkPointStartLeftstepLeftLeg, False)])

        self.walkAnglesEndLeft = np.column_stack(
            [self.inverseKinematicsList(self.walkPointEndLeftstepRightLeg, True),
             self.inverseKinematicsList(self.walkPointEndLeftstepLeftLeg, False)])
        self.walkAnglesEndRight = np.column_stack(
            [self.inverseKinematicsList(self.walkPointEndRightstepRightLeg, True),
             self.inverseKinematicsList(self.walkPointEndRightstepLeftLeg, False)])
             
        self.walkAnglesWalkingRight = np.column_stack(
            [self.inverseKinematicsList(self.walkPointRightStepRightLeg, True),
             self.inverseKinematicsList(self.walkPointRightStepLeftLeg, False)])
        self.walkAnglesWalkingLeft = np.column_stack(
            [self.inverseKinematicsList(self.walkPointLeftStepRightLeg, True),
             self.inverseKinematicsList(self.walkPointLeftStepLeftLeg, False)])


def main():
    walk = WalkGenerator()
    walk.setWalkParameter(bodyMovePoint=8, legMovePoint=8, height=50, stride=80, sit=30, swayBody=60, swayFoot=0,
                          bodyPositionForwardPlus=0, swayShift=5, liftPush=0.4, landPull=0.7, timeStep=0.06, damping=0.0, incline=0.0)
    walk.generate()
    walk.showGaitPoint2D()
    walk.showGaitPoint2DTop()
    walk.showGaitPoint3D()


if __name__ == "__main__":
    main()
