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


def ssl_csr_create(key=None, digest="sha1", subjects=None):
    if key is None:
        # FIXME: named exception
        raise Exception("bla")
    if digest.lower() not in CSR_DIGESTS:
        # FIXME: named exception
        raise Exception('bla')
    if type(subjects) is not types.DictType:
        # FIXME: named exception
        raise Exception('foo')
    if not subjects.has_key("CN"):
        # FIXME: named exception
        raise Exception("No CommonName")
    for i in subjects.keys():
        if not i in SUBJECTS:
            #FIXME: named exception
            raise Exception('Wrong Subjects')        
    req = crypto.X509Req()
    subj = req.get_subject()
    try:
        for (keyf, value) in subjects.items():
            setattr(subj, keyf, value)
    except AttributeError, e:
        raise AttributeError(e.message)
    req.set_pubkey(key)
    req.sign(key, digest)
    return req

def ssl_csr_export(req=None):
    if req is None:
        #FIXME: named exception
        raise Exception("bla")
    req_dump = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req)
    return req_dump

def ssl_csr_import(req_dump=None):
    if req_dump is None:
        # FIXME: Named Exception
        raise Exception("bla")
    req = crypto.load_certificate_request(crypto.FILETYPE_PEM, req_dump)
    return req

    
        
