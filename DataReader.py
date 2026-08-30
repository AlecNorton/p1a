import scipy
from scipy import io
import math
import numpy as np
class DataReader:
    def __init__(self, mat_number):
        self.imu_mat_path = "p1a/Data/Train/IMU/imuRaw" + str(mat_number) + ".mat"
        self.vicon_mat_path = "p1a/Data/Train/Vicon/viconRot" + str(mat_number) + ".mat"
        self.imu_mat = io.loadmat(self.imu_mat_path)
        self.vicon_mat = io.loadmat(self.vicon_mat_path)
        self.params_mat = io.loadmat('p1a/IMUParams.mat')['IMUParams']
        self.gyro_bias = self.gyro_bias_calibrate(200)
        self.gyro_noise = self.gyro_noise_calibrate(200)
        self.clean()
        self.align()
        #Perform again to get updated values for current units
        #self.gyro_model = self.gyro_model_calibrate(200)
        #self.accel_model = self.accel_model_calibrate(200)

    
    #Convert IMU linear and rotational velocities based on described equations. 
    
    def clean(self):
        #Cleaning IMU
        '''
        val_type_index = 0
        new_list = []
        for val_type in self.imu_mat['vals']:
            new_list.append([])
            for val_instance in val_type:
                #Converting linear accelerations
                if(val_type_index < 3):
                    new_val = (float(val_instance)+float(self.params_mat['IMUParams'][1][val_type_index]))/float(self.params_mat['IMUParams'][0][val_type_index])
                else:
                    new_val = (3300/1023) * (math.pi/180) *.3 * (float(val_instance) - self.gyro_model[0][val_type_index-3])
                #Converting rotational accelerations.
                new_list[val_type_index].append(new_val)
            val_type_index = val_type_index + 1
        self.imu_mat['vals'] = new_list
        '''
        self.imu_mat['ts'] = self.imu_mat['ts'][0]

        #Several parts of VICON data has NANS! Resolve by simply excluding them from dataset. 
        vicon_ts = self.vicon_mat['ts'][0]
        vicon_data = []
        rotMats = []
        for i in range(0, len(vicon_ts)):
            rotMat = self.vicon_mat['rots'][0:, 0:, i]
            if(np.isnan(rotMat[0][0])):
                #Invalid. 
                vicon_ts = np.delete(vicon_ts, i)
                print(f"Matrix {i} included NaNs, do not include...")
                continue
            try:
                scipy.spatial.transform.Rotation.from_matrix(rotMat)
                rotMats.append(rotMat)
            except ValueError:
                print(f"Matrix {i} is not a valid rotational matrix...{rotMat}")
                #print(f"Determinant is {scipy.linalg.det(rotMat)}")
                vicon_ts = np.delete(vicon_ts, i)
        self.vicon_mat['rots'] = scipy.spatial.transform.Rotation.from_matrix(rotMats)
        self.vicon_mat['ts'] = vicon_ts     
      

    #Determine gyro bias by averaging 
    def gyro_bias_calibrate(self, num_entries):
        gyro_bias_z = np.mean(self.imu_mat['vals'][3][0:num_entries])
        gyro_bias_y = np.mean(self.imu_mat['vals'][4][0:num_entries])
        gyro_bias_x = np.mean(self.imu_mat['vals'][5][0:num_entries])

        return [gyro_bias_z, gyro_bias_y, gyro_bias_x]

    def gyro_noise_calibrate(self, num_entries):
        gyro_noise = []
        for gyro in range(3, 6):
            new_list = []
            for i in range(0, len(self.imu_mat['vals'][gyro])):
                vals = self.get_sample(i, True)
                new_list.append(vals[gyro])
            gyro_noise.append(np.std(new_list))
        return gyro_noise

    def accel_model_calibrate(self, num_entries):
        accel_bias_x = np.mean(self.imu_mat['vals'][0][0:num_entries])
        accel_bias_y = np.mean(self.imu_mat['vals'][1][0:num_entries])
        accel_bias_z = np.mean(self.imu_mat['vals'][2][0:num_entries])

        return [[accel_bias_x, accel_bias_y, accel_bias_z]]

    def align(self):
        vicon_ts = self.vicon_mat['ts']
        imu_ts = self.imu_mat['ts']
        #If vicon is longer, interpolate imu so that it matches in length.
        begin_search_val = 0
        new_imu_data = [[], [], [], [], [], []]
        new_imu_ts = []
        #Likely not this one...?
        print("Interpolating imu...")
        '''
        for ts in vicon_ts:
            #print(f"Target ts: {ts}")
            index, imu_ts = self.search(imu_ts, ts)
            if(index == -1):
                #Nothing was found. Do not add
                break
            #print(f"Index: {index}")
            start_ts = imu_ts[0]
            step_ts = imu_ts[1]
            #print(f"Start TS: {start_ts}")
            #print(f"End_ts: {step_ts}")
            start_accel = self.get_sample(index+begin_search_val, True)
            end_accel = self.get_sample(index+begin_search_val + 1, True)
            #print(f"Start acceleration: {start_accel}")
            #print(f"end_accel: {end_accel}")
            unit_start_accel = start_accel/np.linalg.norm(start_accel)
            unit_end_accel = end_accel/np.linalg.norm(end_accel)
            cosOmega = np.clip(np.dot(unit_start_accel, unit_end_accel), -1.0, 1.0)
            #print(cosOmega)
            #wprint(f"Omega: {math.acos(cosOmega)}")
            
            ratio = 1 - (step_ts - ts)/(step_ts - start_ts)
            #print(f"Ratio: {ratio}")
            begin_search_val = index
            if(math.acos(cosOmega) != 0):
                new_accel = (math.sin((1-ratio)*math.acos(cosOmega))/math.sin(math.acos(cosOmega)))*unit_start_accel 
                new_accel = new_accel + (math.sin(ratio*math.acos(cosOmega))/math.sin(math.acos(cosOmega)))*unit_end_accel
                new_accel = new_accel * ((1-ratio)*np.linalg.norm(start_accel) + ratio*np.linalg.norm(end_accel))
            else:
                new_accel = (1-ratio)*unit_start_accel + ratio*unit_end_accel
                new_accel = new_accel * ((1-ratio)*np.linalg.norm(start_accel) + ratio*np.linalg.norm(end_accel))

            #print(f"New accel: {new_accel}")
            for i in range(0, 6):
                new_imu_data[i].append(new_accel[i])
            new_imu_ts.append(ts)

        self.imu_mat['vals'] = new_imu_data
        self.imu_mat['ts'] = new_imu_ts
        new_vicon_ts = list(filter(lambda x: x >=new_imu_ts[0] and x <= new_imu_ts[-1], self.vicon_mat['ts']))
        startIndex = np.where(self.vicon_mat['ts'] == new_vicon_ts[0])[0][0]

        endIndex = np.where(self.vicon_mat['ts'] == new_vicon_ts[-1])[0][0] +1
        new_vicon_mat = self.vicon_mat['rots'][startIndex:endIndex]
        self.vicon_mat['rots'] = new_vicon_mat
        self.vicon_mat['ts'] = new_vicon_ts
        '''
            

        print("Interpolating vicon.")
        slerp = scipy.spatial.transform.Slerp(vicon_ts, self.vicon_mat['rots'])
        #Ensure all imu_ts are within slerp ability to inteprolate. 
        new_imu_ts = list(filter(lambda x: x >= vicon_ts[0] and x<= vicon_ts[-1], imu_ts))
        #Get start and end index of new range of new_imu_ts
        startIndex = np.where(self.imu_mat['ts'] == new_imu_ts[0])[0][0]
        endIndex = np.where(self.imu_mat['ts'] == new_imu_ts[-1])[0][0]+1
        self.imu_mat['ts'] = new_imu_ts
        self.vicon_mat['ts'] = new_imu_ts
        vals = self.imu_mat['vals']
        new_list = []
        for i in range(0, 6):
            new_list.append(vals[i][startIndex:endIndex])
        self.imu_mat['vals'] = new_list
        self.vicon_mat['rots'] = slerp(new_imu_ts)

    def search(self, list, val):
        correctIndex = -1
        for i in range(0, len(list)-1):
            if(val > list[i] and val < list[i+1]):
                correctIndex = i
                break
            elif(val == list[i]):
                correctIndex = i
                break
        return correctIndex, list[correctIndex:]

    def get_sample(self, i, data_flag):
        if(data_flag):
            #Collect imu_mat data
            vals = self.imu_mat['vals']
            return np.array(self.convert_linear_accel([vals[0][i], vals[1][i], vals[2][i]])+self.convert_rotational_accel([vals[3][i], vals[4][i], vals[5][i]]))
        else:
            rot = self.vicon_mat['rots'][i]
            return rot
    
    def convert_linear_accel(self, accel):
        
        [ax, ay, az] = [accel[0], accel[1], accel[2]]
        '''
        conv_ax = ((ax + self.params_mat[1][0]) / self.params_mat[0][0])
        conv_ay = ((ay + self.params_mat[1][1]) / self.params_mat[0][1])
        conv_az = ((az + self.params_mat[1][2]) / self.params_mat[0][2])
        '''
        
        conv_ax = (ax*self.params_mat[0][0] + self.params_mat[1][0])*9.81
        conv_ay = (ay*self.params_mat[0][1] + self.params_mat[1][1])*9.81
        conv_az = (az*self.params_mat[0][2] + self.params_mat[1][2])*9.81
        
        return [conv_ax, conv_ay, conv_az]
    
    def convert_rotational_accel(self, acc):
        [wz, wy, wx] = [acc[0], acc[1], acc[2]]
        conv_wx = (3300/1023)* (math.pi/180) * .3 * (wx - self.gyro_bias[2])
        conv_wy = (3300/1023)* (math.pi/180) * .3 * (wy - self.gyro_bias[1])
        conv_wz = (3300/1023)* (math.pi/180) * .3 * (wz - self.gyro_bias[0])
        return [conv_wz, conv_wy, conv_wx]
            
        

