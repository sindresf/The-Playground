from config_parse.parse import parse_config
from timeit import default_timer as timer
from pyglet import window
from graphics_module.visuals import *
import numpy as np
config_file = 'C:\\Users\\sindr\\Source\\Repos\\The-Playground\\Python\\Machine Learning\\LSTM Music Visualizer\\LSTM Music Visualizer\\config.json'
start = timer()
configs = parse_config(config_file)
print()
end = timer()
elapsed = round((end - start) * 1000,3)
print("parsing config took: %s ms\n" % elapsed)


#TEST Vizual movement shifting (not "go to this point", but noise influence typ
#thing
v = Visuals(configs.graphics)
v.init()
v.run()

#def screen_to(p):
#    return (np.array(p) - (w.width / 2, w.height / 2)) / zoom

#def to_screen(p):
#    return p * zoom + (w.width / 2, w.height / 2)

#while True:
#    w.clock.tick()
#    if clear:
#        w.clear()
    
#    if w.mouse_pressed:
#        for i in range(10):
#            p = screen_to(w.mouse) + np.random.randn(1, 2) * 0.05
#            points[idx] = p
#            idx += 1
#            if idx >= points.shape[0]:
#                idx = 0
                
#    if w.pressed(window.key.SPACE):
#        noisy = not noisy
        
#    if w.pressed(window.key.C):
#        clear = not clear
                
#    if w.pressed(window.key.R):
#        init()
        
#    if w.pressed(window.key.H):
#        h0 = np.random.randn(POINTS, HDIM)
#        c0 = np.random.randn(POINTS, HDIM)
        
#    if w.pressed(window.key.UP):
#        HDIM *= 2
#        init()
#        w.clear()
        
#    if w.pressed(window.key.DOWN):
#        HDIM /= 2
#        init()
#        w.clear()
        
#    w.reset_keys()
    
#    if noisy:
#        i = np.random.randint(0, points.shape[0] - 10)
#        for j in range(10):
#            points[i + j] = np.random.randn(1, 2)
        
    
#    #points = points.dot(W)
    
#    #points += screen_to(w.mouse)
#    #points = np.tanh(points.dot(W1))
#    #points = np.tanh(points.dot(W2))
#    #points = points.dot(W3)
    
#    #h = np.zeros_like(h0)
#    #c = np.zeros_like(c0)
    
#    #points_mod = np.zeros_like(points)
    
#    #for i in range(points.shape[0]):
#    #    x = np.array([[points[i, 0], points[i, 1]]])
#    #    net.ff([x], h0[i].reshape(1, HDIM), c0[i].reshape(1, HDIM))
#    #    points_mod[i] = net.outputs[0].h
#    #    h[i], c[i] = net.units[0].h.copy(), net.units[0].c.copy()
    
#    #h0 = h.copy()
#    #c0 = c.copy()
    
#    #w.update_particles(to_screen(points_mod))
    
#    #w.draw_text('Untrained LSTM fixed points and attractors.  Hidden
#    #dimension: {}'.format(HDIM), size=12, p=(10, 10))
    
#    t += 1
    
#    """
#    if t > 60:
#        init()
#        t = 0
        
#        tt += 1
#        if tt > 9:
#            tt = 0
#            HDIM *= 2.0
#            init()
#    """
#    if w.update() == False:
#        break
    
#w.close()
#print("done")


#DEV parser for vizuals
#TEST config parsing for vizuals
#TEST Vizual color shifting

#DEV parser for LSTM
#TEST config parsing for LSTM

#DEV pixels builder
#TEST different pixels based on config initialization (random builder type)

#DEV parser for music_module
##TEST config parsing for music_module

#DEV parser for overall use (LSTM_Music_Visualizer)
##TEST config parsing for overall use (LSTM_Music_Visualizer)