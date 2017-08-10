from ml_module.interface import IInfluencer
from music_module.interface import IMusic
from graphics_module.interface import IVisuals
from parse_module.interface import parse_config
from timeit import default_timer as timer
import numpy as np

configs = None
i_visuals = None
i_influencer = None
i_music = None

def print_time_since(start, what_txt):
    end = timer()
    elapsed = round((end - start) * 1000,3)
    print("%s took: %s ms\n" % (what_txt,elapsed))

def parse(*arg):
    global configs
    start = timer()
    configs = parse_config(arg[0]) #this needs to handle plural and directory
    np.random.seed(configs.program.random_seed)
    print_time_since(start,"parsing")

def build(): #build everything
    global configs, i_influencer, i_visuals,i_music
    start = timer()
    i_influencer = IInfluencer(configs.influencer)
    i_influencer.build()
    i_visuals = IVisuals(i_influencer.influence_visual_object, i_influencer.influencer_description, configs.graphics,configs.program)
    i_visuals.build()
    i_music = IMusic(configs.music)
    i_music.build()
    print_time_since(start,"modules build")

def run(): #run the whole thing
    print("running program")
    i_visuals.run()


if __name__ == "__main__": #TODO take in config file as command arg
    program_start = timer()
    config_file = 'C:\\Users\\sindr\\Source\\Repos\\The-Playground\\Python\\Machine Learning\\LSTM Music Visualizer\\LSTM Music Visualizer\\config.json'
    parse(config_file)
    build()

    run()
    print_time_since(start,"program run")