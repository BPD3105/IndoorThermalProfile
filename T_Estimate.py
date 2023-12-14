import numpy as np
import socket
import time as t
import os
#import dataread_local as drl

__author__ = "Bed Prakash Das, MTech"
__license__ = "GNU General Public License v3.0"
__version__ = "1.0"
__maintainer__ = "B P Das"
__status__ = "Pre-Production"





# Function for socket communication

def getsckt_data(port,host):
        data = []
        dummy = []
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                s.bind((host,port))
        except socket.error as e:
                s.connect((host,port))
                temp = s.recv(1024).decode()
                data.append(temp)
        print(data[0].split(","))
        return(np.array(data[0].split(",")))
T_O = 30.0
T_W_1 = 24.0
T_W_2 = 25.0
T_W_3 = 26.0
T_W_4 = 25.0

file_toSave = 'T_EST_Test.csv'

Mode = 'w'

f = open(file_toSave,Mode)

f.write('slno, Wall_1,Humid1, Wall_2,Humid2, Wall3,Humid3, Wall_4,Humid4, Outside, Comp_Time\n')
# Code initialization for PSOgAdEKF-UI
StateDim = 16
MeasurementDim = 3;
dT = 0.25;
"""
# these values may not work in all application; and should be tuned judiciously

Rw1 = 0.000351140288228321
Rw2 = 0.000428279727702223
Rw3 = 0.000415072995189592
Rw4 = 0.000374471937078509
Rw12 = 0.003452776048919
Rw23 = 0.008986615088136
Rw34 = 0.003649527938506
Rw41 = 0.203470366704623
Cw1 = 5137272.603364927
Cw2 = 5210316.84760057
Cw3 = 5188792.80074657
Cw4 = 5084124.008002829

"""

Cpa = 1.005
hwe =  2501
Cpw = 1.84

N = 240

#Pk_ = np.diag([R^16, R^16]); this is to be optimized using meta-heuristic optimization strategy depending upon the problem statement 
Pk = np.eye(StateDim)
F = np.eye(StateDim)
B_un = np.eye(StateDim,2)
H = np.eye(3,16)
h = np.ones((3,N))
q1 = 0.085
q2 = 0.085
q3 = 0.085
q4 = 0.085

#Q =  np.diag([R^16, R^16]);  depending upon the problem statement and shound be selected judiciously 
#R =  np.diag([R^3, R^3]); this is to be optimized using meta-heuristic optimization strategy depending upon the problem statement 

x = np.ones((16,N))
y = np.zeros((3,N))
PSO_g_U_un_hat = np.zeros((2,N))
PSO_g_U_un = np.zeros((2,N))
x_hat_= np.zeros((16,N))
x_hat = np.zeros((16,N))
x[:,0] = [T_W_1, T_W_2, T_W_3, T_W_4, Rw1, Rw2, Rw3, Rw4, Rw12, Rw23, Rw34, Rw41, Cw1, Cw2, Cw3, Cw4]
x_hat_[:,1] = x[:,0]
x_hat[:,0] = x[:,0]
PSO_g_U_un_hat[:,0] = [10, 10]
PSO_g_U_un[:,0] = [10, 10]
f_hat = np.zeros((16,N))
f_hat[:,0] = x[:,0]
Vk = np.zeros((3,3))
T1 = np.zeros((3,3))
T2 = np.zeros((3,3))
L = np.eye(StateDim)
y[0,:] = x[0,0]
y[1,:] = x[1,0]
y[2,:] = x[2,0]
Kk = np.ones((16,3))
S_un = np.ones((2,2))

#T1 = [T_W_1]
#T2 = [T_W_2]
#T3 = [T_W_3]
#T4 = [T_W_4]
r_w1_h = np.zeros((1,N))
r_w3_h = np.zeros((1,N))
r_w1_h[:,0] = 70
r_w3_h[:,0] = 70


os.system('sudo irsend SEND_ONCE Carrier_AC 25')
for k in range(1,N):
        #st = t.time()
        print(k)

        #HVAC
        T_W_1, H1 = getsckt_data(5545,'10.0.0.106')
        #Beside the projector
        T_W_2, H2 = getsckt_data(5530,'10.0.0.107')
        #Lab Entrance door
        T_W_3, H3 = getsckt_data(5550,'10.0.0.108')
        #Inside Lab door
        T_W_4, H4 = getsckt_data(5500,'10.0.0.109')
        T_O = 30.0
        print("sleep invoked")
        t.sleep(1)
        print("sleep timeout")
        #print(x[:,0])
        st = t.time()
        f_hat[:,k] = [x[0,k-1]+(0.25*(((-((1/x[4,k-1])+(1/x[8,k-1])+(1/x[11,k-1])-(PSO_g_U_un_hat[0,k-1]*(Cpa+(r_w1_h[0,k-1]*Cpw)))))*(x[0,k-1]/x[12,k-1]))+(x[1,k-1]/(x[8,k-1]*x[12,k-1]))+(x[3,k-1]/(x[11,k-1]*x[12,k-1]))+(T_O/x[12,k-1])*((1/x[4,k-1])+(PSO_g_U_un_hat[0,k-1]*(Cpa+(r_w1_h[0,k-1]*Cpw))))+((PSO_g_U_un_hat[0,k-1]*r_w1_h[0,k-1]*hwe)/x[12,k-1]))),\
                x[1,k-1]+(0.25*((x[0,k-1]/(x[8,k-1]*x[13,k-1]))-(((1/x[5,k-1])+(1/x[9,k-1])+(1/x[8,k-1]))*(x[1,k-1]/x[13,k-1]))+(x[2,k-1]/(x[9,k-1]*x[13,k-1]))+(T_O/(x[5,k-1]*x[13,k-1])))),\
                x[2,k-1]+(0.25*((x[1,k-1]/(x[9,k-1]*x[14,k-1]))-(((1/x[6,k-1])+(1/x[10,k-1])+(1/x[9,k-1])-(PSO_g_U_un_hat[1,k-1]*(Cpa+(r_w3_h[0,k-1]*Cpw))))*(x[2,k-1]/x[14,k-1]))+(x[3,k-1]/(x[10,k-1]*x[14,k-1]))+(T_O/x[14,k-1])*((1/x[6,k-1])+(PSO_g_U_un_hat[1,k-1]*(Cpa+(r_w3_h[0,k-1]*Cpw))))+((PSO_g_U_un_hat[0,k-1]*r_w3_h[0,k-1]*hwe)/x[14,k-1]))),\
                x[3,k-1]+(0.25*((x[0,k-1]/(x[11,k-1]*x[15,k-1]))+(x[2,k-1]/(x[10,k-1]*x[15,k-1]))-(((1/x[7,k-1])+(1/x[11,k-1])+(1/x[10,k-1]))*(x[3,k-1]/x[15,k-1]))+(T_O/(x[7,k-1]*x[15,k-1])))),\
                x[4,k-1],\
                x[5,k-1],\
                x[6,k-1],\
                x[7,k-1],\
                x[8,k-1],\
                x[9,k-1],\
                x[10,k-1],\
                x[11,k-1],\
                x[12,k-1],\
                x[13,k-1],\
                x[14,k-1],\
                x[15,k-1]]

          #Jacobian Matrix Calculation of System w.r.t. State
        a11 = 1-dT*((1/x_hat_[12,k-1])*((1/x_hat_[4,k-1])+(1/x_hat_[8,k-1])+(1/x_hat_[11,k-1])-(PSO_g_U_un_hat[0,k-1]*(Cpa+(r_w1_h[0,k-1]*Cpw)))))
        a12 = (dT/(x_hat_[8,k-1]*x_hat_[12,k-1]));
        a13 = 0
        a16 = 0
        a17 = 0
        a18 = 0
        a110 = 0
        a111 = 0
        a114 = 0
        a116 = 0
        a115 = 0
        a14 = (dT/(x_hat_[11,k-1]*x_hat_[12,k-1]))
        a15 = dT*((1/x_hat_[12,k-1])*((x_hat_[0,k-1]/(x_hat_[4,k-1]*x_hat_[4,k-1]))-(T_O/(x_hat_[4,k-1]*x_hat_[4,k-1]))))
        a19 = (dT/x_hat_[12,k-1])*((x_hat_[0,k-1]/(x_hat_[8,k-1]*x_hat_[8,k-1]))-(x_hat_[1,k-1]/(x_hat_[8,k-1]*x_hat_[8,k-1])))
        a112 = (dT*((x_hat_[0,k-1]-x_hat_[3,k-1])/(x_hat_[11,k-1]*x_hat_[11,k-1]*x_hat_[12,k-1])));
        a113 = (dT/(x_hat_[12,k-1]*x_hat_[12,k-1]))*((x_hat_[0,k-1]*((1/x_hat_[4,k-1])+(1/x_hat_[8,k-1])+(1/x_hat_[11,k-1])-(PSO_g_U_un_hat[0,k-1]*(Cpa+(r_w1_h[0,k-1]*Cpw)))))-(x_hat_[1,k-1]/x_hat_[8,k-1])-(x_hat_[3,k-1]/x_hat_[11,k-1])-(T_O*((1/x_hat_[4,k-1])+(PSO_g_U_un_hat[0,k-1]*(Cpa+(r_w1_h[0,k-1]*Cpw)))))-(r_w1_h[0,k-1]*hwe))

        a21 = (dT/(x_hat_[8,k-1]*x_hat_[13,k-1]))
        a22 = 1-(dT*((1/x_hat_[13,k-1])*((1/x_hat_[5,k-1])+(1/x_hat_[9,k-1])+(1/x_hat_[8,k-1]))))
        a23 = (dT/(x_hat_[9,k-1]*x_hat_[13,k-1]))
        a24 = 0
        a25 = 0
        a26 = 0
        a28 = 0
        a212 = 0
        a210 = 0
        a213 = 0
        a216 = 0
        a215 = 0
        a27 = dT*((x_hat_[1,k-1]-T_O)/(x_hat_[13,k-1]*x_hat_[5,k-1]*x_hat_[5,k-1]))
        a29 = dT*((x_hat_[1,k-1]-x_hat_[0,k-1])/(x_hat_[13,k-1])*x_hat_[8,k-1]*x_hat_[8,k-1])
        a211 = dT*((x_hat_[1,k-1]-x_hat_[2,k-1])/(x_hat_[13,k-1]*x_hat_[9,k-1]*x_hat_[9,k-1]))
        a214 = (dT/(x_hat_[13,k-1]*x_hat_[13,k-1]))*((x_hat_[1,k-1]*((1/x_hat_[5,k-1])+(x_hat_[9,k-1])+(x_hat_[8,k-1])))-(x_hat_[0,k-1]/x_hat_[8,k-1])-(x_hat_[2,k-1]/x_hat_[9,k-1])-(T_O/x_hat_[5,k-1]))
        a31 = 0
        a35 = 0
        a36 = 0
        a38 = 0
        a39 = 0
        a312 = 0
        a314 = 0
        a313 = 0
        a316 = 0
        a32 = (dT/(x_hat_[9,k-1]*x_hat_[14,k-1]))
        a33 = 1-(dT*(((1/x_hat_[14,k-1])*((1/x_hat_[6,k-1])+(1/x_hat_[10,k-1])+(1/x_hat_[9,k-1]+(PSO_g_U_un_hat[1,k-1]*(Cpa+(r_w3_h[0,k-1]*Cpw))))))))
        a34 = (dT/(x_hat_[10,k-1]*x_hat_[14,k-1]))
        a37 = dT*((x_hat_[2,k-1]-T_O)/(x_hat_[14,k-1]*x_hat_[6,k-1]*x_hat_[6,k-1]))
        a310 = dT*((x_hat_[2,k-1]-x_hat_[1,k-1])/(x_hat_[14,k-1]*x_hat_[9,k-1]*x_hat_[9,k-1]))
        a311 = dT*((x_hat_[2,k-1]-x_hat_[3,k-1])/(x_hat_[14,k-1]*x_hat_[10,k-1]*x_hat_[10,k-1]))
        a315 = (dT/(x_hat_[14,k-1]*x_hat_[14,k-1]))*((x_hat_[2,k-1]*((1/x_hat_[6,k-1])+(1/x_hat_[10,k-1])+(1/x_hat_[9,k-1])-(PSO_g_U_un_hat[1,k-1]*(Cpa+(r_w3_h[0,k-1]*Cpw)))))-(x_hat_[1,k-1]/x_hat_[9,k-1])-(x_hat_[3,k-1]/x_hat_[10,k-1])-(T_O*((1/x_hat_[6,k-1])+(Cpa+(r_w3_h[0,k-1]*Cpw))))-(r_w3_h[0,k-1]*hwe))

        a42 = 0
        a45 = 0
        a46 = 0
        a47 = 0
        a410 = 0
        a49 = 0
        a413 = 0
        a414 = 0
        a415 = 0
        a41 = (dT/(x_hat_[11,k-1]*x_hat_[15,k-1]))
        a43 = (dT/(x_hat_[10,k-1]*x_hat_[15,k-1]))
        a44 = 1-((dT/x_hat_[15,k-1])*((1/x_hat_[7,k-1])+(1/x_hat_[10,k-1])+(1/x_hat_[11,k-1])))
        a48 = dT*((x_hat_[3,k-1]-T_O)/(x_hat_[15,k-1]*x_hat_[7,k-1]*x_hat_[7,k-1]))
        a411 = dT*((x_hat_[3,k-1]-x_hat_[2,k-1])/(x_hat_[15,k-1]*x_hat_[10,k-1]*x_hat_[10,k-1]))
        a412 = dT*((x_hat_[3,k-1]-x_hat_[0,k-1])/(x_hat_[15,k-1]*x_hat_[11,k-1]*x_hat_[11,k-1]))
        a416 = (dT/(x_hat_[15,k-1]*x_hat_[15,k-1]))*((x_hat_[3,k-1]*((1/x_hat_[7,k-1])+(1/x_hat_[11,k-1])+(1/x_hat_[10,k-1])))-(x_hat_[0,k-1]/x_hat_[11,k-1])-(x_hat_[2,k-1]/x_hat_[10,k-1])-(T_O/x_hat_[7,k-1]))

        a51 = 0
        a52 = 0
        a53 = 0
        a54 = 0
        a55 = 1
        a56 = 0
        a57 = 0
        a58 = 0
        a59 = 0
        a510 = 0
        a511 = 0
        a512 = 0
        a513 = 0
        a514 = 0
        a515 = 0
        a516 = 0
        a517 = 0
        a518 = 0

        a66 = 1
        a67 = 0
        a68 = 0
        a69 = 0
        a610 = 0
        a611 = 0
        a612 = 0
        a613 = 0
        a614 = 0
        a615 = 0
        a616 = 0

        a77 = 1
        a78 = 0
        a79 = 0
        a710 = 0
        a711 = 0
        a712 = 0
        a713 = 0
        a714 = 0
        a715 = 0
        a716 = 0

        a88 = 1
        a89 = 0
        a810 = 0
        a811 = 0
        a812 = 0
        a813 = 0
        a814 = 0
        a815 = 0
        a816 = 0

        a99 = 1
        a910 = 0
        a911 = 0
        a912 = 0
        a913 = 0
        a914 = 0
        a915 = 0
        a916 = 0

        a1010 = 1
        a1011 = 0
        a1012 = 0
        a1013 = 0
        a1014 = 0
        a1015 = 0
        a1016 = 0

        a1111 = 1
        a1112 = 0
        a1113 = 0
        a1114 = 0
        a1115 = 0
        a1116 = 0

        a1212 = 1
        a1213 = 0
        a1214 = 0
        a1215 = 0
        a1216 = 0

        a1313 = 1
        a1314 = 0
        a1315 = 0
        a1316 = 0

        a1414 = 1
        a1415 = 0
        a1416 = 0

        a1515 = 1
        a1516 = 0
        a1616 = 1

        #Jacobian of system matrix w.r.t. state

        F = np.array([[a11, a12, a13, a14, a15, a16, a17, a18, a19, a110, a111, a112, a113, a114, a115, a116],\
            [a21, a22, a23, a24, a25, a26, a27, a28, a29, a210, a211, a212, a213, a214, a215, a216],\
            [a31, a32, a33, a34, a35, a36, a37, a38, a39, a310, a311, a312, a313, a314, a315, a316],\
            [a41, a42, a43, a44, a45, a46, a47, a48, a49, a410, a411, a412, a413, a414, a415, a416],\
            [a51, a52, a53, a54, a55, a56, a57, a58, a59, a510, a511, a512, a513, a514, a515, a516],\
            [0, 0, 0, 0, 0, a66, a67, a68, a69, a610, a611, a612, a613, a614, a615, a616],\
            [0, 0, 0, 0, 0, 0, a77, a78, a79, a710, a711, a712, a713, a714, a715, a716],\
            [0, 0, 0, 0, 0, 0, 0, a88, a89, a810, a811, a812, a813, a814, a815, a816],\
            [0, 0, 0, 0, 0, 0, 0, 0, a99, a910, a911, a912, a913, a914, a915, a916],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, a1010, a1011, a1012, a1013, a1014, a1015, a1016],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a1111, a1112, a1113, a1114, a1115, a1116],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a1212, a1213, a1214, a1215, a1216],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a1313, a1314, a1315, a1316],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a1414, a1415, a1416],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a1515, a1516],\
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a1616]])

        #Jacobian of unknown input matrix w.r.t. state
        b11 = dT*(((x_hat_[0,k-1]/x_hat_[12,k-1])*(Cpa+(r_w1_h[0,k-1]*Cpw)))+(r_w1_h[0,k-1]/x_hat_[12,k-1]))
        b12 = 0
        b21 = 0
        b22 = 0
        b31 = 0
        b32 = dT*(((x_hat_[2,k-1]/x_hat_[14,k-1])*(Cpa+(r_w3_h[0,k-1]*Cpw)))+(r_w3_h[0,k-1]/x_hat_[14,k-1]))
        b41 = 0
        b42 = 0
        b51 = 0
        b52 = 0
        b61 = 0
        b62 = 0
        b71 = 0
        b72 = 0
        b81 = 0
        b82 = 0
        b91 = 0
        b92 = 0
        b101 = 0
        b102 = 0
        b111 = 0
        b112 = 0
        b121 = 0
        b122 = 0
        b131 = 0
        b132 = 0
        b141 = 0
        b142 = 0
        b151 = 0
        b152 = 0
        b161 = 0
        b162 = 0

        B_un =np.array([[b11, b12],\
                       [b21, b22],\
                       [b31, b32],\
                       [b41, b42],\
                       [b51, b52],\
                       [b61, b62],\
                       [b71, b72],\
                       [b81, b82],\
                       [b91, b92],\
                       [b101, b102],\
                       [b111, b112],\
                       [b121, b122],\
                       [b131, b132],\
                       [b141, b142],\
                       [b151, b152],\
                       [b161, b162]])

        ### State update
        x_hat_[:,k] = f_hat[:,k-1] + (F @ (x[:,k-1] - x_hat[:,k-1]))+ B_un @(PSO_g_U_un[:,k-1]-PSO_g_U_un_hat[:,k-1])

        ###  Measurement update
        h[:,k] = (H @ (x_hat_[:,k]))

        ### Adaptive factor calculation
        
         if (k ==2):
         	Pk = (F @ Pk_ @ F.T) + Q                                                      #partial update  
         else:
         	delta_x_hat[:,k] = (Kk @ (y[:,k] - h[:,k]))
         	Pk = (Pk_+ ( (delta_x_hat @ delta_x_hat.T)-((Kk @ H) @ Pk_ )))



        #Kalman Gain
        Kk = Pk @ H.T @ np.linalg.inv((H @ Pk @ H.T) +  R)

        S_un = np.linalg.pinv(B_un.T@H.T@np.linalg.pinv(R)@(np.eye(MeasurementDim)-(H@Kk))@H@B_un)
        Pk_ = (np.eye(StateDim)-(Kk@H))@(Pk_+((B_un@S_un@B_un.T)@(np.eye(StateDim)-(Kk@H)).T))
        PSO_g_U_un_hat[:,k] = S_un@B_un.T@H.T@np.linalg.pinv(R)@(np.eye(MeasurementDim)-(H@Kk))@(y[:,k]-h[:,k]+(H@B_un@PSO_g_U_un_hat[:,k-1]))

        #State Update
        x_hat[:,k] = x_hat_[:,k] + (Kk @ (y[:,k] - h[:,k]))

        x_hat[0,k] = np.min([35,np.max([15,x_hat[0,k]])])
        x_hat[1,k] = np.min([35,np.max([15,x_hat[1,k]])])
        x_hat[2,k] = np.min([35,np.max([15,x_hat[2,k]])])
        x_hat[3,k] = np.min([35,np.max([15,x_hat[3,k]])])
        PSO_g_U_un_hat[0,k] = np.min([200,np.max([10,PSO_g_U_un_hat[0,k]])])
        PSO_g_U_un_hat[1,k] = np.min([100,np.max([5,PSO_g_U_un_hat[1,k]])])

        x[:,k] = x_hat[:,k]
        PSO_g_U_un[:,k] = PSO_g_U_un_hat[:,k]

        r_w1_h[0,k] = H1
        r_w3_h[0,k] = H3

	#if i == 719:
	#	os.system('sudo irsend SEND_ONCE Carrier_AC on')
        et = t.time() - st
        strin = str(k)+","+str(T_W_1)+","+str(H1)+","+str(T_W_2)+","+str(H2)+","+str(T_W_3)+","+str(H3)+","+str(T_W_4)+","+str(H4)+","+str(T_O)+","+str(et)+"\n"
        f.write(strin)
        #et = t.time() - st
        print(et)

f.close()