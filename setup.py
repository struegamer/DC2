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
import setuptools
from distutils.core import setup
from distutils.file_util import copy_file
from distutils.command.install_scripts import install_scripts

setup(name='dc2',
        version='0.9',
        description='DC² Namespace Package',
        author='Stephan Adig',
        author_email='sh@sourcecode.de',
        url='http://launchpad.net/dc2',
        packages=['dc2']
)

setup(name="dc2.distrotools",
      version="0.9'",
      description="DC² Distrotools",
      author="Stephan Adig",
      author_email="sh@sourcecode.de",
      url="http://launchpad.net/dc2",
      packages=['dc2.distrotools','dc2.distrotools.config','dc2.distrotools.actions'],
      namespace_packages=['dc2'],
      scripts=[
          'scripts/dc2-mirror',
          'scripts/dc2-create-chroot'
          ]
)

setup(name="dc2.client",
        version="0.9'",
        description="DC² Client",
        author="Stephan Adig",
        author_email="sh@sourcecode.de",
        url="http://launchpad.net/dc2",
        namespace_packages=['dc2'],
        packages=[
            'dc2.client',
            'dc2.client.api',
            'dc2.client.api.dc2.inventory',
            'dc2.client.api.dc2',
            'dc2.client.api.helpers',
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
        version="0.9'",
        description="DC² Application Server",
        author="Stephan Adig",
        author_email="sh@sourcecode.de",
        url="http://launchpad.net/dc2",
        namespace_packages=['dc2'],
        packages=[
            'dc2.appserver',
            'dc2.appserver.apps',
            'dc2.appserver.auth',
            'dc2.appserver.auth.rpcmethods',
            'dc2.appserver.globals',
            'dc2.appserver.helpers',
            'dc2.appserver.rpc',
            'dc2.appserver.rpcmethods',
        ],
        scripts=["scripts/dc2-prepare_initial_data"]
)

setup(name='dc2.lib',
        version='0.9',
        description='DC2 General Library',
        author='Stephan Adig',
        author_email='sh@sourcecode.de',
        url='http://launchpad.net/dc2',
        namespace_packages=['dc2'],
        packages=[
            'dc2.lib',
            'dc2.lib.auth',
            'dc2.lib.auth.helpers',
            'dc2.lib.auth.kerberos',
            'dc2.lib.auth.kerberos.xmlrpc',
            'dc2.lib.auth.kerberos.authentication',
            'dc2.lib.db',
            'dc2.lib.db.mongo',
            'dc2.lib.web',
            'dc2.lib.web.pages',
            'dc2.lib.web.csrf',
        ]
    )

setup(name='dc2.admincenter',
        version='0.9',
        description='DC2 AdminCenter',
        author='Stephan Adig',
        author_email='sh@sourcecode.de',
        url='http://launchpad.net/dc2/',
        namespace_packages=['dc2'],
        packages=[
            'dc2.admincenter',
            'dc2.admincenter.apps',
            'dc2.admincenter.apps.admin',
            'dc2.admincenter.apps.admin.dc2backends',
            'dc2.admincenter.globals',
            'dc2.admincenter.lib',
            'dc2.admincenter.lib.auth',
            'dc2.admincenter.lib.backends',
        ]
)
