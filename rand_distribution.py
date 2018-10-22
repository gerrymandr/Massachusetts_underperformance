#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:06:45 2018

@author: Eug

Create a random distribution of vote shares of varying levels of variance
"""

import numpy as np
import csv
import copy
import matplotlib.pyplot as plt
from skew_test import truncate_skewed_normal

# Inputs
input_folder = 'Elections/'
input_name = 'pMassPres16'
input_end = '.csv'
output_folder = 'variance_sims/'
nth_series = '2'

d_index = 3
r_index = 4
total_index = 5
pop_index = 6



# Load in data
input_file = input_folder + input_name + input_end
with open(input_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    file_data = []
    for row in readCSV:
        file_data.append(row)

# Put data in desired format
d_votes = []
r_votes = []
total_votes = []
pop = []
for i in range(1, len(file_data)):
    d_votes.append(int(file_data[i][d_index]))
    r_votes.append(int(file_data[i][r_index]))
    total_votes.append(int(file_data[i][total_index]))
    pop.append(float(file_data[i][pop_index]))
      
# Calculate turnout and R share of votes for each geo unit
turnouts = []
r_shares = []
for i in range(len(total_votes)):
    turnouts.append(total_votes[i] / pop[i])
    r_shares.append(r_votes[i] / total_votes[i])


# Create new data sets and save them  
mean = .3525
for variance in range(2, 33, 1):
    var = variance / 1000
    r_new = truncate_skewed_normal(-8, mean, var, len(file_data), show=False, verbose=True)
    new_data = copy.deepcopy(file_data)
    new_data[0] += ['turnout', 'new_r_share', 'new_d_votes', 'new_r_votes']
    for i in range(0,len(new_data) - 1):
        new_data[i + 1].append(turnouts[i])
        new_data[i + 1].append(r_new[i])
        new_data[i + 1].append(total_votes[i] * (1 - r_new[i]))
        new_data[i + 1].append(total_votes[i] * r_new[i])
    
    output_file = output_folder + nth_series + '_var_' + str(var) + '_from_' + input_name + '.csv'
    with open(output_file, 'w', newline='') as outfile:
        out = csv.writer(outfile)
        for row in new_data:
            out.writerow(row)
            
    
    