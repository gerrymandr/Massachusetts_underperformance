#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:32:49 2018

@author: Eug
"""
import numpy as np
import csv
from operator import itemgetter
import math
import os

def test(data, num_congressional):
    # find ideal population per district
    total_pop = 0
    for i in range(len(data)):
        total_pop += data[i][2]
    ideal_pop =  total_pop / num_congressional
    
    # find republican share of two way vote
    r_vote = 0
    twoway_vote = 0
    for town in data:
        r_vote += town[1]
        twoway_vote += town[1] + town[0]
    r_share = r_vote / twoway_vote
    
    # find Republican benefit thingy
    for l in range(len(data)):

        try:
            data[l].append((data[l][1] - data[l][0]) / data[l][2])
        except ZeroDivisionError:
            if feedback:
                print('precinct index: ', l)
                print('total votes: ', data[l][2])
            data[l].append(0)
    
    data_sorted = sorted(data, key=itemgetter(3), reverse=True)
    
    pop_r = 0
    pop_r_small = 0
    pop_r_large = 0
    r_extra = 0
    for town in data_sorted:
        r_extra += (town[1] - town[0])
        if r_extra < 0: 
            r_extra -= (town[1] - town[0])
            pop_r_small = pop_r
            pop_r_large = pop_r_small + town[2]
            break
        else:
            pop_r += town[2]
    if pop_r_small == 0:
        pop_r_small = pop_r
        pop_r_large = pop_r
    feasible = pop_r_small / ideal_pop
    if math.isclose(feasible, round(feasible), abs_tol=.001):
        feasible = round(feasible)
    feasible = math.floor(feasible)
    if feasible > 0:
        print('***********')
    print('Ideal district population: ', ideal_pop)
    print('R share of two way vote: ', r_share)
    print('Pop R retaining majority: ', pop_r_small)
    print('R majority districts possible: ', feasible)
    print('Pop R just after losing majority: ', pop_r_large)
    proto_infeasible = pop_r_large / ideal_pop
    if math.isclose(proto_infeasible, round(proto_infeasible), abs_tol=.001):
        proto_infeasible = round(proto_infeasible)
    infeasible = math.floor(proto_infeasible) + 1
    print('R majority districts impossible:', infeasible )
    if feasible > 0:
        print('***********')
    print()

        
'''    
# Uncomment to use all generated distributions

input_folder = 'variance_sims/'
input_files_names = os.listdir(input_folder)     
input_files = []
for i in input_files_names:
    if i[0] != '.':
        input_files.append(input_folder + i)
 '''
    
# Uncomment to use real data
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


'''
# Uncomment to use generated distributions
input_folder = 'variance_sims/'
input_files = []
var_num = .002
for i in range(31):
    var_num = (i + 2) / 1000 
    num = str(var_num)
    input_files.append(input_folder + 'var_' + num + '_from_pMassPres16.csv')
'''

num_congressional = [9] * len(input_files)

d_index = 2
r_index = 3
pop_index = 4
feedback = False


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
    for j in range(len(data)):
        data[j] = list(data[j])
        for k in range(len(data[j])):
            data[j][k] = float(data[j][k])
    
    print('From ', input_files[i])
    test(data, num_congressional[i])    


    