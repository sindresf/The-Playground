class Config_struct(object):
    def __init__(self, struct_name="Base Config Structure"):
        self.name = struct_name
        self.opt = {}

    def register_config_setting(self, setting, configuration):
        setattr(self, setting, configuration)

    def register_opt_config_settings(self, opts):
        for setting,configuration in opts.items():
            self.opt[setting] = configuration

    def __str__(self):
        #TODO "stringbuilder" indent tree of attributes and values
        #print outside of debugging here would be a command line --help
        #or "H" pressed for help
        #type of thing
        return self.name

class Configs(object):
    def __init__(self):
        self.name = "config module holder"

    def add_config_module(self, config_struct):
        setattr(self, config_struct.name, config_struct)

    def __str__(self):
        #TODO calles each "getattrib" string representation
        return self.name