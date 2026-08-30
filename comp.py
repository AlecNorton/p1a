from DataReader import DataReader
import matplotlib.pyplot as plt
import numpy as np
import math
from math import cos, sin, tan

def Z(angle):
    return np.asarray([[1, 0, 0], [0, cos(angle), -sin(angle)], [0 ,sin(angle), cos(angle)]])
def Y(angle):
    return np.asarray([[cos(angle) ,0 ,sin(angle)], [0, 1, 0], [-sin(angle), 0, cos(angle)]])
def X(angle):
    return np.asarray([[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]])


def convert_to_euler(roll, pitch, yaw):
    return np.asarray([[1 ,sin(roll)*tan(pitch), cos(roll)*tan(pitch)], [0, cos(roll), -sin(roll)], [0, sin(roll)/cos(pitch), cos(roll)/cos(pitch)]])
def ZYX(yaw, pitch, roll):
    return np.matmul(Z(yaw), Y(pitch), X(roll))
def XYZ(yaw, pitch, roll):
    return np.matmul(X(yaw), Y(pitch), Z(roll))
def YXZ(yaw, pitch, roll):
    return np.matmul(Y(yaw), X(pitch), Z(roll))
def YZX(yaw, pitch, roll):
    return  np.matmul(Y(yaw), Z(pitch), X(roll))
def XZY(yaw, pitch, roll):
    return np.matmul(X(yaw), Z(pitch), Y(roll))
def ZXY(yaw, pitch, roll):
    return np.matmul(Z(yaw), Y(pitch), X(roll))
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (10, 4))
#Assume start at zero.

dr = DataReader(3)

[ax, ay, az, wz, wy, wz] = dr.get_sample(0, True)
roll = math.atan( (ay / math.sqrt(math.pow(ax, 2) + math.pow(az, 2)))) 
pitch= math.atan( -(ax / math.sqrt(math.pow(ay, 2) + math.pow(az, 2)))) 
yaw = math.atan( (math.sqrt(math.pow(ax, 2) + math.pow(ay, 2)))/az)
orientation = [[roll, pitch, yaw]]

gamma = .9
#Get standard deviation
for i in range(1, len(dr.imu_mat['ts'])):
    #bias_dot_x = np.random.normal(0, dr.gyro_noise[2])
    #bias_dot_y = np.random.normal(0, dr.gyro_noise[1])
    #bias_dot_z = np.random.normal(0, dr.gyro_noise[0])
    #Calculating b_dot. 

    deltaTime = dr.imu_mat['ts'][i] - dr.imu_mat['ts'][i-1]


    #time_bias = np.add(time_bias, np.multiply([bias_dot_z, bias_dot_y, bias_dot_x], deltaTime))

    [ax, ay, az, wz, wy, wx] = dr.get_sample(i, True)

    roll = math.atan( (ay / math.sqrt(math.pow(ax, 2) + math.pow(az, 2)))) 
    pitch= math.atan( -(ax / math.sqrt(math.pow(ay, 2) + math.pow(az, 2)))) 
    yaw = math.atan( (math.sqrt(math.pow(ax, 2) + math.pow(ay, 2)))/az)

    #Perform low-pass 
    accel = np.multiply([roll, pitch, yaw], gamma)
    #Convert to roll, pitch, yaw.
    mat = convert_to_euler(orientation[i-1][0], orientation[i-1][1], orientation[i-1][2])
    gyro = np.matmul(mat, np.transpose([wx, wy, wz]))
    #Perform high-pass
    gyro = np.multiply(gyro, (1-gamma))
    orientation.append(np.add(gyro, accel))

roll_gyro = [orient[0] for orient in orientation[0:]]
pitch_gyro= [orient[1] for orient in orientation[0:]]
yaw_gyro = [orient[2] for orient in orientation[0:]]

#Roll and pitch seem to be swatched
vicon = dr.vicon_mat['rots'].as_euler('ZYX')
yaw_vicon = [euler[0] for euler in vicon[1:]]
pitch_vicon = [euler[1] for euler in vicon[1:]]
roll_vicon = [euler[2] for euler in vicon[1:]]

ax1.plot(dr.imu_mat['ts'][0:], roll_gyro, label = 'ROLL_GYRO')
ax2.plot(dr.imu_mat['ts'][0:], pitch_gyro, label = 'PITCH_GYRO')
ax3.plot(dr.imu_mat['ts'][0:], yaw_gyro, label = 'YAW_GYRO')
ax1.plot(dr.vicon_mat['ts'][1:], roll_vicon, label = 'ROLL_VICON')
ax2.plot(dr.vicon_mat['ts'][1:], pitch_vicon, label = 'PITCH_VICON')
ax3.plot(dr.vicon_mat['ts'][1:], yaw_vicon, label = 'YAW_VICON')
ax1.legend()
ax2.legend()
ax3.legend()
plt.show()