#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


## Model Parameters (DO NOT CHANGE)

Tol = 1e-6            # tolerance for model convergence
Status_Mode = 0       # 1: Calibdation mode; 0: Forecast mode
Status_EmpPred = 1    # 1: Predict emp-residential location pair; 0: Predict residential location only 
Status_HrentPred = 1  # 1: Endogenous house rents; 0: Exogenous house rents

# MaxITN = 5000         # max iteration times
# LLCoefIJ = np.array([[0.0,0.0]]) # log-linear transformation coef
# D = 250               # number of working days
# Lambda = np.array([[1.0,1.0]])  # dispersion parameter for location choice? (can't see those words after location)
# LT = len(Lambda[0])   # number of labour type


# In[ ]:




