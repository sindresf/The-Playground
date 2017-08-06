import json
from config_parse.config_structs import *

def parse_config(file=None, files=None):
    if file is not None: return __parse_config_file(file)
    if files is not None: return __parse_config_files(files)

def __parse_config_file(file):
    js_config = None
    configs = Configs()
    with open(file) as json_data:
        js_config = json.load(json_data)
    for config_module_name in js_config:
        conf_struct = Config_struct(config_module_name)
        __register_settings_to(conf_struct,js_config[config_module_name])
        configs.add_config_module(conf_struct)
    return configs

def __parse_config_files(files):
    js_config = None
    configs = Configs()
    js_configs = []
    with open(file) as json_data:
        js_configs.append(json.load(json_data))
    for js_config in js_configs:
        for config_module_name in js_config:
            conf_struct = Config_struct(config_module_name)
            __register_settings_to(conf_struct,js_config[config_module_name])
            configs.add_config_module(conf_struct)
    return configs


def __register_settings_to(struct, settings):
    for setting in settings:
        if setting == 'opt': struct.register_opt_config_settings(settings[setting])
        else:
            if(type(setting) is type({})):
                for s in setting:
                    __register_settings_to(struct,s)
            struct.register_config_setting(setting,settings[setting])