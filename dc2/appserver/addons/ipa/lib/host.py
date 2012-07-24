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

if not FREEIPA_ENABLED:
    print "You need to enable FREEIPA use"
    sys.exit(1)
if not KERBEROS_AUTH_ENABLED:
    print "You need to enable KERBEROS Authentication"
    sys.exit(1)

def host_add(host_dict=None):
    pass

 takes_params = (
             Str('fqdn', _hostname_validator,
                             cli_name='hostname',
                                         label=_('Host name'),
                                                     primary_key=True,
                                                                 normalizer=normalize_hostname,
                                                                         ),
                     Str('description?',
                                     cli_name='desc',
                                                 label=_('Description'),
                                                             doc=_('A description of this host'),
                                                                     ),
                             Str('l?',
                                             cli_name='locality',
                                                         label=_('Locality'),
                                                                     doc=_('Host locality (e.g. "Baltimore, MD")'),
                                                                             ),
                                     Str('nshostlocation?',
                                                     cli_name='location',
                                                                 label=_('Location'),
                                                                             doc=_('Host location (e.g. "Lab 2")'),
                                                                                     ),
                                             Str('nshardwareplatform?',
                                                             cli_name='platform',
                                                                         label=_('Platform'),
                                                                                     doc=_('Host hardware platform (e.g. "Lenovo T61")'),
                                                                                             ),
                                                     Str('nsosversion?',
                                                                     cli_name='os',
                                                                                 label=_('Operating system'),
                                                                                             doc=_('Host operating system and version (e.g. "Fedora 9")'),
                                                                                                     ),
                                                             Str('userpassword?',
                                                                             cli_name='password',
                                                                                         label=_('User password'),
                                                                                                     doc=_('Password used in bulk enrollment'),
                                                                                                             ),
                                                                     Flag('random?',
                                                                                     doc=_('Generate a random password to be used in bulk enrollment'),
                                                                                                 flags=('no_search', 'virtual_attribute'),
                                                                                                             default=False,
                                                                                                                     ),
                                                                             Str('randompassword?',
                                                                                             label=_('Random ('usercertificate?', validate_certificate,
                                                                                                             cli_name='certificate',
                                                                                                                         label=_('Certificate'),
                                                                                                                                     doc=_('Base-64 encoded server certificate'),
                                                                                                                                             ),
                                                                                                     Str('krbprincipalname?',
                                                                                                                     label=_('Principal name'),
                                                                                                                                 flags=['no_create', 'no_update', 'no_search'],
                                                                                                                                         ),
                                                                                                             Str('macaddress*',
                                                                                                                             normalizer=lambda value: value.upper(),
                                                                                                                                         pattern='^([a-fA-F0-9]{2}[:|\-]?){5}[a-fA-F0-9]{2}$',
                                                                                                                                                     pattern_errmsg='Must be of the form HH:HH:HH:HH:HH:HH, where each H is a hexadecimal character.',
                                                                                                                                                                 csv=True,
                                                                                                                                                                             label=_('MAC address'),
                                                                                                                                                                                         doc=_('Hardware MAC address(es) on this host'),
                                                                                                                                                                                                 ),
                                                                                                                     Bytes('ipasshpubkey*', validate_sshpubkey,
                                                                                                                                     cli_name='sshpubkey',
                                                                                                                                                 label=_('Base-64 encoded SSH public key'),
                                                                                                                                                             flags=['no_search'],
                                                                                                                                                                     ),
                                                                                                                             Str('sshpubkeyfp*',
                                                                                                                                             label=_('SSH public key fingerprint'),
                                                                                                                                                         flags=['virtual_attribute', 'no_create', 'no_update', 'no_search'],
                                                                                                                                                                 ),
                                                                                                                             assword'),

