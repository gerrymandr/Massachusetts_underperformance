#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 10:38:44 2018

@author: Eug

Takes the population of towns and divides it amongst the towns' voting precincts
proportional to each precinct's share of the town's vote.
"""


import csv

pop00_file = '/Users/Eug/Documents/VRDI/Massachusetts/Elections/MassPres00.csv'
pop10_file = '/Users/Eug/Documents/VRDI/Massachusetts/Elections/MassPres16.csv'

#'Users/Eug/Documents/VRDI/Massachusetts/raw_vote/PD43+__2002_U_S_Senate_General_Election_including_precincts'
#'Users/Eug/Documents/VRDI/Massachusetts/raw_vote/PD43+__2004_President_General_Election_including_precincts'

input_file = '''/Users/Eug/Documents/VRDI/Massachusetts/raw_vote/PD43+__2016_
President_General_Election_including_precincts.csv'''
pop_file = pop10_file
output_file = '/Users/Eug/Documents/VRDI/Massachusetts/Elections/pMassPres16.csv'

# For each town, town_data has an entry that stores that town's population and 
# total votes

# Here we create town_data and give it population data 
with open(pop_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    town_data = {}
    for row in readCSV:
        town_data[row[0]] = [row[4], 0]
        
    
# Load up precinct vote data
with open(input_file) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    file_data = []
    for row in readCSV:
        # Clean the input for computer use
        for i in range(len(row)):
            row[i] = row[i].replace(',', '')
            row[i] = row[i].replace('N.', 'North')
            row[i] = row[i].replace('S.', 'South')
            row[i] = row[i].replace('W.', 'West')
        file_data.append(row[:6])
    # get rid of the totals
    file_data = file_data[0:-1]

# Add each town's total votes to town_data
for i in range(1, len(file_data)):
    town_data[file_data[i][0]][1] += int(file_data[i][5])
    
# Add a column to file data storing each precinct's share of the town's 
# population by its share of the town's total vote
file_data[0].append('pop by share of vote')
for i in range(1, len(file_data)):
    file_data[i].append(int(town_data[file_data[i][0]][0]) * (int(file_data[i][5]) / town_data[file_data[i][0]][1]))

with open(output_file, 'w', newline='') as out_file:
    out = csv.writer(out_file)
    for i in file_data:
        out.writerow(i)
    