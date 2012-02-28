# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#################################################################################


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

SUPPORTED_DISTROS=["ubuntu","debian","centos"]

def read_yaml_file(filename=None,action_type=None):
    if filename is not None and filename != "" and os.path.exists(filename) and action_type is not None:
        fp=open(filename,"rb")
        yaml_file=fp.read()
        fp.close()
        config_space=yaml.load(yaml_file)
        if action_type=="mirror":
            if check_mirror_config(config_space,filename):
                return config_space
        if action_type=="nfsroot":
            if check_nfsroot_config(config_space,filename):
                return config_space
    return None

def check_nfsroot_config(config_space=None,filename=None):
    if config_space is None or filename is None:
        return None
    if not config_space.has_key("config"):
        raise ConfigurationException("Your YAML configuration in '%s' doesn't have a default config section" % filename)
    if not config_space["config"].has_key("basefiles_directory"):
        raise ConfigurationException("Your YAML configuration in '%s' doesn't have a basefiles directory set" % filename)
    if not config_space.has_key("suites"):
        raise ConfigurationException("Your YAML configuration in '%s' doesn't have a suites section" % filename)
    suites=config_space["suites"]
    for suite in suites:
        if not suites[suite].has_key("type"):
            raise ConfigurationException("Your YAML configuration in '%s' has no type definition in suite '%s'" % (filename,suite))
        if suites[suite]["type"]=="debian":
            #
            # Debian Specific Checks
            #
            if not suites[suite].has_key("debootstrap_mirror_url"):
                raise ConfigurationException("Your YAML configuration in '%s' has no debootstrap_mirror_url in suite '%s'" % (filename,suite))
            if not suites[suite].has_key("arch"):
                raise ConfigurationException("Your YAML configuration in '%s' has no arch setting in suite '%s'" % (filename,suite))
            if suites[suite]["arch"] is None or len(suites[suite]["arch"].keys())>0:
                if not suites[suite]["arch"].has_key("amd64") or not suites[suite]["arch"].has_key("i386"):
                    raise ConfigurationException("Your YAML configuration in '%s' has no arch specific settings (no i386 or amd64) in suite '%s'" % (filename,suite))
        if suites[suite]["type"]=="rpm":
            #
            # RPM Based Distros specific check
            #
            pass
    return True

def check_mirror_config(config_space=None,filename=None):
    if config_space is None or filename is None:
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
