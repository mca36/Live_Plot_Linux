from multiprocessing import Process, Queue
import YEI_BL as YEI
import time
<<<<<<< HEAD
#import numpy as np
#import matplotlib.pyplot as plt
from collections import deque
=======
import numpy as np
import matplotlib.pyplot as plt
>>>>>>> live_plot/beta

#%% Initialize settings
#plt.close('all')
stream_dur=60; delay=1 #seconds
interval=100000 #microseconds


#%% Initialize communication
com_handle=YEI.create_com() #args=COMPort #
print('COMPORT created')
time.sleep(2)
print('start stream...')
status=YEI.start_stream(com_handle,stream_dur,interval) #args=(COM_Port,IMU logic ID,stream duration)
<<<<<<< HEAD
#data=np.zeros((((10**6)/interval)*stream_dur,8)) #allocate space for data
data_len=((10**6)/interval)*stream_dur
i=0

#%% deque shuffling 
gx=deque([0.0]*data_len)
gy=deque([0.0]*data_len)
gz=deque([0.0]*data_len)

def add_buff(buff,val):
    global data_len
    
    if len(buff)<data_len:
        buff.append(val)
        return buff
    else:
        buff.pop()
        buff.appendleft(val)
        return buff

#%% Process 1


=======
data=np.zeros((((10**6)/interval)*stream_dur,8)) #allocate space for data
i=0
#%% Process 1

import time
>>>>>>> live_plot/beta
def process1(q):
    global com_handle,stop
    
    while True:
        y=[]
        y=YEI.data_collect(com_handle)
        q.put(y)
        time.sleep(interval/10**6)
        if y[7]==1 or y[7]==2:
            YEI.stop_stream(com_handle)
            break
            
            
    YEI.close_com(com_handle)
    print('COMPORT closed')
    
    
 #%%Process 2       
def process2(q):
    global i,data
    print ('Collection started')
    while True:
        data[i,:]=q.get()
        if data[i,7]==1 or data[i,7]==2:
            print('Stop is equal to 2')
            break
        i+=1
    
    print('Plot data')
<<<<<<< HEAD
#    data=data[data[:,0]>0,:] #truncate zeros 
#    t=[(x-data[0,0])*10**-6 for x in data[:,0]]

=======
    data=data[data[:,0]>0,:] #truncate zeros 
    t=[(x-data[0,0])*10**-6 for x in data[:,0]]
    print('almost there')
    
    plt.figure(1)
    plt.plot(t,data[:,1],label='X-Axis')
    plt.plot(t,data[:,2],label='Y-Axis')
    plt.plot(t,data[:,3],label='Z-Axis')
    plt.legend()
    plt.grid()
    plt.title('Gyroscope')
    plt.xlabel('Time (s)')
    plt.ylabel('Angular Velocity (rad/s)')
    
    plt.figure(2)
    plt.plot(t,data[:,4],label='X-Axis')
    plt.plot(t,data[:,5],label='Y-Axis')
    plt.plot(t,data[:,6],label='Z-Axis')
    plt.grid()
    plt.legend()
    plt.title('Accelerometer')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (G)')
    plt.show()
>>>>>>> live_plot/beta
    

 #%%Start both processes   
if __name__=='__main__':

    q=Queue()
    process_one=Process(target=process1,args=(q,))
    process_two=Process(target=process2,args=(q,))

    process_one.start()
    process_two.start()
    q.close()
    q.join_thread()
    
    process_one.join()
    process_two.join()

   
