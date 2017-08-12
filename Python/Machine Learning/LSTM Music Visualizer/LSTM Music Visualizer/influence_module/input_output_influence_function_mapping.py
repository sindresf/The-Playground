# The 9 mappings from input to output based on point(x,y) and color(r,g,b)
import numpy as np
def P2P(m,p,c):
    print("p: " + str(p))
    #p = np.reshape(p,newshape=(2,0))
    #p = (None, p , 0)
    #print("np: " + str(p))
    print()
    return m.predict(p), c

def P2C(m,p,c):
    return p, m.predict(p)

def P2PC(m,p,c):
    preds = m.predict(p)
    return preds[0:1], preds[2:4]

def C2P(m,p,c):
    return m.predict(c), c

def C2C(m,p,c):
    return p, m.predict(c)

def C2PC(m,p,c):
    preds = m.predict(c)
    return preds[0:1], preds[2:4]

def PC2P(m,p,c):
    return m.predict(zip(p,c)), c

def PC2C(m,p,c):
    return p, m.predict(zip(p,c))

def PC2PC(m,p,c):
    preds = m.predict(zip(p,c))
    return preds[0:1], preds[2:4]

i2o_func_matrix = [[None, None, None,None, None],
               [None,P2P,P2C,None,P2PC],
               [None,C2P,C2C,None,C2PC],
               [None, None, None,None, None],
               [None,PC2P,PC2C,None,PC2PC]]

def get_io_based_influence_function(i,o):
    return func_matrix[i][o]