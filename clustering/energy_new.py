# implements the happy capy score and the lonely capy score for measuring clustering 
# to speed up computations, sparse matrices are used (although the implementations without
# sparsity are also retained)
# use sparse_capy(x,y,A) to obtain the happy capy score given vote vectors x and y and 
# an adjacency matrix A, where the indexing is consistent across x,y,A  
# use the sparse_lonely_capy(x,y,A) to obtain lonely capy score for y given vote vectors
# x and y and an adjacency matrix A, where indexing is consistent across x,y,A

from scipy.sparse import identity
import numpy as np

def self_energy(x, A):
    '''
    x - population vector for x
    A - adjacency matrix for graph
    
    return - energy score of cluster
    '''
    result = np.matmul(x.T, np.matmul(A + np.identity(A[0].size), x)) - np.dot(x.T, np.ones((A[0].size,1)))
    return result[0,0]/2

def sparse_self_energy(x, A):
    '''
    x - population vector for x
    A - sparse adjacency matrix for graph
    
    return - energy score of cluster
    '''
    M = A + identity(A.shape[0])
    first = np.dot(x.T, M.dot(x))
    second = np.dot(x.T, np.ones((A.shape[0],1)))
    result = first - second
    return result[0,0]/2 
    
def diff_energy(x, y, A):
    '''
    x - population vector for x
    y - population vector for y
    A - adjacency matrix for graph
    
    return - energy score of cluster
    '''
    result = np.matmul(x.T, np.matmul(A + np.identity(A[0].size), y))
    return result[0,0]

def sparse_diff_energy(x, y, A):
    '''
    x - population vector for x
    y - population vector for y
    A - sparse adjacency matrix for graph
    
    return - energy score of cluster
    '''
    M = A + identity(A.shape[0])
    return np.dot(x.T, M.dot(y))[0,0]

def sparse_inner_product(x, y, A):
    '''
    x - population vector for x 
    y - population vector for y 
    A - sparse adjacency matrix for graph
    
    return - energy score of cluster
    '''
    M = A + identity(A.shape[0])
    result = np.dot(x.T, M.dot(y))
    return result
    
def sparse_inner_capy(x,y,A):
    '''
    x - population vector for x
    y - population vector for y
    A - sparse adjacency matrix for graph
    
    return - the inner product capy score
    '''
    xx = sparse_inner_product(x, x, A)
    xy = sparse_inner_product(x, y, A)
    yy = sparse_inner_product(y, y, A) 
    return (xx/(xx+xy) + yy/(yy+xy))/2

def capy(x,y,A):
    '''
    x - population vector for x
    y - population vector for y
    A - adjacency matrix for graph
    
    return - the capy score
    '''
    xx = self_energy(x,A)
    xy = diff_energy(x,y,A)
    yy = self_energy(y,A)
    return (xx/(xx+xy) + yy/(yy+xy))/2

def sparse_capy(x,y,A):
    '''
    x - population vector for x
    y - population vector for y
    A - sparse adjacency matrix for graph
    
    return - the capy score
    '''
    xx = sparse_self_energy(x,A)
    xy = sparse_diff_energy(x,y,A)
    yy = sparse_self_energy(y,A)
    return (xx/(xx+xy) + yy/(yy+xy))/2

def sparse_lonely_capy(x,y,A):
    '''
    x - population vector for x
    y - population vector for y 
    A - sparse adjacency matrix for graph 
    
    return - the lonely capy score 
    '''
    yy = sparse_self_energy(y,A)
    xy = sparse_diff_energy(x,y,A)
    return yy/(yy+xy)