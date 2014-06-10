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
from OpenSSL import crypto
from ssl_constants import *

def ssl_cert_create(csr=None, serial_no=None, digest="sha1", notBefore=0, notAfter=0, ca_key=None, ca_cert=None):
    if csr is None:
        # FIXME: Named Exception
        raise Exception("No Request Buffer given")
    if serial_no is None:
        # FIXME: Named Exception
        raise Exception("Serial number not set or < 0")
    if not digest in DIGESTS:
        # FIXME: Named Exception
        raise Exception("Digest not in DIGEST set")
    if notBefore is None or notBefore < 0:
        # FIXME: Named Exception
        raise Exception("'Not Before' date not set or < 0")
    if notAfter is None or notAfter < 0:
        # FIXME: Named Exception
        raise Exception("'Not After' date not set or < 0")
    if ca_key is None:
        # FIXME: Named Exception
        raise Exception("CA Key not set")
    if ca_cert is None:
        # FIXME: Named Exception
        raise Exception("CA Certificate not set")
    
    cert = crypto.X509()
    cert.set_version(2)
    cert.set_serial_number(long(serial_no))
    cert.gmtime_adj_notBefore(notBefore)
    cert.gmtime_adj_notAfter(notAfter)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(csr.get_subject())
    cert.set_pubkey(csr.get_pubkey())
    ext1 = crypto.X509Extension('subjectKeyIdentifier', False, 'hash', subject=cert,)
    ext2 = crypto.X509Extension('basicConstraints', False, 'CA:FALSE')
    cert.add_extensions((ext1, ext2))
    cert.sign(ca_key, digest)
    return cert

def ssl_cert_import(cert_dump=None):
    if cert_dump is None:
        # FIXME: Named Exception
        raise Exception("cert_dump not set")
    cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_dump)
    return cert


def ssl_cert_export(cert_obj=None):
    if cert_obj is None:
        # FIXME: Named Exception
        raise Exception("Cert not set")
    cert_dump = crypto.dump_certificate(crypto.FILETYPE_PEM, cert_obj)
    return cert_dump
 
