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