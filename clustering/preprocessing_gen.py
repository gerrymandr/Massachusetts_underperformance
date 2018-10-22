#Preprocesses data given in the config file, which in turn pulls from a shapefile 
#Returns dual graph for state, along with a list of numpy arrays called data_vectors
#Each element in this list is itself a numpy array of data specified in config file (districtings, vote shares, etc.)
#The order of these arrays in the list data_vectors is maintained from the order specified in the columns section of the config 
#Each numpy array is indexed in the same order as dual_graph.nodes
#Returns pos vector, containing centroids of nodes, used for drawing graph 
#Returns node_size vector, containing node_sizes that are proportional to the population of a node
#Indexing consisting across all of the above, and in particular, is in the order of the node list of dual_graph 
#WARNING: this order is different from the order of the attribute table of the shapefile (since the order is based on how the dual_graph is constructed)

import configparser
import networkx as nx
import numpy as np
from make_graph import construct_graph_from_file
import geopandas as gpd
import matplotlib.pyplot as plt
import shapefile as shp

def get_data(config_file):	
	########## Inputs ##########
	# read in config file
	config = configparser.ConfigParser()
	config.read(config_file)

	# shapefile and unique ID info
	shapefile = config['shapefile']['fname']
	geoid = config['shapefile']['geoid']

	# get column names from votes and districtings to read
	cols = []
	columns = config['columns']
	for key in columns:
		cols.append(columns[key])

	# optional demographic data
	if 'demographics' in config:
		for key in config['demographics']:
			cols.append(config['demographics'][key])
	# make dual graph
	dual_graph = construct_graph_from_file(shapefile, geoid, cols)
	num_nodes = dual_graph.number_of_nodes()
	
	#list of vectors 
	data_vectors = []
	#list of vector indexed by nodes
	data_vectors_att = []
	# streamline the process
	for key in columns:
		vector = np.zeros((num_nodes,1))
		vector_att = nx.get_node_attributes(dual_graph, columns[key])
		data_vectors.append(vector)
		data_vectors_att.append(vector_att)
        
	# get position data for drawing nodes at centroids
	df_vtd = gpd.read_file(shapefile)
	vtd_centroids = df_vtd.centroid
	vtd_x = vtd_centroids.x
	vtd_y = vtd_centroids.y
    
	inverse = {}
	sf = shp.Reader(shapefile)
	for i in range(len(sf.fields)):
		if sf.fields[i][0] == geoid:
			idx = i-1
			break
	records = sf.records()
	for i in range(len(records)):
		inverse[records[i][idx]] = i
        
	# assign attributes in order of nodes to match adjacency matrix
	for i in range(len(data_vectors)):
		count = 0 
		for node in dual_graph.nodes():
			data_vectors[i][count] = data_vectors_att[i][node]
			count += 1

	pos = {}                
	for node in dual_graph.nodes():
		pos[node] = (vtd_x[inverse[node]], vtd_y[inverse[node]])

	node_size = [(data_vectors[1][i] + data_vectors[2][i])/500 for i in range(dual_graph.number_of_nodes())]

	return dual_graph, data_vectors, pos, node_size

