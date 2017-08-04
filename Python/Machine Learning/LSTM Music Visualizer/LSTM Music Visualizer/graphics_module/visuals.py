from graphics_module.objects import Pixel
from graphics_module.objects import Point
import numpy as np
import pyglet
from pyglet.gl import *
from pyglet import gl
from pyglet.window import key
from pyglet.window import mouse
from pyglet import graphics
from pyglet import clock
from pyglet import font
from pyglet import window

class Window(window.Window): #TODO connect any variables to config or Pixel config, as well as Point and
                                    #Color and Pixel classes
    def __init__(self, *args, **Kwargs):
        super(Window, self).__init__(*args,**Kwargs)
        self.clock = clock.get_default()
        self.reset_keys()
        self.mouse_pressed = False
        self.mouse = Point()
        self.label = None
        self.set_line_width()
        self.set_point_size()
        self.particle_batch = None

    def set_line_width(self, width=3.0):
        gl.glLineWidth(width)

    def set_point_size(self,size=1.0):
        gl.glPointsize(size)

    def reset_keys(self):
        self.pressed_keys = {}

    def pressed(self, key):
        return key in self.pressed_keys

    def on_mouse_pressed(self, x, y, button, modifiers):
        self.mouse_pressed = button and mouse.LEFT

    def on_mouse_released(self, x, y, button, modifiers):
        self.mouse_pressed = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse.x = x
        self.mouse.y = y
        self.dx = dx
        self.dy = dy

    def on_key_press(self, symbol, modifiers):
        self.pressed_keys[symbol] = True

    def on_key_release(self, symbol, modifiers):
        pass

    def set_particles(self, particles):
        self.particles = []
        self.particle_batch = graphics.Batch()

        for p in particles:
            c = np.random.randint(126, 256)
            new_p = self.particle_batch.add(1, gl.GL_POINTS, None, ('v2f/stream', p), ('c38', (c, c, c)))
            self.particles += [new_p]

    def update_particles(self, particles):
        for i, p in enumerate(self.particles):
            v = p.vertices
            v[0] = particles[i][0]
            v[1] = particles[i][1]

    def line_loop(self, vertices):
        out = []
        for i in range(len(vertices) - 1):
            out.extend(vertices[i])
            out.extend(vertices[i + 1])

        out.extend(vertices[len(vertices) - 1])
        out.extend(vertices[0])

        return len(out) // 2, out

    def triangle_fan(self, vertices):
        out = []
        for i in range(1, len(vertices) - 1):
            out.extend(vertices[0])
            out.extend(vertices[i])
            out.extend(vertices[i + 1])
        return len(out) // 2, out

    def draw_poly(self, vertices, color):
        l1_count, l1_vertices = self.line_loop(vertices)
        graphics.draw(l1_count,gl.GL_LINES,
                             ('v2f', l1_vertices),
                             ('c4f', [color[0], color[1], color[2], 1] * (l1_count)))

    def draw_poly_fill(self, vertices, color):
        tf_count, tf_vertices = self.triangle_fan(vertices)
        if tf_count == 0: return
        graphics.draw(tf_count, gl.GL_TRIANGLES,
                             ('v2f', tf_vertices),
                             ('c4f', [0.5 * color[0], 0.5 * color[1], 0.5 * color[2], 0.5] * (tf_count)))

    def __get_rect_vertices(self,x,y,w,h):
        return ((x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y))

    def draw_rect(self,x,y,w,h,color,thickness=1):
        verts = self.__get_rect_vertices(x,y,w,h)
        if thickness > 0: self.draw_poly(verts, color) #only edges
        else: self.draw_poly_fill(verts, color) #filled

    def draw_point(self, point, color=(255,255,255)):
        graphics.draw(1, gl.GL_POINTS,
                             ('v2f', point),
                             ('c3B', color))

    def draw_text(self,text,size=18,p=None):
        p = (10,10) if not p else p
        self.label = pyglet.text.Label(text,font_name='monospace',font_size=size,x=p[0],y=p[1],anchor_x='left',anchor_y='bottom')

    def update(self):
        if self.has_exit:
            self.close()
            return False

        if self.label: self.label.draw()
        if self.particle_batch: self.particle_batch.draw()

        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
        return True

##All this from config and stuff
MAX_PARTICLES = 10000
MAX_ADD_PARTICLES = 100
GRAVITY = -100
w = Window(width=1280, height=720)
w.set_fps(60)

POINTS = 500

HDIM = 4

net = None

def init():
    global points, net, h0, c0
    h0 = np.zeros([POINTS, HDIM])
    c0 = np.zeros([POINTS, HDIM])
    points = np.random.randn(POINTS, 2) * 2
    net = lstm.LSTMNetwork(2, HDIM, 2, 1, None, None)

init()
idx = 0
t = 0
tt = 0
zoom = 80.0
noisy = False
clear = True

def screen_to(p):
    return (np.array(p) - (w.width / 2, w.height / 2)) / zoom

def to_screen(p):
    return p * zoom + (w.width / 2, w.height / 2)


#functions for interacting with vizuzuz
def add_pixels():
    pass

def update_pixels():
    pass

def update_stats(dt):
    pass
