from parse_module.interface import parse_config


#this is what is run through the command line
#command line argument
config_file = 'C:\\Users\\sindr\\Source\\Repos\\The-Playground\\Python\\Artificial Intelligence\\Evolutionary Algorithm\\G.E-A images\\G.E-A generic\\configs\\program_config.json'

def run(config_file_path): #type hint this
    parse_config(config_file_path)


if __name__ == "__main__":
    run(config_file) #make this come from the command line