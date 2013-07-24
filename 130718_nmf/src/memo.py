# Import nimfa library entry point for factorization
import nimfa

# Construct sparse matrix in CSR format, which will be our input for factorization
from scipy.sparse import csr_matrix
from scipy import array
from numpy import dot
V = csr_matrix((array([1,2,3,4,5,6]), array([0,2,2,0,1,2]), array([0,2,3,6])), shape=(3,3))

# Print this tiny matrix in dense format
print V.todense()

# Run Standard NMF rank 4 algorithm
# Update equations and cost function are Standard NMF specific parameters (among others).
# If not specified the Euclidean update and Frobenius cost function would be used.
# We don't specify initialization method. Algorithm specific or random initialization will be used.
# In Standard NMF case, by default random is used.
# Returned object is fitted factorization model. Through it user can access quality and performance measures.
# The fctr_res's attribute `fit` contains all the attributes of the factorization.
fctr = nimfa.mf(V, method = "nmf", max_iter = 30, rank = 4, update = 'divergence', objective = 'div')
fctr_res = nimfa.mf_run(fctr)

# Basis matrix. It is sparse, as input V was sparse as well.
W = fctr_res.basis()
print "Basis matrix"
print W.todense()

# Mixture matrix. We print this tiny matrix in dense format.
H = fctr_res.coef()
print "Coef"
print H.todense()

# Return the loss function according to Kullback-Leibler divergence. By default Euclidean metric is used.
print "Distance Kullback-Leibler: %5.3e" % fctr_res.distance(metric = "kl")

# Compute generic set of measures to evaluate the quality of the factorization
sm = fctr_res.summary()
# Print sparseness (Hoyer, 2004) of basis and mixture matrix
print "Sparseness Basis: %5.3f  Mixture: %5.3f" % (sm['sparseness'][0], sm['sparseness'][1])
# Print actual number of iterations performed
print "Iterations: %d" % sm['n_iter']

# Print estimate of target matrix V
print "Estimate"
print dot(W.todense(), H.todense())