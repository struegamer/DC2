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

import subprocess

SUPPORTED_DISTROS = ["ubuntu", "debian", "centos"]


def do_mirror(config=None, dist_type=None):
    if config is None:
        return None
    if 'distributions' in config and config["distributions"] is not None:
        distributions = config["distributions"]
        if dist_type is not None:
            if dist_type == "all":
                for distro in SUPPORTED_DISTROS:
                    if distro in distributions:
                        do_mirror_job(
                            config["config"], distributions[distro], distro)
            else:
                do_mirror_job(
                    config["config"], distributions[dist_type], dist_type)


def do_mirror_job(default_config=None, distributions=None, distro_type=None):
    if default_config is None or distributions is None and distro_type is None:
        return None
    if distro_type in ["ubuntu", "debian"]:
        do_debian_mirror_job(default_config, distributions, distro_type)
    if distro_type in ["centos"]:
        do_rsync_mirror_job(default_config, distributions, distro_type)


def do_rsync_mirror_job(
    default_config=None,
    distributions=None,
        distro_type=None):
    if default_config is None or distributions is None and distro_type is None:
        return None
    if 'releases' in distributions and distributions["releases"] is not None:
        for key in distributions["releases"]:
            call_args = []
            call_args.append("/usr/bin/rsync")
            call_args.append("--progress")
            call_args.append("--verbose")
            call_args.append("-azH")
            call_args.append("--delete")
            release = distributions["releases"][key]
            if 'with_source' in release and release["with_source"] is False:
                call_args.append("--exclude 'SRPMS*'")
            if 'host' in release and release["host"] is not None:
                pass
    return None


def do_debian_mirror_job(
    default_config=None,
    distributions=None,
        distro_type=None):
    if default_config is None or distributions is None and distro_type is None:
        return None
    if 'releases' in distributions and distributions["releases"] is not None:
        for key in distributions["releases"]:
            call_args = []
            call_args.append("/usr/bin/debmirror")
            call_args.append("--progress")
            call_args.append("--verbose")
            call_args.append("--nosource")
            release = distributions["releases"][key]
            if 'sections' in release and release["sections"] is not None:
                call_args.append("--section=%s" % release["sections"])
            else:
                call_args.append("--section=%s" %
                                 distributions["defaults"]["sections"])
            if 'arch' in release and release["arch"] is not None:
                call_args.append("--arch=%s" % release["arch"])
            else:
                call_args.append("--arch=%s" %
                                 distributions["defaults"]["arch"])
            if 'host' in release and release["host"] is not None:
                call_args.append("--host=%s" % release["host"])
            else:
                call_args.append("--host=%s" %
                                 distributions["defaults"]["host"])
            if 'method' in release and release["method"] is not None:
                call_args.append("--method=%s" % release["method"])
            else:
                call_args.append("--method=%s" %
                                 distributions["defaults"]["method"])

            if 'rootdir' in release and release["rootdir"] is not None:
                call_args.append("--root=%s" % release["rootdir"])
            else:
                call_args.append("--root=%s" %
                                 distributions["defaults"]["rootdir"])

            if 'stable' in release and release["stable"] is not None:
                if release["stable"] is True:
                    if distro_type == "ubuntu":
                        call_args.append(
                            "--dist={0},{0}-security,{0}-updates".format(key))
                    if distro_type == "debian":
                        call_args.append("--dist={0},{0}-updates".format(key))
                else:
                    call_args.append("--dist={0}".format(key))
            else:
                if distributions["defaults"]["stable"] is True:
                    if distro_type == "ubuntu":
                        call_args.append(
                            "--dist={0},{0}-security,{0}-updates".format(key))
                    if distro_type == "debian":
                        call_args.append("--dist={0},{0}-updates".format(key))
                else:
                    call_args.append("--dist={0}".format(key))

            if ('mirror_directory' in release and
                    release["mirror_directory"] is not None):
                call_args.append(release["mirror_directory"])
            elif ('mirror_directory' in distributions["defaults"] and
                    distributions["defaults"]["mirror_directory"] is not None):
                call_args.append(distributions["defaults"]["mirror_directory"])
            else:
                call_args.append(default_config["mirror_directory"])
            subprocess.call(call_args)
