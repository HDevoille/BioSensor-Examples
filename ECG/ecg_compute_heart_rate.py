from pylsl import StreamInlet,resolve_stream
import numpy as np
import matplotlib.pyplot as plt


streams = resolve_stream('name','OpenSignals')

inlet = StreamInlet(streams[0])

# linear spaced vector between 0.5 pi and 1.5 pi 
v = np.linspace(0.5 * np.pi, 1.5 * np.pi, 15)

# create sine filter for approximating QRS feature
peak_filter = np.sin(v)

n=0
calibration_data = []
calibration_time = []

print("start")
while n < 1000:
    sample, timestamp = inlet.pull_sample()
    calibration_data.append(sample[1])
    calibration_time.append(timestamp)
    n+=1
print("end")

ecg_transform = np.correlate(calibration_data,peak_filter,mode='same')
print("length: ",len(ecg_transform))

peak = float(abs(max(ecg_transform))) * 0.95
print("max: ",peak)
time = calibration_time[-1] - calibration_time[0]
peak_count = 0

for i in ecg_transform:
    if i > peak:
        print(i)
        peak_count+=1

heart_rate = (peak_count/time)*60

print("number of peak: ",peak_count)
print("time: ",time)
print("heart rate: ",heart_rate)

plt.plot(ecg_transform)
plt.show()
