import sys
import os
import os.path

try:
    import yaml
except ImportError,e:
    print e
    sys.exit(1)

try:
    from exceptions import ConfigurationException
except ImportError,e:
    print e
    sys.exit(1)

SUPPORTED_DISTROS=["ubuntu","debian"]

def read_yaml_file(filename=None,action_type=None):
    if filename is not None and filename != "" and os.path.exists(filename) and action_type is not None:
        fp=open(filename,"rb")
        yaml_file=fp.read()
        fp.close()
        config_space=yaml.load(yaml_file)
        if check_config(config_space,filename,action_type) is True:
            return config_space
    return None

def check_config(config_space=None,filename=None,check_type=None):
    if config_space is None or filename is None or check_type is None:
        return None
    if not config_space.has_key("config"):
        raise ConfigurationException("Your YAML configuration in '%s' doesn't have a default config section" % filename)
    if not config_space.has_key("distributions"):
        raise ConfigurationException("Your YAML configuration in '%s' doesn't have a distributions section" % filename)
    distributions=config_space["distributions"]
    for key in distributions:
        if key not in SUPPORTED_DISTROS:
            raise ConfigurationException("Your YAML configuration in '%s' has a non supported distribution named '%s'" % (filename,key))
        if not distributions[key].has_key("defaults"):
            raise ConfigurationException("Your YAML configuration in '%s' has no defaults section in distribution '%s'" % (filename,key))
        if not distributions[key].has_key("releases"):
            raise ConfigurationException("Your YAML configuratoin in '%s' has no releases section in distribution '%s'" % (filename,key))
    return True
