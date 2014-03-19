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

import types


def rpcmethod(**kwargs):

    def set_info(method):
        method.is_rpc = True
        method.is_xmlrpc = False
        method.is_jsonrpc = False
        method.params = {}
        method.returns = {}
        method.external_name = getattr(method, "__name__")

        if 'name' in kwargs:
            method.external_name = kwargs["name"]
        if 'params' in kwargs:
            method.params = kwargs["params"]
        if 'returns' in kwargs:
            method.returns = kwargs["returns"]
        return method
    return set_info

