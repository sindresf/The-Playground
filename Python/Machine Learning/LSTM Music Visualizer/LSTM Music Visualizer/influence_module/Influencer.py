class Influencer(object):
    def __init__(self,conf):
        self.config = conf
        
    def build(self):
        self.build = True

    def influence(self, visual_objects):
        return visual_objects

    def influencer_info(self):
        return "Base Influencer, does nothing."

class NetworkInfluencer(Influencer):
    def __init__(self,conf):
        self.config = conf
        
    def build(self):
        self.build = True

    def shift_train(self):
        self.train = "shift"

    def influence(self, visual_objects):
        return visual_objects

    def influencer_info(self):
        return "Base Network Influencer, does nothing."
