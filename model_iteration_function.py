#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import numpy as np


# In[2]:


def model_iteration(Tol,Status_HrentPred,Status_Mode,Status_EmpPred,Time1,EmpSeCTot,EmpSeC,HS,BFS,Hrent0,Wage,HSExpShare):
    
    ### Model Parameters
    MaxITN = 5000         # max iteration times
    LLCoefIJ = np.array([[0.0,0.0]]) # log-linear transformation coef
    D = 250               # number of working days
    Lambda = np.array([[1.0,1.0]])  # dispersion parameter for location choice? (can't see those words after location)
    LT = len(Lambda[0])   # number of labour type
    
    ### Data Input
    # assuming same travel time for all SeCs
    Time = np.repeat(Time1[None,...],LT,axis=0)

    # travel distance matrix (Unit: km)
    Dist = Time 
    
    # define employment input
    if Status_EmpPred == 1:
        EmpInput = EmpSeCTot
    else:
        EmpInput = EmpSeC
        
    Hrent = Hrent0

    # number of zones - read from housing input
    ZNum = len(HS)

    # read zonal residual attractiveness term from file (saved on server)
    name_ZAT = 'ZAT'
    name_ZAttrI = 'ZAttrI'
    name_ZAttrIJ = 'ZAttrIJ'

    from functions import read_ZAT
    ZAttrI, ZAttrIJ = read_ZAT(LT,ZNum,name_ZAT,name_ZAttrI,name_ZAttrIJ) 
    # (cuz this function needs ZNum variable as well, I put it after generating ZNum variable? Otherwise cannot run actually..)

    
    ### Model Iteration
    from functions import ProbIJ_Mix, Update_Hrent, Calibrate_ZAttr

    start_time = time.time()

    if Status_HrentPred == 1:
        print('--------------------------- Iteration starts ------------------------')

        for k in list(range(1,MaxITN+1)):

            if k == MaxITN:
                print('-------------------------- MaxITN reached --------------------------')
                break

            Output = ProbIJ_Mix(Status_EmpPred,D,LLCoefIJ,Lambda,EmpInput,Time,Dist,HS,BFS,Hrent0,ZAttrIJ,ZAttrI,LT,ZNum) #add LT,ZNum
            Hrent, Error = Update_Hrent(Output,LT,ZNum,Wage,HSExpShare,Hrent0,HS)

            if Error < Tol:
                print('--------------------- Hrent Converged at ITN = {} ------------------'.format(k))
                break
            else:
                Hrent0 = 1.0*Hrent + 0.0*Hrent0
                continue

    else:
        print('--------------- Calculate location choice probability ---------------')
        Output = ProbIJ_Mix(Status_EmpPred,D,LLCoefIJ,Lambda,EmpInput,Time,Dist,HS,BFS,Hrent0,ZAttrIJ,ZAttrI,LT,ZNum)


    if Status_Mode == 1:
        print('---------------------- ZATTR Calibration start ----------------------')
        ZAttrIJ,ZAttrI = Calibrate_ZAttr(D,LLCoefIJ,Lambda,Time,HS,BFS,Hrent,LT,ZNum)
        sio.savemat('ZAT(Python).mat', {'ZAttrIJ':ZAttrIJ, 'ZAttrI':ZAttrI})

    print("Elapsed time is: %.4f seconds" % (time.time() - start_time)) 
    
    
    return Output, Hrent, Error, ZAttrIJ, ZAttrI


# In[ ]:




