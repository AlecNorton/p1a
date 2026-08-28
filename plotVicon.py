import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from DataReader import DataReader
from p1a.rotplot import rotplot
# Initialize figure and axis
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
dr = DataReader(6)

def update(frame):
    """Callback function that clears and replots each frame."""
    ax.clear()
    rot = dr.get_sample(frame, False)
    rotplot(rot.as_matrix(), ax)
    ax.set_title(f"Replotting Method - Frame {frame}")
    ax.grid(True)


# Create the animation
# frames: total number of frames
# interval: delay between frames in milliseconds
ani = FuncAnimation(fig, update, frames=len(dr.vicon_mat['ts']), interval=.001)

plt.show()