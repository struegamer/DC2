# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011  Stephan Adig <sh@sourcecode.de>
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
import types
import datetime
from OpenSSL import crypto
from ssl_constants import *



def ssl_crl_revoke_certificate(crl_obj=None, cert_obj=None, reason=None):
    if crl_obj is None:
        # FIXME: Named Exception
        raise Exception("CRL_OBJ is not set")
    if cert_obj is None:
        # FIXME: Named Exception
        raise Exception("cert_obj not set")
    if reason is None:
        # FIXME: Named Exception
        raise Exception("Revoke Reason not set")
    if not reason in REVOKE_REASONS:
        raise Exception("Revoke Reason is not in REVOKE_REASONS")
    
    revoke_obj = crypto.Revoked()
    revoke_obj.set_reason(reason)
    revoke_obj.set_serial(str(cert_obj.get_serial_number()))
    revoke_obj.set_rev_date(datetime.datetime.now().strftime("%Y%m%d%H%M%SZ"))
    crl_obj.add_revoked(revoke_obj)
    return crl_obj

def ssl_crl_create(ca_key=None, ca_cert=None):
    if ca_key is None:
        # FIXME: Named Exception
        raise Exception("ca_key not set")
    if ca_cert is None:
        # FIXME: Named Exception
        raise Exception("ca_cert not set")
    crl = crypto.CRL()
    return crl
    
def ssl_crl_import(crl_dump=None):
    if crl_dump is None:
        # FIXME: Named Exception
        raise Exception("crl_dump not set")
    crl = crypto.load_crl(crypto.FILETYPE_PEM, crl_dump)
    return crl

def ssl_crl_export(crl_obj=None, ca_key=None, ca_cert=None):
    if crl_obj is None:  
        # FIXME: Named Exception
        raise Exception("crl_obj not set")
    if ca_key is None:
        # FIXME: Named Exception
        raise Exception("ca_key not set")
    if ca_cert is None:
        # FIXME: Named Exception
        raise Exception("ca_cert not set")
    return crl_obj.export(ca_cert, ca_key, crypto.FILETYPE_PEM)

    
