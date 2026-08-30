from DataReader import DataReader
import matplotlib.pyplot as plt
import numpy as np
import math
dr = DataReader(1)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize = (10, 4))
#Assume start at zero.
orientation = []
gamma = .2
for i in range(0, len(dr.imu_mat['ts'])):
    [ax, ay, az, wz, wy, wx] = dr.get_sample(i, True)
    
    roll = math.atan( (ay / math.sqrt(math.pow(ax, 2) + math.pow(az, 2)))) 
    pitch= math.atan( -(ax / math.sqrt(math.pow(ay, 2) + math.pow(az, 2)))) 
    yaw = math.atan( (math.sqrt(math.pow(ax, 2) + math.pow(ay, 2)))/az)

    
    #Perform low-pass filter. 
    if(i > 0):
        roll = (1-gamma)*orientation[i-1][0] + gamma*roll
        pitch = (1-gamma)*orientation[i-1][1] + gamma*pitch
        yaw = (1-gamma)*orientation[i-1][2] + gamma*yaw
    orientation.append([roll, pitch, yaw])

yaw_accel = [orient[0] for orient in orientation[0:]]
pitch_accel= [orient[1] for orient in orientation[0:]]
roll_accel = [orient[2] for orient in orientation[0:]]

print(roll_accel)

vicon = dr.vicon_mat['rots'].as_euler('ZYX')
yaw_vicon = [euler[0] for euler in vicon[0:]]
pitch_vicon = [euler[1] for euler in vicon[0:]]
roll_vicon = [euler[2] for euler in vicon[0:]]

ax1.plot(dr.imu_mat['ts'][0:], yaw_accel, label = 'ROLL_GYRO')
ax2.plot(dr.imu_mat['ts'][0:], pitch_accel, label = 'PITCH_GYRO')
ax3.plot(dr.imu_mat['ts'][0:], roll_accel, label = 'YAW_GYRO')
ax1.plot(dr.vicon_mat['ts'][0:], roll_vicon, label = 'ROLL_VICON')
ax2.plot(dr.vicon_mat['ts'][0:], pitch_vicon, label = 'PITCH_VICON')
ax3.plot(dr.vicon_mat['ts'][0:], yaw_vicon, label = 'YAW_VICON')
ax1.legend()
ax2.legend()
ax3.legend()
plt.show()