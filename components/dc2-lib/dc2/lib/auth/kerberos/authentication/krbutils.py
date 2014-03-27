# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
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

import os
import os.path

krbccache_dir = '/tmp/'
krbccache_prefix = 'krbcc_'


def krb5_format_principal_name(user, realm):
        return '{0}@{1}'.format(user, realm)


def krb5_unparse_ccache(scheme, name):
        return '{0}:{1}'.format(scheme.upper(), name)


def get_ccache_name(scheme='FILE'):
        if scheme == 'FILE':
                name = os.path.join(krbccache_dir, '{0}{1}'.format(
                    krbccache_prefix, os.getpid()))
        else:
                raise ValueError('ccache scheme "{0}" unsupported'.format(
                    scheme))
        ccache_name = krb5_unparse_ccache(scheme, name)
        return ccache_name
