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


def do_nfsroot(config=None):
    if config is None:
        return none
    suites=config["suites"]
    for suite in suites:
        if suites[suite]["type"]=="debian":
            do_debian_chroot(config,suite=suite)


def do_debian_chroot(config=None,which_suite=None):
    if config is None or which_suite is None:
        return None
    suite=config["suites"][which_suite]
    # 
    # Create temp directory which contains the chroot in step 1
    #
    pass
