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
import xmlrpclib
import types

try:
    from settings import FREEIPA_ENABLED
    from settings import KERBEROS_AUTH_ENABLED
    from settings import FREEIPA_SERVER_URL
    from settings import FREEIPA_KERBEROS_SERVICE
except ImportError,e:
    print "You don't have a settings file"
    sys.exit(1)

try:
    from dc2.lib.auth.kerberos import KerberosServerProxy
except ImportError,e:
    print "Your DC2 installation is not correct"
    sys.exit(1)

if not FREEIPA_ENABLED:
    print "You need to enable FREEIPA use"
    sys.exit(1)
if not KERBEROS_AUTH_ENABLED:
    print "You need to enable KERBEROS Authentication"
    sys.exit(1)

iparpc=KerberosServerProxy(FREEIPA_SERVER_URL,FREEIPA_KERBEROS_SERVICE,allow_none=True)

def host_add(host_dict=None):
    """Needed input keys:
        fqdn
        description
        locality
        nshostlocation
        nshardwareplatform
        nsosversion
        userpassword
        random:True/false
        usercertificate:base64
        krbprincipalname
        macaddress
        ipasshpubkey:base64
        sshpubkeyfp:ssh fingerprint
    """
    if host_dict is None or type(host_dict) is not types.DictType:
        raise Exception('host_dict is none or not of type Dict')
    pass

def host_find(host_dict=None):
    if host_dict is None or type(host_dict) is not types.DictType:
        raise Exception('host_dict is none or not of type Dict')
    pass

def host_del(host_dict=None):
    if host_dict is None or type(host_dict) is not types.DictType:
        raise Exception('host_dict is none or not of type Dict')
    pass

def host_mod(host_dict=None):
    if host_dict is None or type(host_dict) is not types.DictType:
        raise Exception('host_dict is none or not of type Dict')
    pass
