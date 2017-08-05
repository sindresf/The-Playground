from config_parse.parse import parse_config
from timeit import default_timer as timer
config_file = 'C:\\Users\\sindr\\Source\\Repos\\The-Playground\\Python\\Machine Learning\\LSTM Music Visualizer\\LSTM Music Visualizer\\config.json'
start = timer()
config, graphics_config, LSTM_config, music_config = parse_config(config_file)
print()
end = timer()
elapsed = round((end - start) * 1000,3)
print("parsing config took: %s ms\n" % elapsed)

#DEV parser for vizuals
#TEST config parsing for vizuals
#TEST Vizual color shifting
#TEST Vizual movement shifting (not "go to this point", but noise influence typ
#thing

#DEV parser for LSTM
#TEST config parsing for LSTM

#DEV pixels builder
#TEST different pixels based on config initialization (random builder type)

#DEV parser for music_module
##TEST config parsing for music_module

#DEV parser for overall use (LSTM_Music_Visualizer)
##TEST config parsing for overall use (LSTM_Music_Visualizer)