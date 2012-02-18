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

import xmlrpclib

class CSR(object):
    def __init__(self,rpcurl):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(rpcurl,allow_none=True)
        
    def csr_list(self):
        csr_list=self._proxy.cs2.ssl.csrs.list()
        if csr_list is not None and len(csr_list)>0:
            return csr_list
        return None
        
    def csr_get(self,commonname=None):
        if commonname is not None and commonname != "":
            csr=self._proxy.cs2.ssl.csrs.retrieve(commonname)
            if csr is not None:
                return csr
        return None
        