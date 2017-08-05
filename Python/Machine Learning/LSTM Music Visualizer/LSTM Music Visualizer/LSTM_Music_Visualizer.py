from LSTM_module import *
from music_module import *
from graphics_module import *
from config_parse.parse import parse_config
#
## PLAN
#
#   this one does as much only "interface calls" to other things
#   to run the visualization over and over.
#
#   personal standardized config file parser
#   gonna have: a random LSTM builder (combining all the random variables and
#   actual layers and such)
#       - with parameters for constraining the build (and inpu output)
#   a LSTM
#   a pixel(point) distribution handler
#       - with point color for tracking
#   a graphics module
#       - with interpolation and not
#       - try to construct as much of it in a generic way so I can use the
#         module all over
#   o-oh
#   need a music (midi?) file interptreter module
#       - with parameterized frequency (or whatever) variable stuff
#   combiner for the "random training" of the LSTM and the noise of the
#   predicts with the music analyzer
#
#   try to get into proper testing?  probably should, meh though
##

#
#  minimal not-even-viable product
#
#  parses config
#  can make b&w
#  and just random walks them
#

#
#  minimal viable product
#
#  parses config
#  can make b&w and colored pixel arrays and interpolate lines based on
#  movement
#  asks simple network for next position
#  loads a music file and just does SOMETHING with it
#

#
#  AWESOME PRODUCT
#
#  parses config like a beautiful all-encompassing baoz
#  can make any type of pixels, including size and interpolate lines based on
#  movement
#  ask whatever kind of network (LSTM OR OTHER D:!) for any kind of output
#  can shift-train the network like a motherFokker
#  loads a song and (probably easiest to do it through config) matches it to
#  beat (64th note tempo for base movement maybe?)
#  analyses song in some ways, simple is ok even for AWESOME, like just having
#  frequency buckets
#  and look for spikes and shift whatever based on whatever
#  and saves it as a movie (sound not included, more like a gif)
#  in high quality, and good framerate (youtube awesomeness standard)
#
if _name_ == "__main__": #TODO take in config file as command arg
    config_file = 'C:\\Users\\sindr\\Source\\Repos\\The-Playground\\Python\\Machine Learning\\LSTM Music Visualizer\\LSTM Music Visualizer\\config.json'
    config, graphics_config, LSTM_config, music_config = parse_config(config_file)

    #TODO now that the configs are "ready" the inits will be like:
    #program = All_This(config)
    # graphics = Graphics(graphics_config)
    # lstm = LSTM(lstm_config)
    # music = Music(music_config)
    #and let it all cascade from there

    #so even for MneVP this goes:
    #load config(path) <- should be command line argument, and the only argument, even "show progress" should be in the config
    #parse config (don't know if this is needed with yaml/json as much?
    #(pretend to) load(music_file)
    #(pretend to) make config.amount of networks that live for song/amount time, (with provisions for "dying vizuals")
    #init graphics
    #make init pixels
    #(pretend to) make pixels move based on network
    #(pretend to) influence network/pixel behaviour on music analysis