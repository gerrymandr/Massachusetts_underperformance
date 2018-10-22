#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 21:09:04 2018

@author: Eug

Make histograms of the R share of the vote in political units
"""

import numpy as np
import csv
from operator import itemgetter
import math
import matplotlib.pyplot as plt

input_files = [
        'Elections/MassPres00.csv',
        'Elections/MassPres04.csv',
        'Elections/MassPres08.csv',
        'Elections/MassPres12.csv',
        'Elections/MassPres16.csv',
        'Elections/MassSen00.csv',
        'Elections/MassSen02.csv',
        'Elections/MassSen06.csv',
        'Elections/MassSen08.csv',
        'Elections/MassSen10.csv',
        'Elections/MassSen12.csv',
        'Elections/MassSen13.csv',
        'Elections/MassSen14.csv'
        ]
num_congressional = [9] * len(input_files)

d_index = 2
r_index = 3
pop_index = 4

for i in range(len(input_files)):
    # load in data
    with open(input_files[i]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        file_data = []
        for row in readCSV:
            file_data.append(row)
    file_data = np.transpose(file_data)
    # prune data
    d_votes = file_data[d_index][1:]
    r_votes = file_data[r_index][1:]
    pop = file_data[pop_index][1:]        
    data = np.transpose([d_votes, r_votes, pop])
    data = list(data)
    
    x_is = []
    r_total = 0
    vote_total = 0
    for town in data:
        x_is.append(int(town[1]) / (int(town[0]) + int(town[1])))
        r_total += int(town[1])
        vote_total += int(town[0]) + int(town[1])
    state_average = r_total / vote_total
    
    
    plt.figure()
    plt.title(input_files[i])
    plt.xlabel('R share')
    plt.xlim(0,1)
    plt.ylabel('units')
    plt.ylim(0, 100)
    plt.axvline(x=state_average, color='r', label='State average')
    plt.hist(x_is)
    plt.show()