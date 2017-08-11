from influence_module.Influencer import NetworkInfluencer
#import keras.LSTM
class LSTM_influencer(NetworkInfluencer):
    def __init__(self,conf):
        self.config = conf
        
    def build(self):
        self.build = True

    def shift_train(self):
        self.train = "shift"

    def influence(self, visual_objects):
        return visual_objects #pred.visual_objects

    def influencer_info(self):
        return "LSTM. {info}"