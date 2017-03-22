from multiprocessing import Process, Queue
import time
import numpy as np
import pyqtgraph as pg
import YEI_BL as YEI
from collections import deque
import RMX
import scipy.integrate as sci_int

#pg.setConfigOption('background','w')
#%% Initialize settings
stream_dur=60; delay=1 #seconds
interval=100000 #microseconds
maxlen=int(60/(interval*10**-6))


#%% Initialize Deques
t=deque([0.0]*maxlen);
acc_x=deque([0.0]*maxlen); acc_y=deque([0.0]*maxlen); acc_z=deque([0.0]*maxlen);
gyro_x=deque([0.0]*maxlen); gyro_y=deque([0.0]*maxlen); gyro_z=deque([0.0]*maxlen);
posx=deque([0.0]*maxlen); posy=deque([0.0]*maxlen);
             
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
    j=0; 
    global gyro_x,gyro_y,gyro_z,t
    global acc_x,acc_y, acc_z, maxlen
    global posx,posy
    end=maxlen-1

    win=pg.GraphicsWindow(title="LIVE PLOT")
    win.resize(1000,600)
    
    p1=win.addPlot(title="IMU Trajectory",labels={"left":("Y (m)",),"bottom":("X (m)",)})
    p1.showGrid(x=True,y=True)
    p1.addLegend()
    
    accx_sum=0; accy_sum=0; accz_sum=0;
    gyrox_sum=0; gyroy_sum=0; gyroz_sum=0;
    B=[0,0,0] #Gyro bias
    loc_vel=[0,0,0]; loc_pos=[0,0,0]
    while True:
        y=q.get()
        t=deq_flop(t,y[0]*10**-6); 
        gyro_x=deq_flop(gyro_x,y[1]); gyro_y=deq_flop(gyro_y,y[2]);
        gyro_z=deq_flop(gyro_z,y[3]); acc_x=deq_flop(acc_x,y[4]);  
        acc_y=deq_flop(acc_y,y[5]);  acc_z=deq_flop(acc_z,y[6]);    
        if j==0:
            t_start=t[end]
            t[end]-=t_start
            print('Initializing orientation. Stand Still')

        elif j<20:
            t[end]-=t_start
            accx_sum+=acc_x[end]; accy_sum+=acc_y[end]; accz_sum+=acc_z[end]
            gyrox_sum+=gyro_x[end]; gyroy_sum+=gyro_y[end]; gyroz_sum+=gyro_z[end]
            
        elif j==20: #Initial orientation
            t[end]-=t_start
            Acc_avg=[accx_sum/(j+1),accy_sum/(j+1),accz_sum/(j+1)]
            B=[gyrox_sum/(j+1),gyroy_sum/(j+1),gyroz_sum/(j+1)]
            print(Acc_avg)
            print(B)

            quat=RMX.initial_quaternion(Acc_avg,0)
            quat_p=quat

        else:
            t[end]-=t_start
            dt=t[end]-t[end-1]
            quat=RMX.instant_quaternion(gyro_x[end]-B[0],gyro_y[end]-B[1],gyro_z[end]-B[2],quat_p,dt)
            RotMX=RMX.quat2rmx(quat)
            loc_acc=RMX.local_acc(RotMX,acc_x[end],acc_y[end],acc_z[end])
            #print([gyro_x[end],gyro_y[end],gyro_z[end]])
            quat_p=quat
            #print(loc_acc)
            
            for i in range(3):
                loc_vel[i]+=RMX.trapz(loc_acc[i],dt)
                loc_pos[i]+=RMX.trapz(loc_vel[i],dt)
                #loc_vel[i]+=sci_int.quad(RMX.quat2loc_acc(acc))
                #USE DBLQUAD INSTEAD (FASTER AND MORE ACCURATE)
            posx=deq_flop(posx,loc_pos[0]); posy=deq_flop(posy,loc_pos[1])
            
            p1.plot(posx,posy,clear=True,pen='r')
            
        pg.QtGui.QApplication.processEvents()
        
        
        if y[7]==1 or y[7]==2:
            print('Communication terminated')
            break
        
        j+=1
       
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

   

