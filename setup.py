#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
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
#

import setuptools
from distutils.core import setup

setup(name='dc2',
      version='0.10',
      description='DC² Namespace Package',
      author='Stephan Adig',
      author_email='sh@sourcecode.de',
      url='http://launchpad.net/dc2',
      packages=['dc2']
      )

setup(name="dc2.distrotools",
      version='0.10',
      description="DC² Distrotools",
      author="Stephan Adig",
      author_email="sh@sourcecode.de",
      url="http://launchpad.net/dc2",
      packages=['dc2.distrotools',
                'dc2.distrotools.config',
                'dc2.distrotools.actions'],
      namespace_packages=['dc2'],
      scripts=[
          'scripts/dc2-mirror',
          'scripts/dc2-create-chroot'
      ]
      )

setup(name="dc2.client",
      version='0.10',
      description="DC² Client",
      author="Stephan Adig",
      author_email="sh@sourcecode.de",
      url="http://launchpad.net/dc2",
      namespace_packages=['dc2'],
      packages=['dc2.client',
                'dc2.client.api',
                'dc2.client.api.dc2.inventory',
                'dc2.client.api.dc2.inventory.lshw',
                'dc2.client.api.dc2.cliparsers',
                'dc2.client.api.dc2',
                'dc2.client.api.helpers',
                'dc2.client.api.dc2.objects',
                'dc2.client.api.dc2.objects.interfaces',
                'dc2.client.api.dc2.addons',
                'dc2.client.api.dc2.addons.freeipa',
                'dc2.client.api.cs2',
                'dc2.client.api.cs2.objects'
                ],
      scripts=[
          'scripts/dc2-client',
          'scripts/dc2-ssl-client',
          'scripts/dc2-client-ng'
      ])

setup(name="dc2.appserver",
      version='0.10',
      description="DC² Application Server",
      author="Stephan Adig",
      author_email="sh@sourcecode.de",
      url="http://launchpad.net/dc2",
      namespace_packages=['dc2'],
      packages=['dc2.appserver',
                'dc2.appserver.apps',
                'dc2.appserver.auth',
                'dc2.appserver.auth.rpcmethods',
                'dc2.appserver.globals',
                'dc2.appserver.helpers',
                'dc2.appserver.rpc',
                'dc2.appserver.rpcmethods',
                'dc2.appserver.addons',
                'dc2.appserver.addons.freeipa',
                'dc2.appserver.addons.dns'],
      scripts=["scripts/dc2-prepare_initial_data", "scripts/dc2-squashfs"])

setup(name='dc2.lib',
      version='0.10',
      description='DC2 General Library',
      author='Stephan Adig',
      author_email='sh@sourcecode.de',
      url='http://launchpad.net/dc2',
      namespace_packages=['dc2'],
      packages=['dc2.lib',
          'dc2.lib.exceptions',
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
          'dc2.lib.web.requesthandlers',
          'dc2.lib.web.controllers',
          'dc2.lib.web.helpers',
          'dc2.lib.decorators',
          'dc2.lib.decorators.logging',
          'dc2.lib.transports',
          'dc2.lib.logging',
          'dc2.lib.freeipa',
          'dc2.lib.freeipa.lib',
          'dc2.lib.freeipa.lib.objects',
          'dc2.lib.freeipa.lib.records']
      )

setup(name='dc2.api',
      version='0.10',
      description='DC2 API',
      author='Stephan Adig',
      author_email='sh@sourcecode.de',
      url='http://launchpad.net/dc2',
      namespace_packages=['dc2'],
      packages=[
          'dc2.api',
          'dc2.api.dc2',
          'dc2.api.dc2.inventory',
          'dc2.api.dc2.deployment',
          'dc2.api.dc2.configuration',
          'dc2.api.dc2.settings',
          'dc2.api.dc2.addons',
          'dc2.api.dc2.addons.freeipa',
          'dc2.api.dc2.addons.dns',
      ]
      )

setup(name='dc2.admincenter',
      version='0.10',
      description='DC2 AdminCenter',
      author='Stephan Adig',
      author_email='sh@sourcecode.de',
      url='http://launchpad.net/dc2/',
      namespace_packages=['dc2'],
      packages=[
          'dc2.admincenter',
          'dc2.admincenter.apps',
          'dc2.admincenter.apps.controllers',
          'dc2.admincenter.apps.controllers.admin',
          'dc2.admincenter.apps.controllers.admin.jsonctrl',
          'dc2.admincenter.apps.controllers.jsonctrl',
          'dc2.admincenter.globals',
          'dc2.admincenter.lib',
          'dc2.admincenter.lib.auth',
          'dc2.admincenter.lib.backends',
          'dc2.admincenter.lib.controllers',
          'dc2.admincenter.lib.ribs',
          'dc2.admincenter.lib.interfacetypes',
          'dc2.admincenter.lib.inettypes',
          'dc2.admincenter.lib.pxemethods',
          'dc2.admincenter.lib.installmethods',
      ]
      )
