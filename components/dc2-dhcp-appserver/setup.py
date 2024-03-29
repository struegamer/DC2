#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from setuptools import setup, find_packages

setup(
    name='dc2.dhcp.appserver',
    version='0.1',
    description='DC2 AdminCenter',
    author='Stephan Adig',
    author_email='sh@sourcecode.de',
    url='http://launchpad.net/dc2/',
    namespace_packages=['dc2','dc2.dhcp'],
    packages=find_packages()
)
