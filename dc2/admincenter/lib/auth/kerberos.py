# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

import sys
import os

try:
    import web
except ImportError as e:
    print(e)
    print('you did not install web.py')
    print(e)
    sys.exit(1)

try:
    import krbV
except ImportError as e:
    print(e)
    print('you don\'t have python-krbV installed')
    print(e)
    sys.exit(1)

try:
    from dc2.lib.auth.kerberos.authentication import run
    from dc2.lib.auth.kerberos.authentication import krb5_format_principal_name
    from dc2.lib.auth.kerberos.authentication import get_ccache_name
except ImportError as e:
    print(e)
    print("You didn't install dc2.lib")
    print(e)
    sys.exit(1)

from exceptions import KerberosAuthError

ENCODING = 'UTF-8'

def do_kinit(username=None, password=None):
    if username is None or password is None:
        raise ValueError('Username and Password can\'t be None')
    if username == '' or password == '':
        raise ValueErorr('Username and Password can\'t be empty strings')
    realm = krbV.default_context().default_realm.decode(ENCODING)
    principal = krb5_format_principal_name(username, realm)
    ccache_name = get_ccache_name()
    (stdout, stderr, returncode) = run(['/usr/bin/kinit', principal],
            env={'KRB5CCNAME':ccache_name},
            stdin=password, raiseonerr=False)
    os.environ['KRB5CCNAME'] = ccache_name
    web.ctx.session.krb5ccname = ccache_name
    if returncode != 0:
        raise KerberosAuthError(principal=principal, message=unicode(stderr))

