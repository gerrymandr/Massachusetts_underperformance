#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 14:29:25 2018

Collects the salient information from the data files and collects them
into one labeled file.

@author: Eug
"""

import csv
import numpy as np

input_files = [
        'Pres04',
        'Pres08',
        'Pres12',
        'Pres16',
        'Sen02',
        'Sen06',
        'Sen08',
        'Sen10',
        'Sen12',
        'Sen13',
        'Sen14'
        ]
num_congressional = [9] * len(input_files)

d_index = 3
r_index = 4
pop_index = 6

races = []
labels = []
for i in range(len(input_files)):
    infile = 'Elections/pMass' + input_files[i] + '.csv'
    # load in data
    with open(infile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        file_data = []
        for row in readCSV:
            file_data.append(row)
    file_data = np.transpose(file_data)
    # prune data
    labels += [input_files[i] + 'D']
    d_votes = file_data[d_index][1:]
    labels += [input_files[i] + 'R']
    r_votes = file_data[r_index][1:]
    labels += [input_files[i] + 'Pop']
    pop = file_data[pop_index][1:]
    races.append([d_votes, r_votes, pop])
    
with open('MassPrecinctsAllYears.csv', 'w', newline='') as outfile:
    row = ''
    for label in labels:
        row += label + ','
    outfile.write(row[:-1] + '\n')
    for i in range(2175):
        row = ''
        for j in races:
            for k in range(len(j)):
                if i < len(j[k]):
                    row += str(j[k][i]) 
                row += ','
        row = row[:-1]
        row += '\n'
        outfile.write(row)
    
    
    