from graphics_module.objects import *
import numpy as np
import pyglet
from pyglet.gl import * #TODO this can all be cleaned up after it's working
from pyglet import gl
from pyglet.window import key
from pyglet.window import mouse
from pyglet import graphics
from pyglet import clock
from pyglet import font
from pyglet import window

class Window(window.Window):
    def __init__(self,window_config=None,fullscreen=False):
        super().__init__(width=window_config['width'], height=window_config['height'],fullscreen=fullscreen, screen = window.get_platform().get_default_display().get_screens()[1])
        self.__config = window_config
        self.clock = clock.get_default()
        self.fps_display = pyglet.window.FPSDisplay(self)
        self.fps_display.label = pyglet.text.Label(font_size=18,
                                                    x= 14,
                                                    y= 35,
                                                    anchor_x='left',
                                                    anchor_y='bottom')
        self._set_fps(window_config['fps'])
        self.fps_display.update()
        self.reset_keys()
        self.mouse_pressed = False
        self.mouse = Point()
        self.label = None
        self.particle_batch = None

    
    def _set_fps(self, fps=60):
        self.clock.set_fps_limit(fps)
        self.fps_display.set_fps(fps)

    def set_line_width(self, width=3.0):
        gl.glLineWidth(width)

    def set_point_size(self,size=1.7):
        gl.glPointSize(size)

    def screen_to(self,zoom_lvl, p):
        return (np.array(p.gl_repr()) - (self.width / 2, self.height / 2)) / zoom_lvl

    def to_screen(self,zoom_lvl, p):
        return p * zoom_lvl + (self.width / 2.0, self.height / 2.0)

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

    def set_particles(self, points,colors):
        self.particles = []
        self.particle_batch = graphics.Batch()

        for i, p in enumerate(points):
            new_p = self.particle_batch.add(1, gl.GL_POINTS, None, ('v2f/stream', p), ('c3B', colors[i]))
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

    def draw_text(self,text):
        self.label.__setattr__('text',text)
        
    def draw_fps(self):
        self.fps_display.set_fps(pyglet.clock.get_fps())
        self.fps_display.draw()

    def update(self):
        if self.has_exit:
            self.close()
            return False

        if self.label: self.label.draw()
        if self.particle_batch: self.particle_batch.draw()
        self.fps_display.update()
        self.draw_fps()
        self.dispatch_events()
        self.dispatch_event('on_draw')
        self.flip()
        return True

class Visuals(object):
    def __init__(self, conf, prog_conf):
        self.graphics_config = conf
        self.program_config = prog_conf #just remove this if I end up don't needing it
        self.key_config = conf.key_bindings
        self.zoom = conf.zoom
        self.noisy = conf.noisy
        self.clear = conf.clear
        self.window = Window(window_config=conf.window,fullscreen=prog_conf.fullscreen)
        text_config = conf.opt['text_overlay']
        if conf.display_text_overlay:
            self.window.label = pyglet.text.Label(font_name=text_config['font'],
                                                    font_size=text_config['font_size'],
                                                    x=text_config['position']['x'],
                                                    y=text_config['position']['y'],
                                                    anchor_x=text_config['position']['x_anchor'],
                                                    anchor_y=text_config['position']['y_anchor'])
        self.window.set_line_width(conf.init_line_width)
        self.window.set_point_size(conf.init_particle_size)
        self.MAX_PARTICLES = prog_conf.max_particles
        self.MAX_ADD_PARTICLES = prog_conf.max_add_particles
        self.POINTS = prog_conf.init_particle_amount
        self.GRAVITY = -100 #TODO learn wtf this is, dunno if it's like a necessary constant or a config
        self.HDIM = 4 # this too
        self.idx = 0# this too
        self.t = 0# this too
        self.tt = 0# this too
        self.inflfl = 2.5
        self.init()
    
    def init(self, influencer=None):
        global points,colors, net, h0, c0
        h0 = np.zeros([self.POINTS, self.HDIM])
        c0 = np.zeros([self.POINTS, self.HDIM])
        points = np.random.randn(self.POINTS, 2) * 2
        colors = np.asarray([(np.random.randint(120, 240),np.random.randint(120, 240),np.random.randint(120, 240)) for x in range(len(points))])
        if influencer is not None: self.influencer = influencer
        #else: self.influencer = lambda : return random through exception here,
        #cuz even "complete random" should be "built"
        self.window.set_particles(points,colors)

    def __handle_input(self): 
        if 1 < 2:
            return False

    def sizer_influencer(self):
        global points
        points = np.random.randn(self.POINTS, 2)
        y_thing = 1.3
        if self.inflfl > 0.2: self.inflfl -= 0.075
        else:
            self.inflfl = 2.75
            y_thing = 0.2
        points[:,0] *= self.inflfl
        points[:,1] *= self.inflfl * y_thing

    def move_around_influencer(self):
        global points
        move = lambda arr: np.asarray([x + (0.06 - np.random.rand() * 0.12) for x in arr])
        points = np.apply_along_axis(move,0,points)
        points = np.apply_along_axis(move,1,points)


    def get_influencer_info(self): #TODO make into a "Influencer interface function call" or program level call?
                                   #that would ask the influencer?
        return 'Untrained LSTM fixed points and attractors. Hidden dimension: {}'.format(self.HDIM)

    def run(self):
        global points, colors
        self.clear_tick = 1
        while True:
            self.window.clock.tick()
            if self.clear: #if I want a "trail" I will need a point history, not clear weirdness, OR an
                           #alpha fill that has "decay rate"
                            #like "if self.trail_clear"
                            #"self.window.trail_clear" which doesn't clear, it
                            #draws a see-through square over the whole screen
                self.window.clear()

            self.__handle_input()
        
            self.move_around_influencer() #this is the magic step TODO a "callable" type hint argument, making this a
                                          #higher order function
            self.window.set_particles(points,colors)
            self.window.update_particles(self.window.to_screen(self.zoom,points))

            if self.graphics_config.display_text_overlay:
                txt = self.get_influencer_info()
                self.window.draw_text(txt)
                
            if self.window.update() == False:
                break
            self.clear_tick += 1
        self.window.close()
        print("visuals shut down.")