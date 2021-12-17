from scipy.sparse import coo_matrix

a = coo_matrix((10, 10))

print(a.toarray())
