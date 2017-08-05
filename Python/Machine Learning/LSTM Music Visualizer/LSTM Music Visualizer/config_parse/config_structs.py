class Config_struct(object):
    def __init__(self, struct_name="Base Config Structure"):
        self.name = struct_name

    def register_config_setting(self, setting, configuration):
        setattr(self, setting, configuration)

    def register_opt_config_settings(self, opts):
        self.opt = lambda: None
        for key in opts:
            setattr(self.opt, key, opts[key])

    def __str__(self):
        return '\n\topt:' + str(self.opt) + '\n'

class Config(Config_struct):
    def __init__(self):
        super().__init__("config")

    def __str__(self):
        return "going through attribs for print to come at a later date"
        #return self._string_rep()

    def _string_rep(self):
        return 'mustav:' + str(self.mustav) + ", " + super().__str__()
        
class Graphics_config(Config_struct):
    def __init__(self):
        super().__init__("graphics")

    def __str__(self):
        return "going through attribs for print to come at a later date"
        #return self._string_rep()

    def _string_rep(self):
        return 'mustav:' + str(self.mustav) + ", " + super().__str__()

class LSTM_config(Config_struct):
    def __init__(self):
        super().__init__("lstm")

    def __str__(self):
        return "going through attribs for print to come at a later date"
        #return self._string_rep()
    
    def _string_rep(self):
        return 'mustav:' + str(self.mustav) + ", " + super().__str__()
        
class Music_config(Config_struct):
    def __init__(self):
        super().__init__("music")

    def __str__(self):
        return "going through attribs for print to come at a later date"
        #return self._string_rep()

    def _string_rep(self):
        return 'mustav:' + str(self.mustav) + ", " + super().__str__()