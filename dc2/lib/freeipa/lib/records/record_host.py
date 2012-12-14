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
import types
import base64
import xmlrpclib

from record_base import RecordBase

class RecordHost(RecordBase):
    def _make_pem(self, cert_data):
        """
        Convert a raw base64-encoded blob into something that looks like a PEM
        file with lines split to 64 characters and proper headers.
        
        Taken from FreeIPA/ipalib/x509.py
        Adjusted to python3 format
        
        Copyright (C) 2010 RedHat 
        Authors:  Rob Crittenden <rcritten@redhat.com>
        License: GPLv3
        
        """
        pemcert = '\n'.join([cert_data[x:x + 64] for x in range(0, len(cert_data), 64)])
        return '-----BEGIN CERTIFICATE-----\n{0}\n-----END CERTIFICATE-----'.format(pemcert)


    def _return_special_data(self, name):
        if name == 'usercertificate':
            usercert = self._raw_data[name]
            pemcerts = []
            for cert in usercert:
                if isinstance(cert, xmlrpclib.Binary):
                    pemcert = self._make_pem(base64.b64encode(cert.data))
                    pemcerts.append(pemcert)
            return pemcerts
        return None
