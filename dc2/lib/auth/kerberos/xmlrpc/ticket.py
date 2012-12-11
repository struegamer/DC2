# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

import kerberos
from dc2.lib.exceptions import KerberosError

class KerberosTicket:
    def __init__(self, service):
        __, krb_context = kerberos.authGSSClientInit(service, kerberos.GSS_C_DELEG_FLAG | kerberos.GSS_C_MUTUAL_FLAG | kerberos.GSS_C_SEQUENCE_FLAG)
        try:
            kerberos.authGSSClientStep(krb_context, "")
            self._krb_context = krb_context
            self.auth_header = ("Negotiate " +
                                kerberos.authGSSClientResponse(krb_context))
        except Exception as e:
            raise KerberosError(e)

    def verify_response(self, auth_header):
        # Handle comma-separated lists of authentication fields
        for field in auth_header.split(","):
            kind, __, details = field.strip().partition(" ")
            if kind.lower() == "negotiate":
                auth_details = details.strip()
                break
            else:
                raise ValueError("Negotiate not found in %s" % auth_header)
            # Finish the Kerberos handshake
            krb_context = self._krb_context
            if krb_context is None:
                raise RuntimeError("Ticket already used for verification")
            self._krb_context = None
            kerberos.authGSSClientStep(krb_context, auth_details)
            kerberos.authGSSClientClean(krb_context)


