import YEI_BL as YEI
import time
import numpy as np
import matplotlib.pyplot as plt

plt.close('all')
stream_dur=30; delay=1 #seconds
interval=100000 #microseconds
data=np.zeros((((10**6)/interval)*stream_dur,8)) #allocate space for data


#%% IMU Communication
#YEI.close_com(50)
com_handle=YEI.create_com() #args=COMPort #
print('COMPORT created')
time.sleep(2)
#%%
print('start stream...')
status=YEI.start_stream(com_handle,stream_dur,interval) #args=(COM_Port,IMU logic ID,stream duration)

i=0; start_t=time.clock(); current_t=time.clock()
while stream_dur>(current_t-start_t):#current time doesnt update
    data[i,:]=YEI.data_collect(com_handle) #args=(COM_Port,logic ID)
    current_t=time.clock()
    time.sleep(interval/10**6)
    if data[i,7]==1 or data[i,7]==2:
        YEI.stop_stream(com_handle)
        break
    
    i+=1

    
print('Done streaming')
#%%  
#time.sleep(2)
YEI.close_com(com_handle)
print('COMPORT closed')

#%%
data=data[data[:,0]>0,:] #truncate zeros 
t=[(x-data[0,0])*10**-6 for x in data[:,0]]

plt.figure(1)
plt.plot(t,data[:,1],t,data[:,2],t,data[:,3])
plt.grid()
plt.title('Gyroscope')
plt.xlabel('Time (s)')
plt.ylabel('Angular Velocity (rad/s)')

plt.figure(2)
plt.plot(t,data[:,4],t,data[:,5],t,data[:,6])
plt.grid()
plt.title('Accelerometer')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (G)')

plt.figure(3)
plt.plot(t,data[:,7])
plt.title('Button State')
plt.xlabel('Time (s)')
plt.ylabel('Button State')


