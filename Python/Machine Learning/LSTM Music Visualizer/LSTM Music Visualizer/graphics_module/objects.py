import numpy as np

class Screen(object):
    def __init__(self,height=400,width=400):
        self.height = height
        self.width = width
        self.midPoint = Point(x=int(self.width / 2),y=int(self.height / 2))

    def get_normalized_coords(self, point):
        return [point.x / self.width, point.y / self.height]

    def get_scaled_up_coords(self,point):
        return Point(x=int(point[0] * self.width),y=int(point[1] * self.height))

class Point(object):
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def get_normalized_coords(self,screen):
        return (self.x / screen.width, self.y / screen.height)

    def rand_shift_position(self,screen,x=True,y=True,x_shift_max=16,y_shift_max=16,dist="uniform"):
        if x: self.x = max(0,min(screen.width, self.x + np.random.randint(x_shift_max)))
        if y: self.y = max(0,min(screen.height, self.y + np.random.randint(y_shift_max)))
        
    def gl_repr(self):
        return (self.x,self.y)
    def __repr__(self):
        return self._string_rep()
    def __str__(self):
        return self._string_rep()

    def _string_rep(self):
        return str('x:' + str(self.x) + ',y:' + str(self.y))

    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
class Velocity(object):
    def __init__(self,dx=0.0,dy=0.0):
        self.dx = dx
        self.dy = dy

    def set_max_velocity(self,dx_max=2.0,dy_max=2.0):
        self.dx_max = dx_max
        self.dy_max = dy_max

    def get_normalized_velocity(self,screen):
        return (self.dx / screen.dx_max, self.dy / screen.dy_max)

    def rand_shift_velocity(self,screen,dx=True,dy=True,dx_shift_max=2.0,dy_shift_max=2.0,dist="uniform"):
        if dx: self.dx = max(0.0,min(screen.width, self.dx + np.random.rand(dx_shift_max)))
        if dy: self.dy = max(0.0,min(screen.height, self.dy + np.random.rand(dy_shift_max)))
        
    def gl_repr(self):
        return (self.dx,self.dy)
    def __repr__(self):
        return self._string_rep()
    def __str__(self):
        return self._string_rep()

    def _string_rep(self):
        return str('dx:' + str(round(self.dx,2)) + ',dy:' + str(round(self.dy,2)))

    def __eq__(self, other):
        if not isinstance(other, Velocity):
            return False
        return self.dx == other.dx and self.dy == other.dy

    def __hash__(self):
        return hash((self.dx, self.dy))

class Color(object):
    def __init__(self, r=255,g=255,b=255,a=1.0):
        self.r = r
        self.g = g
        self.b = b
        self.alpha = a
        self.min_intensity = 0
        self.max_intensity = 255
        self.min_alpha = 0.0
        self.max_alpha = 1.0

    def set_color_intensity_interval(self,min=0,max=255):
        self.min_intensity = min
        self.max_intencity = max

    def set_alpha_interval(self,min=0.0,max=1.0):
        self.min_alpha = min
        self.max_alpha = max

    def get_normalised_color(self):
        return (self.r / self.__max_intensity, self.g / self.__max_intensity, self.b / self.__max_intensity)

    def shift_color(self,rgb=[True,True,True],alpha=True,rgb_max_shift_amount=128,aplha_max_shift_amount=1.0,dist="uniform"):
        for color in [self.r,self.g,self.b][rgb]:
            color = max(self.min_intensity,min(self.max_intencity,color + np.random.randint(-rgb_max_amount,rgb_max_amount)))
        if alpha: self.alpha = max(self.min_alpha,min(self.max_alpha,color + np.random.randint(-rgb_max_amount,rgb_max_amount)))

    def scale_up_normalised_color(self,r=None,g=None,b=None):
        self.r = int(r * self.__max_intensity) if r is not None else self.r
        self.g = int(g * self.__max_intensity) if g is not None else self.g
        self.b = int(b * self.__max_intensity) if b is not None else self.b
        
    def gl_repr(self):
        return (self.r,self.g,self.b)
    def __repr__(self):
        return self._string_rep()
    def __str__(self):
        return self._string_rep()

    def _string_rep(self):
        return 'rgba: ({:d},{:d},{:d},{:f})'.format(self.r,self.g,self.b,round(self.alpha,3))

    def __eq__(self, other):
        if not isinstance(other, Color):
            return False
        return self.r == other.r and self.g == other.g and self.b == other.b and round(self.alpha,2) == round(self.alpha,2)

    def __hash__(self):
        return hash((self.r, self.g,self.b,self.alpha))

class Pixel(object):
    def __init__(self,point=Point(),color=Color(),velocity=None):
        self.point = point
        self.color = color
        self.velocity = velocity

    def rand_shift_position(self,screen,x=True,y=True,x_shift_max=16,y_shift_max=16,dist="uniform"):
        self.point.rand_shift_position(screen,x,y,x_shift_max,y_shift_max,dist)

    def rand_shift_velocity(self,screen,dx=True,dy=True,dx_shift_max=2.0,dy_shift_max=2.0,dist="uniform"):
        self.velocity.rand_shift_velocity(screen,dx,dy,dx_shift_max,dy_shift_max,dist)

    def shift_color(self,rgb=[True,True,True],alpha=True,rgb_max_shift_amount=128,aplha_max_shift_amount=1.0,dist="uniform"):
        self.color.shift_color(rgb,alpha,rgb_max_shift_amount,aplha_max_shift_amount,dist)

    def to_features(self,screen,point=True,color=[True,True,True,True],velocity=False):
        features = np.array(dtype=np.float)
        if point: features.append(self.point.get_normalized_coords(screen))
        norm_colors = self.color.get_normalised_color()[color[:len(color) - 1]]
        if len(norm_colors) > 0: features.append(norm_colors)
        if color[3]: features.append(self.color.alpha)
        if velocity: features.append(self.velocity.get_normalized_velocity(screen))
        return features
    
    def gl_reps(self):
        if self.velocity is None: return self.point.gl_repr(), self.color.gl_repr(), self.color.alpha
        else: return self.point.gl_repr(), self.color.gl_repr(), self.color.alpha, self.velocity.gl_repr()

    def __repr__(self):
        return self._string_rep()
    def __str__(self):
        return self._string_rep()

    def _string_rep(self):
        return str(self.point) + " | " + str(self.color)

    def __eq__(self, other):
        if not isinstance(other, Pixel):
            return False
        return self.point == other.point and self.color == other.color

    def __hash__(self):
        return hash(self.point,self.color)