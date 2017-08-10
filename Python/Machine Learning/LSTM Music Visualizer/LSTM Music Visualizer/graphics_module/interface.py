from graphics_module.visuals import *
class IVisuals(object):
    def __init__(self,influencer_function, descriptor, conf, prog_conf):
        self.influencer_function = influencer_function
        self.influencer_descriptor = descriptor
        self.visuals = Visuals(conf,prog_conf)

    def build(self):
        self.visuals.build()

    def run(self):
        self.visuals.run(self.influencer_function, self.influencer_descriptor)