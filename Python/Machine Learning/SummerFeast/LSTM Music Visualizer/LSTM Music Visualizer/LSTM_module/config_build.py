#import lstm keras stuff
from LSTM_module.LSTM import ILSTM
def build_network(config):
    #this should be the only public method, as EVERYTHING should come from the
    #config
    #for layers in config.layers, within random boundaries if any:
        #add layer to model with config.activations and config.weights, and
        #config.count and so on
    return ILSTM(network=lstm_build)