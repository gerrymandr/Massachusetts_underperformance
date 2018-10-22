#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 10:26:52 2018

@author: Eug

Create a skewed normal distribution truncated to between 0 and 1 with desired
mean and variance
"""

from scipy.stats import skewnorm
import numpy as np
import matplotlib.pyplot as plt
import math

# Create a skewed normal distribution of the given length truncated to between
# 0 and 1
def truncated(a, loc, scale, size):
    data = skewnorm.rvs(a, loc=loc, scale=scale, size=size)
    for i in range(size):
        while data[i] < 0 or data[i] > 1:
            data[i] = skewnorm.rvs(a, loc=loc, scale=scale)
    return data
   
# Calculate the loc and scale of the skewed normal distribution from the
# desired mean and variance
def calc(a, mean, variance):
    scale = math.sqrt(variance /(1 - (2 * a * a)/(math.pi * (1 + a * a))))
    loc = mean - scale * (a / math.sqrt(1 + a * a)) * math.sqrt(2 / math.pi)
    return loc, scale

# Truncating messes with mean and variance, so this finds a fake mean and 
# variance that when truncated gives a distribution of the desired mean and 
# variance            
def finetune(a, mean, variance, size, verbose=False):
    # Set up variables that will be finetuned
    curr_var = variance
    curr_mean = mean
    
    # Keep looping until fine tuned enough, the loop breaks out from within
    attempt = 0
    while True:
        # Outputs to let user know the program is progressing
        attempt += 1
        if verbose:
            if attempt % 1000 == 0:
                print('On attempt ', attempt, ' to try and find a distribution')
                if attempt % 10000 == 0:
                    print('last var: ', np.var(data), 'and last mean: ', np.mean(data))
                    print('curr_var: ', curr_var, ' and curr_mean: ', curr_mean)
        
        # Calculate loc and scale from mean and variance
        # Then create a data sampling
        loc, scale = calc(a, curr_mean,curr_var)
        data = truncated(a, loc, scale, size)
    
        # If the truncated data is close to the desired moments, then we are
        # done fine tuning.  If not, slightly change the variables.  Better 
        # luck next time!
        var_close = np.isclose(np.var(data), variance, atol=.0001)
        mean_close = np.isclose(np.mean(data), mean, atol=.0001)
        if var_close:
            if mean_close:
                break
            else: 
                if np.mean(data) < mean:
                    curr_mean += .0005
                elif np.mean(data) > mean:
                    curr_mean -= .0005           
        else:
            if np.var(data) < variance:
                curr_var += .005
            elif np.var(data) > variance:
                curr_var -= .001
    # Return acceptible data 
    return data
           
# Nice wrapper for finetune() to import into another file      
def truncate_skewed_normal(a, mean, variance, size, show=False, verbose=False):
    data = finetune(a, mean, variance, size, verbose)
    
    if show:
        plt.figure()
        plt.hist(data, density=True)
        plt.title('mean = ', mean, ', variance = ', variance)
        plt.xlabel('R share')
        plt.ylabel('Probability density')
        plt.xlim(0,1)
        plt.axvline(x=mean, label='Mean', color='r')
        plt.legend()
        
    return data

'''
#Uncomment to use functions within this file
        
# Inputs
a = -8
mean = .3525
variance = .1
size = 1000

# Graph initial pdf
loc, scale = calc(a, mean, variance)
fig, ax = plt.subplots(1, 1)
x = np.linspace(skewnorm.ppf(0.01, a, loc=loc, scale=scale),
                skewnorm.ppf(0.99, a, loc=loc, scale=scale), 100)
ax.plot(x, skewnorm.pdf(x, a,loc=loc, scale=scale), 'r-', lw=5, alpha=0.6, label='skewnorm pdf')

# machine learn the right variables for truncation
data = finetune(a, mean, variance, size)

# Make picture
plt.hist(data, density=True)
plt.xlim(0,1)
plt.axvline(x=mean, label='Mean', color='r')
print('mean: ', np.mean(data))
print('variance: ', np.var(data))
'''