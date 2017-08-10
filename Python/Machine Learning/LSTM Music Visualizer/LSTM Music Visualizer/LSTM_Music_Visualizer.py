from ml_module import *
from music_module import *
from graphics_module import *
from parse_module.parse import parse_config
from parse_module.config_structs import *
from timeit import default_timer as timer
import numpy as np

configs = None

def parse(*arg):
    global configs
    start = timer()
    configs = parse_config(arg[0]) #this needs to handle plural and directory
    np.random.seed(configs.program.random_seed)
    print()
    end = timer()
    elapsed = round((end - start) * 1000,3)
    print("parsing config took: %s ms\n" % elapsed)

def build(): #build everything
    global configs
    start = timer()
    print("building with configs: %s" % isinstance(configs, Configs))
    end = timer()
    elapsed = round((end - start) * 1000,3)
    print("building took: %s ms\n" % elapsed)

def run(): #run the whole thing
    print("running program")

if __name__ == "__main__": #TODO take in config file as command arg
    program_start = timer()
    config_file = 'C:\\Users\\sindr\\Source\\Repos\\The-Playground\\Python\\Machine Learning\\LSTM Music Visualizer\\LSTM Music Visualizer\\config.json'
    parse(config_file)
    build()
    setup_done = timer()
    elapsed = round((setup_done - program_start) * 1000,3)
    print("setup took: %s ms\n" % elapsed)
    run()
    program_end = timer()
    elapsed = round((program_end - program_start) * 1000,3)
    print("program ran for took: %s ms\n" % elapsed)