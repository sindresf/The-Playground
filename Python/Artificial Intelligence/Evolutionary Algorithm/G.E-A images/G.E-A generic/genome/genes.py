#genes of simple types are just the types
#don't make genes that aren't bigger structs
#Example:
class CircleGene(object):
    def __init__(self, config): #config sets the init through random ranges
        self.x = 0
        self.y = 0
        self.radius = 1.0
        self.color = (0,0,0)
        self.alpha = 1.0

class BaseGeometricGene(object):
    def __init__(self): #config sets the init through random ranges
        self.x = 0
        self.y = 0

    def init(self,x,y):
        self.x = x
        self.y = y

    def save_representation(self): #stuff like this, IF not pickle works
        return x + "," + y

    def load_representation(self,rep):
        self.x = float(rep[0])
        self.y = float(rep[1])