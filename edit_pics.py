#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 14:48:09 2018

@author: Eug
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 21:09:04 2018

@author: Eug
"""

import numpy as np
import csv
from operator import itemgetter
import math
import matplotlib.pyplot as plt
import matplotlib

input_files = [
        'Elections/MassPres00.csv',
        'Elections/MassPres16.csv'
        ]
num_congressional = [9] * len(input_files)
titles = [
        '2000 Presidential election',
        '2016 Presidential election',
        ]

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
    
    
    
    font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 24}

    matplotlib.rc('font', **font)
    plt.figure()
    plt.title(titles[i])
    plt.xlabel('R share')
    plt.xlim(0,1)
    plt.ylabel('Number of towns')
    plt.ylim(0, 100)
    plt.axvline(x=np.mean(x_is), color='r', label='Mean')
    plt.axvline(x=np.median(x_is), color='orange', label='Median')
    plt.hist(x_is)
    plt.legend()
    plt.show()