# -*- coding: utf-8 -*-
#
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013  Stephan Adig <sh@sourcecode.de>
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
#


import sys
import os
import os.path

try:
    import yaml
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from exceptions import ConfigurationException
except ImportError, e:
    print e
    sys.exit(1)

SUPPORTED_DISTROS = ["ubuntu", "debian", "centos"]


def read_yaml_file(filename=None, action_type=None):
    if (filename is not None and filename != "" and
            os.path.exists(filename) and
            action_type is not None):
        fp = open(filename, "rb")
        yaml_file = fp.read()
        fp.close()
        config_space = yaml.load(yaml_file)
        if action_type == "mirror":
            if check_mirror_config(config_space, filename):
                return config_space
        if action_type == "nfsroot":
            if check_nfsroot_config(config_space, filename):
                return config_space
    return None


def check_nfsroot_config(config_space=None, filename=None):
    if config_space is None or filename is None:
        return None
    if 'config' not in config_space:
        raise ConfigurationException(
            "Your YAML configuration in '{0}' "
            "doesn't have a default config section".format(filename))
    if 'basefiles_directory' not in config_space["config"]:
        raise ConfigurationException(
            "Your YAML configuration in '{0}' doesn't "
            "have a basefiles directory set".format(filename))
    if 'suites' not in config_space:
        raise ConfigurationException(
            "Your YAML configuration in '{0}' doesn't "
            "have a suites section".format(filename))
    suites = config_space["suites"]
    for suite in suites:
        if 'type' not in suites[suite]:
            raise ConfigurationException(
                "Your YAML configuration in '{0}' has no "
                "type definition in suite '{1}'".format((filename, suite)))
        if suites[suite]["type"] == "debian":
            #
            # Debian Specific Checks
            #
            if 'debootstrap_mirror_url' not in suites[suite]:
                raise ConfigurationException(
                    "Your YAML configuration in '{0}' has no "
                    "debootstrap_mirror_url in suite '{1}'".format(
                        filename, suite))
            if 'arch' not in suites[suite]:
                raise ConfigurationException(
                    "Your YAML configuration in '{0}' has no arch "
                    "setting in suite '{1}'".format(filename, suite))
            if (suites[suite]["arch"] is None or
                    len(suites[suite]["arch"].keys()) > 0):
                if ('amd64' not in suites[suite]["arch"] or
                        'i386' not in suites[suite]["arch"]):
                    raise ConfigurationException(
                        "Your YAML configuration in '{0}' has no arch "
                        "specific settings "
                        "(no i386 or amd64) in suite '{1}'".format(
                            filename, suite))
        if suites[suite]["type"] == "rpm":
            #
            # TODO: RPM Based Distros specific check
            #
            pass
    return True


def check_mirror_config(config_space=None, filename=None):
    if config_space is None or filename is None:
        return None
    if 'config' not in config_space:
        raise ConfigurationException(
            "Your YAML configuration in '{0}' doesn't "
            "have a default config section".format(filename))
    if 'distributions' not in config_space:
        raise ConfigurationException(
            "Your YAML configuration in '{0}' doesn't "
            "have a distributions section".format(filename))
    distributions = config_space["distributions"]
    for key in distributions:
        if key not in SUPPORTED_DISTROS:
            raise ConfigurationException(
                "Your YAML configuration in '{0}' has a non "
                "supported distribution named '{1}'".format(filename, key))
        if 'defaults' not in distributions[key]:
            raise ConfigurationException(
                "Your YAML configuration in '{0}' has no "
                "defaults section in distribution '{1}'".format(filename, key))
        if 'releases' not in distributions[key]:
            raise ConfigurationException(
                "Your YAML configuratoin in '{0}' has no "
                "releases section in distribution '{1}'".format(filename, key))
    return True
