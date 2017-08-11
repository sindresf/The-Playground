import numpy as np
from influence_module.random_walkers import Random_move_and_shift
from influence_module.random_walkers import Random_move
from influence_module.Influencer import *
from influence_module.LSTM_influencer import *
    
class IInfluencer(object):
    def __init__(self, conf):
        self.__config = conf
        print("influencer config:")
        print(conf)
        print(self.__config.name)

    def build(self):
        if(self.__config.name == "random_influencer"):
            if self.__config.type == "random_move_and_shift":
                self.__influencer = Random_move_and_shift(self.__config)
            elif self.__config.type == "random_move":
                self.__influencer = Random_move(self.__config)
            else:
                self.__influencer = Influencer(self.__config)

        if(self.__config.name == "network_influencer"):
            if self.__config.type == "lstm":
                self.__influencer = LSTM_influencer(self.__config)
            else:
                self.__influencer = NetworkInfluencer(self.__config)
        self.__influencer.build()

    def influence_visual_object(self, vis_objs):
        return self.__influencer.influence(vis_objs)

    def influencer_description(self):
        return self.__influencer.influencer_info()