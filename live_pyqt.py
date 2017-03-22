from multiprocessing import Process, Queue
import time
#import numpy as np
import pyqtgraph as pg
import YEI_BL as YEI
from collections import deque

<<<<<<< HEAD
#pg.setConfigOption('background','w')
#%% Initialize settings
stream_dur=600; delay=1 #seconds
=======
pg.setConfigOption('background','w')
#%% Initialize settings
stream_dur=60; delay=1 #seconds
>>>>>>> live_plot/beta
interval=100000 #microseconds
maxlen=int(60/(interval*10**-6))

t=deque([0.0]*maxlen);
acc_x=deque([0.0]*maxlen); acc_y=deque([0.0]*maxlen); acc_z=deque([0.0]*maxlen);
gyro_x=deque([0.0]*maxlen); gyro_y=deque([0.0]*maxlen); gyro_z=deque([0.0]*maxlen);
             
def deq_flop(deq,val):
    deq.append(val); deq.popleft()
    return deq


#%% Initialize communication
com_handle=YEI.create_com() #args=COMPort #
print('COMPORT created')
time.sleep(2)
print('start stream...')
status=YEI.start_stream(com_handle,stream_dur,interval) #args=(COM_Port,IMU logic ID,stream duration)
    
#%% Process 1
def process1(q):
    global com_handle
    
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
<<<<<<< HEAD
    #q.get()
=======
>>>>>>> live_plot/beta
    j=0; 
    global gyro_x,gyro_y,gyro_z,t
    global acc_x,acc_y, acc_z, maxlen
    end=maxlen-1
<<<<<<< HEAD
    
=======

>>>>>>> live_plot/beta
    win=pg.GraphicsWindow(title="Basic Plotting")
    win.resize(1000,600)
    
    p1=win.addPlot(title="Gyroscope",labels={"left":("rad/s",),"bottom":("time (s)",)})
    p1.showGrid(x=True,y=True)
    p1.addLegend()
    win.nextRow()
    p2=win.addPlot(title="Accelerometer",labels={"left":("G",),"bottom":("time (s)",)})
    p2.showGrid(x=True,y=True)
    p2.addLegend()
    
   # x=[];
<<<<<<< HEAD
    
    while True:
        y=q.get()
        t=deq_flop(t,y[0]*10**-6); 
=======
    while True:
        y=q.get()
        t=deq_flop(t,y[0]*10**-6); 
        #t[end-j]=t[end-j]-t[end]
>>>>>>> live_plot/beta
        gyro_x=deq_flop(gyro_x,y[1]); gyro_y=deq_flop(gyro_y,y[2]);
        gyro_z=deq_flop(gyro_z,y[3]); acc_x=deq_flop(acc_x,y[4]);  
        acc_y=deq_flop(acc_y,y[5]);  acc_z=deq_flop(acc_z,y[6]);    

        if j==0:
<<<<<<< HEAD
            t_start=t[end]
            t[end]-=t_start

=======
>>>>>>> live_plot/beta
            p1.setRange(xRange=[0,t[end]])
            p1.plot(t,gyro_x,clear=True,pen='r',name='X-Axis')
            p1.plot(t,gyro_y,pen='b',name='Y-Axis')
            p1.plot(t,gyro_z,pen='g',name='Z-Axis')
            
            p2.setRange(xRange=[0,t[end]])
            p2.plot(t,acc_x,clear=True,pen='r',name='X-Axis')
            p2.plot(t,acc_y,pen='b',name='Y-Axis')
            p2.plot(t,acc_z,pen='g',name='Z-Axis')
        else:
<<<<<<< HEAD
            t[end]-=t_start
=======
>>>>>>> live_plot/beta
            p1.setRange(xRange=[t[end-j],t[end]])
            p1.plot(t,gyro_x,clear=True,pen='r')
            p1.plot(t,gyro_y,pen='b')
            p1.plot(t,gyro_z,pen='g')
            
            p2.setRange(xRange=[t[end-j],t[end]])
            p2.plot(t,acc_x,clear=True,pen='r')
            p2.plot(t,acc_y,pen='b')
            p2.plot(t,acc_z,pen='g')
            
        pg.QtGui.QApplication.processEvents()
        
<<<<<<< HEAD
        j+=1
        
=======
>>>>>>> live_plot/beta
        if y[7]==1 or y[7]==2:
            print('Stop is equal to 2')
            break
        
<<<<<<< HEAD
        
=======
        j+=1
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

   
