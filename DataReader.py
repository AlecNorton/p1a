from scipy import io
class DataReader:
    def __init__(self, mat_number):
        self.imu_mat_path = "ARN_p1a/Data/Train/IMU/imuRaw" + str(mat_number) + ".mat"
        self.vicon_mat_path = "ARN_p1a/Data/Train/Vicon/viconRot" + str(mat_number) + ".mat"
        self.imu_mat = io.loadmat(self.imu_mat_path)
        self.vicon_mat = io.loadmat(self.vicon_mat_path)
        self.lin = [[]] #Linear acceleration values
        self.rot = [] #Rotation acceleration values
        self.params_mat = io.loadmat('ARN_p1a/IMUParams.mat')
    def clean(self):
        val_type_index = 0
        for val_type in imu_mat['vals']:
            for val_instance in val_type:
                #Converting linear accelerations
                if(val_type_index < 3):
                    new_val = (val_instance+self.params_mat['IMUParams'][1][val_type_index])/self.params_mat['IMUParams'][]
                #Converting rotational accelerations.
                self.lin[val_type_index].append
            val_type_index = val_type_index + 1

