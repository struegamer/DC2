#!/usr/bin/python
# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010  Stephan Hermann <sh@sourcecode.de>
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

from distutils.core import setup
from distutils.file_util import copy_file
from distutils.command.install_scripts import install_scripts

setup(name="dc2.distrotools",
      version="0.1",
      description="DC² Distrotools",
      author="Stephan Adig",
      author_email="sh@sourcecode.de",
      url="http://launchpad.net/dc2",
      packages=['dc2','dc2.distrotools','dc2.distrotools.config','dc2.distrotools.actions'],
      scripts=['scripts/dc2-mirror']
)

setup(name="dc2.client",
        version="0.1",
        description="DC² Client",
        author="Stephan Adig",
        author_email="sh@sourcecode.de",
        url="http://launchpad.net/dc2",
        packages=[
            'dc2',
            'dc2.client',
            'dc2.client.api',
            'dc2.client.api.dc2.inventory',
            'dc2.client.api.dc2',
            'dc2.client.api.dc2.objects',
            'dc2.client.api.dc2.objects.interfaces',
            'dc2.client.api.cs2',
            'dc2.client.api.cs2.objects'],
        scripts=[
            'scripts/dc2-client',
            'scripts/dc2-ssl-client'
        ]
)

setup(name="dc2.appserver",
        version="0.1",
        description="DC² Application Server",
        author="Stephan Adig",
        author_email="sh@sourcecode.de",
        url="http://launchpad.net/dc2",
        packages=[
            'dc2',
            'dc2.appserver',
            'dc2.appserver.apps',
            'dc2.appserver.mongodb',
            'dc2.appserver.auth',
            'dc2.appserver.auth.rpcmethods',
            'dc2.appserver.globals',
            'dc2.appserver.helpers',
            'dc2.appserver.rpc',
            'dc2.appserver.rpcmethods'
        ],
        scripts=["scripts/dc2-prepare_initial_data"]
)
