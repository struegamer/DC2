# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

import types
from dc2.api import RPCClient


class SysUsers(RPCClient):
    def find(self, rec=None):
        if rec is None:
            userlist = self._proxy.dc2.configuration.systemusers.list()
            return userlist
        if rec is not None:
            if type(rec) is not types.DictType:
                raise Exception('The search argument is not a dictionary')
            userlist = self._proxy.dc2.configuration.systemusers.list(rec)
            return userlist

    def list(self):
        userlist = self.find()
        return userlist

    def new(self):
        rec = {}
        rec['username'] = ''
        rec['realname'] = ''
        rec['uid'] = ''
        rec['is_admin'] = '0'
        rec['cryptpw'] = ''
        rec['ssh_pubkey'] = ''
        return rec

    def get(self, *args, **kwargs):
        rec = {}
        if 'id' in kwargs:
            rec['_id'] = kwargs.get('id', None)
        userlist = self._proxy.dc2.configuration.systemusers.list(rec)
        if len(userlist) > 0:
            return userlist[0]
        return None

    def add(self, *args, **kwargs):
        rec = {}
        if 'user' in kwargs:
            rec = kwargs.get('user', None)
        doc_id = self._proxy.dc2.configuration.systemusers.add(rec)
        return doc_id

    def update(self, *args, **kwargs):
        rec = {}
        if 'user' in kwargs:
            rec = kwargs.get('user', None)
        doc_id = self._proxy.dc2.configuration.systemusers.update(rec)
        return doc_id

    def delete(self, *args, **kwargs):
        rec = {}
        if 'id' in kwargs:
            rec['_id'] = kwargs.get('id', None)
        result = self._proxy.dc2.configuration.systemusers.delete(rec)
        return result
