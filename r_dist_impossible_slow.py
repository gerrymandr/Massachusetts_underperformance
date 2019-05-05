#Summary: This code is for calculating the exact 'feasibility' bound
#described in the paper: 
#"LOCATING THE REPRESENTATIONAL BASELINE: REPUBLICANS IN MASSACHUSETTS"
#
#The simple greedy algorithm described in detail in the paper suffices
# in most cases, but can produce wide bounds in some cases with large
# geographic unit (towns). The algorithm below is guaranteed to produce 
# precise bounds at the cost of a higher runtime, ~ O(nW) with n being the 
# number of units and W being their total population. Designed to run on 
# town-level data, running on precinct data or similar is not recommended.
#
#
#Looking at the feasibility problem as maximizing the 'value' (population)
# of one district by fitting in geographic units (items) without exceeding
# the 'weight' limit (Republican margin must be positive), it is equivalent
# to the well-known 0-1 knapsack problem. This algorithm is based on a 
# psuedo-polynomial dynamic algorithm for the 0-1 knapsack problem. It 
# first removes all Republican majority units and uses their buffer of a 
# Republican margin as the maximum 'weight' of the district. It then tests 
# which Democratic majority units to add without exceeding that weight in 
# Democratic margin. As a dynamic algorithm, it breaks the feasibility problem
# into many linked subproblems. The subproblem with input [n,w] asks: What 
# is the largest district that can be built using the first n units and 
# allowing a maximum of w in Democratic margin? To solve this, it recursively 
# compares the largest possible district which does vs doesn't include the 
# nth unit (subproblem [n-1, w] vs. subproblem [n-1, w-w_n] + p_n, where 
# w_n is the Democratic margin of the nth unit and p_n is its population.
# The algorithm starts with the maximum n and w and recursively solves
# and stores subproblems as necessary.
#
#
#
#Instructions:
#Read in voting data.
#Instantiate a variable called margin as a numpy array with a row for 
# each geographic unit, and 2 columns.
#The first column being the Republican voting margin per geographic unit
# (Total Republican votes - Total Democrat votes),
# and the second being the total population for a given geographic unit.


import numpy as np
#Example code, for running on the 2013 Senate dataset from
#https://github.com/gerrymandr/Massachusetts_underperformance/blob/master/Elections_revised/Towns/SEN13.xlsx:
#
#import pandas as pd
#
#margin = pd.read_excel('SEN13.xlsx', usecols = [2,5])
#
#margin = np.array(margin)
#margin[:,[0, 1]] = margin[:,[1, 0]]

#w_max first stores the republican margin from all republican majority units, 
# then is used as the maximum 'weight' of democratic margin allowed after.
w_max = 0

#pop tracks the total population accumulated in the large Republican majority
# district being constructed.
pop = 0

#Sort by Republic margin
margin[margin[:,0].argsort(),:]

#Remove and account for Republican majority units
for i in range(len(margin)):
	if margin[i,0] < 0:
		break
	w_max += margin[i,0]
	pop += margin[i,1]

dem_margin = margin[i:,]
dem_margin[:,0] = -dem_margin[:,0]

#Table stores values for each sub-problem. table[n,w] is the population 
# of the largest possible Republican majority district that can be constructed
# using the first (n+1) units in dem_margin, allowing for a maximum of w
# democratic margin. Values which haven't been calculated yet are given
# a value of -1.
table = np.zeros((len(dem_margin), w_max+1), dtype = np.int64) - 1

#Returns the value of table[n,w]. If not yet calculated, calculates it recursively.
def check(n, w):
	#base cases
	if(n < 0):
		return 0
	if(w <= 0):
		table[n,w] = 0
	#If table[n,w] hasn't been calculated yet, calculate it
	elif table[n,w] == -1:
		#Maximum value without using the nth unit
		dont_add = check(n-1,w)
		#If nth unit can't fit, don't use it
		if dem_margin[n,0] > w:
			table[n,w] = dont_add
		else:
			#Maximum value using the nth unit
			add = check(n-1, w - dem_margin[n,0]) + dem_margin[n,1]
			#Pick option which produces a larger district
			table[n,w] = max(add, dont_add)
	return table[n,w]

#Combine population from Republican and Democrat majority units
pop = pop + check(len(dem_margin)-1, w_max)

#pop divided by the ideal district size (727514 in this example)
# and rounded down gives the feasibility bound. The infeasibility 
# bound is 1 above this.
print(pop)