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
import subprocess
import time
import tempfile
import shutil
from threading import Thread

class Debootstrap(Thread):
    def __init__(self,thread_name=None,config=None, which_suite=None):
        self._thread_name=thread_name
        self._config=config
        self._which_suite=which_suite
        Thread.__init__(self,name=self._thread_name)
    def run(self):
        if config is None or which_suite is None:
            return None
        suite=config["suites"][which_suite]
        # 
        # Create temp directory which contains the chroot in step 1
        #
        if os.path.exists("/usr/sbin/debootstrap"):
            for arch in suite["arch"]:
                call_args=[]
                call_args.append("/usr/sbin/debootstrap")
                temppath=tempfile.mkdtemp("dc2-")
                call_args.append("--arch=%s" % arch)
                call_args.append(which_suite)
                call_args.append(temppath)
                call_args.append(suite["debootstrap_mirror_url"])
                subprocess.call(call_args)
                call1_args=[]
                call1_args.append("/bin/tar")
                call1_args.append("-C")
                call1_args.append(temppath)
                call1_args.append("--exclude=*.deb")
                call1_args.append("-cvpzf")
                call1_args.append("%s/%s.tgz" % (config["config"]["basefiles_directory"],suite["arch"][arch]["classname"])
                call1_args.append(".")
                subprocess.call(call1_args)
                shutil.rmtree(temppath)

def do_nfsroot(config=None,which_suite=None):
    if config is None:
        return none
    suites=config["suites"]
    if which_suite == "all":
        for suite in suites:
            if suites[suite]["type"]=="debian":
                do_debian_chroot(config,suite)
    else:
        if suites.has_key(which_suite):
            suite=suites[which_suite]
            if suite["type"]=="debian":
                do_debian_chroot(config,which_suite)


def do_debian_chroot(config=None,which_suite=None):
    if config is None or which_suite is None:
        return None
    suite=config["suites"][which_suite]
    # 
    # Create temp directory which contains the chroot in step 1
    #
    if os.path.exists("/usr/sbin/debootstrap"):
        for arch in suite["arch"]:
            call_args=[]
            call_args.append("/usr/sbin/debootstrap")
            temppath=tempfile.mkdtemp("dc2-")
            call_args.append("--arch=%s" % arch)
            call_args.append(which_suite)
            call_args.append(temppath)
            call_args.append(suite["debootstrap_mirror_url"])
            subprocess.call(call_args)
            call1_args=[]
            call1_args.append("/bin/tar")
            call1_args.append("-C")
            call1_args.append(temppath)
            call1_args.append("--exclude=*.deb")
            call1_args.append("-cvpzf")
            call1_args.append("%s/%s.tgz" % (config["config"]["basefiles_directory"],suite["arch"][arch]["classname"])
            call1_args.append(".")
            subprocess.call(call1_args)
            shutil.rmtree(temppath)
