class Config_struct(object):
    def __init__(self, struct_name="Base Config Structure"):
        self.name = struct_name

    def register_config_setting(self, setting, configuration):
        setattr(self, setting, configuration)

    def register_opt_config_settings(self, opts):
        self.opt = lambda: None
        for key in opts:
            setattr(self.opt, key, opts[key])

    def __str__(self): #TODO this needs a getattrib run through or something for print
        return '\n\topt:' + str(self.opt) + '\n'