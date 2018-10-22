
# coding: utf-8

# In[17]:

# This code calculates basic statistics, given an array of Republican votes, Democratic votes, and district assignments 

import numpy as np 
import matplotlib.pyplot as plt


# In[20]:


#given an arrays of repvotes, demvotes, and districtings indexed consistently, calculate seat share of first arg
def seat_share(repvote, demvote, dists):
    repvote = np.array(repvote)
    demvote = np.array(demvote)
    dists = np.array(dists)
    seats = 0
    for i in np.unique(dists):
        result = np.sum(repvote[dists == i] - demvote[dists == i])
        if result > 0:
            seats +=1.0
            #print(i)
        elif result == 0:
            seats += 0.5
    return seats

#given an array of cluster scores and an array of seat shares, plot seats against cluster 
def seats_vs_energy(energy_scores, seats):
    plt.scatter(energy_scores, seats)
    plt.xlabel("cluster scores")
    plt.ylabel("seats won")
    plt.show()

#given an array of cluster scores and an array of seat shares, plot seats against cluster using bucketing
#bucket_length indicates the number of points to be averaged per bucket 
def means_seats_vs_energy(energy_scores, seats, bucket_length):
    energy_scores = np.array(energy_scores)
    seats = np.array(seats)
    idx = np.argsort(energy_scores)
    energy_scores = np.sort(energy_scores)
    seats = seats[idx]
        
    scores_bucketed = []
    seats_bucketed = []
    for i in range(len(energy_scores) // bucket_length):
        running_total_seats = 0 
        running_total_energy = 0
        for j in range(bucket_length):
            running_total_seats += seats[bucket_length*i+j]
            running_total_energy += energy_scores[bucket_length*i+j]
        scores_bucketed.append(running_total_energy/bucket_length)
        seats_bucketed.append(running_total_seats/bucket_length)
    
    if len(energy_scores)% bucket_length != 0 :
        running_total_seats = 0 
        running_total_energy = 0
        idx = bucket_length*(len(energy_scores) // bucket_length)
        count = 0 
        while idx < len(energy_scores): 
            running_total_seats += seats[idx]
            running_total_energy += energy_scores[idx]
            count +=1
            idx +=1
        seats_bucketed.append(running_total_seats/count)
        scores_bucketed.append(running_total_energy/count)
        
    plt.scatter(scores_bucketed, seats_bucketed)
    plt.xlabel("scores_bucketed")
    plt.ylabel("seats_bucketed")
    plt.show()

#This method calculates the number of toss-up seats for republicans, up to a specified epsilon 
#(seats that are won with 0.5+epsilon of the votes)
def repubs_tossup_seats(dems, repubs, districtings, epsilon):
    if epsilon > 0.5:
        raise "epsilon must be less than or equal to 0.5"
    count = 0 
    for i in np.unique(districtings):
        result = np.sum(repubs[districtings == i]) / np.sum(repubs[districtings == i] + dems[districtings == i])
        if result <= 0.5 + epsilon and result >= 0.5: 
            count += 1.0 
    return count
            
#This method calculates the number of toss-up seats for democrats, up to a specified epsilon 
#(seats that are won with 0.5+epsilon of the votes)
def dems_tossup_seats(dems, repubs, districtings, epsilon):
    return repubs_tossup_seats(repubs, dems, districtings, epsilon) 
            
#This method calculates the number of nearly guaranteed seats for republicans, up to a specified epsilon 
#(seats that are won with 1-epsilon of the votes)
def repubs_guaranteed_seats(dems, repubs, districtings, epsilon):
    if epsilon > 0.5:
        raise "epsilon must be less than or equal to 0.5"
    count = 0 
    for i in np.unique(districtings):
        result = np.sum(repubs[districtings == i]) / np.sum(repubs[districtings == i] + dems[districtings == i])
        if result >= 1 - epsilon:
            count += 1.0 
    return count 

#This method calculates the number of nearly guaranteed seats for democrats, up to a specified epsilon 
#(seats that are won with 1-epsilon of the votes)
def dems_guaranteed_seats(dems, repubs, districtings, epsilon):
    return repubs_guaranteed_seats(repubs, dems, districtings, epsilon)
