from graphics_module.objects import *
import numpy as np

def make_pixels_array_basic(amount):
    return np.full(10,Pixel(), dtype=np.object)

def make_pixels_array_config_based(config):
    if config.colorscheme == "b&w":
        c = Color()
    elif config.colorscheme == "light":
        c = Color(r=245,g=235,b=234,a=0.85) #"light" or whatever to be slightly colorized dots
    if config.aplha == True:
        lol = 4 #random influenced aplha
    #and so on


def get_color(config):
    if not config:#has attribute "lower_limit": I don't know
        lower_limit = 230
