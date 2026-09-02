
# Setup and Usage

## 1. Folder Structure
Place the Data folder inside p1a so that the directory structure looks like this:
```
p1a/Data/Train/IMU/imuRaw1.mat
```
Make sure all .mat IMU files are placed inside:
```
p1a/Data/Train/IMU/
```
## 2. Running the Script
Run the following command from outside p1a folder:  
```
python p1a/Code/wrapper.py --mat_number {NUMBER OF THE IMU DATASET}
```
Replace {NUMBER OF THE IMU DATASET} with the dataset number you want to process (e.g.1,2,..).
