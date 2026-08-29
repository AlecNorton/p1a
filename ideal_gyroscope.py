from DataReader import DataReader
import matplotlib.pyplot as plt
import numpy as np
dr = DataReader(2)

fig = plt.figure()
ax = fig.add_subplot()
#Assume start at zero.
orientation = [[0.0, 0.0, 0.0]]
for i in range(0, len(dr.imu_mat['ts'])-1):
    wz = dr.imu_mat['vals'][3][i] - dr.gyro_model[0][0] -dr.gyro_model[1][0]
    wy = dr.imu_mat['vals'][4][i] - dr.gyro_model[0][1] -dr.gyro_model[1][1]
    wx = dr.imu_mat['vals'][5][i] - dr.gyro_model[0][2] - dr.gyro_model[1][2]

    #wz = dr.imu_mat['vals'][3][i]
    #wy = dr.imu_mat['vals'][4][i]
    #wx = dr.imu_mat['vals'][5][i]
    deltaTime = dr.imu_mat['ts'][i+1] - dr.imu_mat['ts'][i]
    print(deltaTime)
    print([wx, wy, wz])
    print(np.multiply([wx, wy, wz], deltaTime))
    orientation.append(np.add(orientation[i], np.multiply(deltaTime, [wx, wy, wz])))

roll_gyro = [orient[0] for orient in orientation[1:]]
pitch_gyro= [orient[1] for orient in orientation[1:]]
yaw_gyro = [orient[2] for orient in orientation[1:]]

#Roll and pitch seem to be swatched
vicon = dr.vicon_mat['rots'].as_euler('ZYX')
yaw_vicon = [euler[0] for euler in vicon[1:]]
roll_vicon = [euler[1] for euler in vicon[1:]]
pitch_vicon = [euler[2] for euler in vicon[1:]]
ax.plot(dr.imu_mat['ts'][1:], roll_gyro, label = 'ROLL_GYRO')
ax.plot(dr.imu_mat['ts'][1:], pitch_gyro, label = 'PITCH_GYRO')
ax.plot(dr.imu_mat['ts'][1:], yaw_gyro, label = 'YAW_GYRO')
fig2 = plt.figure()
ax2 = fig2.add_subplot()
ax2.plot(dr.vicon_mat['ts'][1:], roll_vicon, label = 'ROLL_GYRO')
ax2.plot(dr.vicon_mat['ts'][1:], pitch_vicon, label = 'PITCH_GYRO')
ax2.plot(dr.vicon_mat['ts'][1:], yaw_vicon, label = 'YAW_GYRO')
ax.legend()
ax2.legend()
plt.show()


