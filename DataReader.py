from scipy import io
import math
class DataReader:
    def __init__(self, mat_number):
        self.imu_mat_path = "p1a/Data/Train/IMU/imuRaw" + str(mat_number) + ".mat"
        self.vicon_mat_path = "p1a/Data/Train/Vicon/viconRot" + str(mat_number) + ".mat"
        self.imu_mat = io.loadmat(self.imu_mat_path)
        self.vicon_mat = io.loadmat(self.vicon_mat_path)
        self.accel = [] #Linear acceleration values
        self.params_mat = io.loadmat('p1a/IMUParams.mat')
        self.gyro_bias = self.gyro_bias_avg(100)
        self.clean_imu()
    
    #Convert IMU linear and rotational velocities based on described equations. 
    def clean_imu(self):
        val_type_index = 0
        for val_type in self.imu_mat['vals']:
            self.accel.append([])
            for val_instance in val_type:
                #Converting linear accelerations
                if(val_type_index < 3):
                    new_val = (float(val_instance)+float(self.params_mat['IMUParams'][1][val_type_index]))/float(self.params_mat['IMUParams'][0][val_type_index])
                else:
                    new_val = (3300/1023) * (math.pi/180) *.3 * (float(val_instance) - self.gyro_bias[val_type_index-3])
                #Converting rotational accelerations.
                self.accel[val_type_index].append(new_val)
            val_type_index = val_type_index + 1

    #Determine gyro bias by averaging 
    def gyro_bias_avg(self, num_entries):
        gyro_bias_x = 0
        gyro_bias_y = 0
        gyro_bias_z = 0
        for i in range(0, num_entries):
            gyro_bias_x = gyro_bias_x + int(self.imu_mat['vals'][3][i])
            gyro_bias_y = gyro_bias_y + int(self.imu_mat['vals'][4][i])
            gyro_bias_z = gyro_bias_z + int(self.imu_mat['vals'][5][i])
        gyro_bias = [gyro_bias_x, gyro_bias_y, gyro_bias_z]
        return [bias/num_entries for bias in gyro_bias]

    def align(self):
        vicon_ts = self.vicon_mat['ts']
        imu_ts = self.imu_mat['ts']
        #If vicon is longer, interpolate imu so that it matches in length.
        begin_search_val = 0
        if(len(vicon_ts) > len(imu_ts)):
            for ts in vicon_ts:

        else:
            for ts in imu_ts:
                pass #TODO

    def search(self, begin_search, list, val):
        for i in range(begin_search, len(list)-2):
            if(val > list[i] and val < list[i+1]){
                return i, list[i], list[i+1]
            }
            elif(val == list[i]){
                return i, -1, -1
            }

