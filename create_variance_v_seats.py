#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 11:58:42 2018

@author: Eug

Code to make the variance v seats graphic
"""

import matplotlib.pyplot as plt
import numpy as np

input_file = 'variance_sims/variance_v_seats.csv'

file_data = []
infile = open(input_file, 'r')
for row in infile:
    string = row.replace('\n','')
    file_data.append(string.split(','))
    
data = np.transpose(file_data)
variance = list(data[0][1:])
feasible = list(data[1][1:])
for i in range(len(variance)):
    variance[i] = float(variance[i])
    feasible[i] = int(feasible[i])
    
plt.figure()
plt.title('Variance vs Feasible seats, mean = 35.25 %') 
plt.plot(variance, feasible)
xmin, xmax = plt.xlim()
plt.hlines(.3525 * 9, xmin, xmax, colors='r', label='Proportional representation')
plt.xticks(np.arange(.002, .033, step=0.006))
plt.legend()
plt.xlabel('Variance')
plt.ylabel('Feasible number of seats')
plt.show()