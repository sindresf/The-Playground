import numpy as np
from ml_module.Influencer import Influencer

class Random_move(Influencer):
    def __init__(self,conf):
        self.move_max = 0.1 #conf.move_max
        self.move_min = self.move_max / 2.0

    def _move(self, arr):
        rand = np.random.rand(2)
        return np.asarray([x + (self.move_min - rand[r] * self.move_max) for r,x in enumerate(arr)])

    def influence(self, visual_objects):
        return np.apply_along_axis(self._move,1,visual_objects[0]), visual_objects[1]

    def influencer_info(self):
        return "Random points mover"

class Random_move_and_shift(Random_move):
    def __init__(self,conf):
        super().__init__(conf)
        self.color_min = 0 #conf.color_min
        self.color_max = 255 #conf.color_max
        self.color_rand_min = -5 #conf.color_rand_min
        self.color_rand_max = 6 #conf.color_rand_max

    def _color_shift(self,c):
        rands = np.random.randint(self.color_rand_min,self.color_rand_max,3)
        color_yeah = lambda c,r: max(self.color_min, min(self.color_max, c + r))
        r = color_yeah(c[0],rands[0])
        g = color_yeah(c[1],rands[1])
        b = color_yeah(c[2],rands[2])
        return np.asarray((r,g,b))

    def influence(self, visual_objects):
        points, colors = visual_objects
        points = np.apply_along_axis(super()._move,1,points)
        colors = np.apply_along_axis(self._color_shift,1,colors)
        return points,colors
        
    def influencer_info(self):
        return "Random points mover and colour shifter"