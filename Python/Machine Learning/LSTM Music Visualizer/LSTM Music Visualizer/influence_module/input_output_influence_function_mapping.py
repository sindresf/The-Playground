# The 9 mappings from input to output based on point(x,y) and color(r,g,b)
import numpy as np
def P2P(m,p,c):
    # reshape input to be [samples, time steps, features]
    p = np.reshape(p, (p.shape[0], 1, p.shape[1]))
    p = m.predict(p)
    # reshape output to be [samples, features]
    p = np.reshape(p, (p.shape[0], p.shape[2]))
    return p, c

def P2C(m,p,c):
    # reshape input to be [samples, time steps, features]
    p = np.reshape(p, (p.shape[0], 1, p.shape[1]))
    return p, m.predict(p)

def P2PC(m,p,c):
    # reshape input to be [samples, time steps, features]
    p = np.reshape(p, (p.shape[0], 1, p.shape[1]))
    preds = m.predict(p)
    return preds[0:1], preds[2:4]

def C2P(m,p,c):
    # reshape input to be [samples, time steps, features]
    c = np.reshape(c, (c.shape[0], 1, c.shape[1]))
    return m.predict(c), c

def C2C(m,p,c):
    # reshape input to be [samples, time steps, features]
    c = np.reshape(c, (c.shape[0], 1, c.shape[1]))
    return p, m.predict(c)

def C2PC(m,p,c):
    # reshape input to be [samples, time steps, features]
    c = np.reshape(c, (c.shape[0], 1, c.shape[1]))
    preds = m.predict(c)
    return preds[0:1], preds[2:4]

def PC2P(m,p,c):
    # reshape input to be [samples, time steps, features]
    #this is not right.
    #needs reshaping into the combined feature size after ziping (theory)
    p = np.reshape(p, (p.shape[0], 1, p.shape[1]))
    c = np.reshape(c, (c.shape[0], 1, c.shape[1]))
    return m.predict(zip(p,c)), c

def PC2C(m,p,c):
    # reshape input to be [samples, time steps, features]
    #this is not right.
    #needs reshaping into the combined feature size after ziping (theory)
    p = np.reshape(p, (p.shape[0], 1, p.shape[1]))
    c = np.reshape(c, (c.shape[0], 1, c.shape[1]))
    return p, m.predict(zip(p,c))

def PC2PC(m,p,c):
    # reshape input to be [samples, time steps, features]
    #this is not right.
    #needs reshaping into the combined feature size after ziping (theory)
    p = np.reshape(p, (p.shape[0], 1, p.shape[1]))
    c = np.reshape(c, (c.shape[0], 1, c.shape[1]))
    preds = m.predict(zip(p,c))
    return preds[0:1], preds[2:4]

i2o_func_matrix = [[None, None, None,None, None],
                    [None, P2P, P2C, None, P2PC],
                    [None, C2P, C2C, None, C2PC],
                    [None, None, None,None, None],
                    [None, PC2P, PC2C,None,PC2PC]]

def get_io_based_influence_function(i,o):
    return func_matrix[i][o]