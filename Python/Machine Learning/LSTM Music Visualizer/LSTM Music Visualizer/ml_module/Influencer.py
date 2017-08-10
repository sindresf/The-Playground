class Influencer(object):
    def __init__(self,conf):
        self.config = conf
        
    def build(self):
        self.build = True

    def influence(self, visual_objects):
        return visual_objects

    def influencer_info(self):
        return "Base Influencer, does nothing."