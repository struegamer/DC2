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

import xmlrpclib

class Cert(object):
    def __init__(self,rpcurl):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(rpcurl,allow_none=True)

    def cert_list(self):
        crt_list=self._proxy.cs2.ssl.certs.list()
        if crt_list is not None and len(crt_list)>0:
            return crt_list
        return None

    def cert_get(self,commonname=None):
        if commonname is not None and commonname != "":
            crt=self._proxy.cs2.ssl.certs.retrieve(commonname)
            if crt is not None:
                return crt
        return None
