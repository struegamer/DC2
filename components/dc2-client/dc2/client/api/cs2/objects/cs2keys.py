# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

class Keys(object):
    def __init__(self,rpcurl):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(rpcurl,allow_none=True)

    def get_key_pem(self,keyname=None):
        if keyname is not None and keyname != "":
            key_pem=self._proxy.cs2.ssl.keys.retrieve(keyname)
            if key_pem is not None:
                return key_pem
        return None

    def key_list(self):
        key_list=self._proxy.cs2.ssl.keys.list()
        if key_list is not None and len(key_list)>0:
            return key_list
        return None

