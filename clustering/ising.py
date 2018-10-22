#runs a Markov chain towards higher (or lower) clustering, as defined by the happy 
#capy score in energy.py
#the proposal step is a swap of populations 
#at each step, the population at a node is preserved
#at each step, the total minority proportion in the state (rho) is preserved 

import numpy as np
from energy_new import sparse_capy
from energy_new import sparse_lonely_capy
from energy_new import sparse_inner_capy 
class ising:

	#specify temperature as beta
	#set target = 1.0 for moving towards higher clustering 
	#set target = 0.0 for moving towards lower clustering 
	#specify number of steps in the chain 
	def __init__(self, repvotes, demvotes, A, beta=2**20, target=1.0, steps=100):
		# vote totals
		self.repvotes = repvotes
		self.demvotes = demvotes

		# temperature
		self.beta = beta

		# adjacency matrix
		self.A = A

		self.target = target
		self.steps = steps
        
	def __iter__(self):
		self.counter = 0
		self.newrepvotes = np.array(self.repvotes)
		self.newdemvotes = np.array(self.demvotes)
		return self

	def __next__(self):
		'''
		iterator to give the next state in the ising_simulation
		'''
		if self.counter == self.steps:
			raise StopIteration
		self.counter += 1
		prop_rep, prop_dem = self.proposal(self.newrepvotes, self.newdemvotes)
		old_en = sparse_inner_capy(self.newrepvotes, self.newdemvotes, self.A)
		new_en = sparse_inner_capy(prop_rep, prop_dem, self.A)
        
		en = old_en
        
		if (old_en < self.target):
			swap = self.accept(old_en, new_en, self.beta)
		else:
			swap = self.accept(new_en, old_en, self.beta)
		if swap:
			en = new_en
			self.newrepvotes = prop_rep
			self.newdemvotes = prop_dem
		return self.newrepvotes, self.newdemvotes, en

	def __len__(self):
		return self.steps

	def accept(self, old, new, beta):
		'''
		metropolis hasting acceptance function for higher energies (i.e. always accept higher)
		old - old energy score
		new - new energy score

		### swap old and new to accept lower energies
		'''
		if new >= old:
			return True
		elif np.random.rand() < np.exp(-beta*(old-new)):
			return True
		else:
			return False

	#proposed change in republican and democrat vote vectors 
	def proposal(self, curr_rep, curr_dem):
		idx1 = 0
		idx2 = 0
		new_rep = np.array(curr_rep)
		new_dem = np.array(curr_dem)
		#choose two distinct nodes uniformly at random 
		while idx1 == idx2:
			idx1 = np.random.randint(0,curr_rep.size-1)
			idx2 = np.random.randint(0,curr_dem.size-1)
		#find the maximum number of people to swap by taking the minimum of the 
		#republican population at the first node and democratic population at second node
		max_num_swap = min(curr_rep[idx1], curr_dem[idx2])
		# let the swap number be chosen uniformly at random from 1 to max_num_swap 
		if max_num_swap > 1:
			num_swap = np.random.randint(1, max_num_swap)
		else:
			num_swap = 0
		#perform the swap by moving num_swap Democrats into node 1 and out of node 2 
		#and moving num_swap Republicans into node 2 and out of node 1 
		new_rep[idx1] -= num_swap
		new_rep[idx2] += num_swap
		new_dem[idx1] += num_swap
		new_dem[idx2] -= num_swap
		return new_rep, new_dem

	def set_target(self, target):
		self.target = target
