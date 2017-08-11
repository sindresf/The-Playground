import numpy as np
from influence_module.Influencer import Influencer

class Random_move(Influencer):
    def __init__(self,conf):
        self.move_max = 0.1 #conf.move_max
        self.move_min = self.move_max / 2.0
        self.move_pool_size = 19467 #cool
        self.move_rand = np.random.rand(self.move_pool_size,2)
        self.move_rand_index = 0

    def _move(self, arr):
        rand = self.move_rand[self.move_rand_index]
        self.move_rand_index = (self.move_rand_index + 1) % self.move_pool_size
        return [x + (self.move_min - rand[r] * self.move_max) for r,x in enumerate(arr)]

    def influence(self, visual_objects):
        return np.apply_along_axis(self._move,1,visual_objects[0]), visual_objects[1]

    def influencer_info(self):
        return "Random points mover."

class Random_move_and_shift(Random_move):
    def __init__(self,conf):
        super().__init__(conf)
        self.color_min = 0 #conf.color_min
        self.color_max = 255 #conf.color_max
        self.color_rand_max = 7 #conf.color_rand_max
        self.color_rand_min = 1 - self.color_rand_max
        self.shift_pool_size = 19467 #cool
        self.shift_c = np.random.rand(self.shift_pool_size)
        self.shift_rands = np.random.randint(self.color_rand_min,self.color_rand_max,(self.shift_pool_size,3))
        self.shift_index = 0
        self.color_yeah = lambda c,r: max(self.color_min, min(self.color_max, c + r))

    def _color_shift(self,c):
        this_shift = self.shift_rands[self.shift_index]
        shift_c = self.shift_c[self.shift_index]
        self.shift_index = (self.shift_index + 1) % self.shift_pool_size
        
        if shift_c < 0.331:
            r = self.color_yeah(c[0],this_shift[0])
            return (r,c[1],c[2])
        elif shift_c < 0.671:
            g = self.color_yeah(c[1],this_shift[1])
            return (c[0],g,c[2])
        elif shift_c < 1.01:
            b = self.color_yeah(c[2],this_shift[2])
            return (c[0],c[1],b)

    def influence(self, visual_objects):
        points, colors = visual_objects
        points = np.apply_along_axis(super()._move,1,points)
        colors = np.apply_along_axis(self._color_shift,1,colors)
        return points,colors
        
    def influencer_info(self):
        return "Random points mover and colour shifter."