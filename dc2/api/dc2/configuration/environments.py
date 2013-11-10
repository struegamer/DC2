# -*- coding: utf-8 -*-
###############################################################################
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
###############################################################################

import types
from dc2.api import RPCClient


class Environments(RPCClient):
    def find(self, rec=None):
        if rec is None:
            environmentlist = self._proxy.dc2.configuration.environments.list()
            return environmentlist
        if rec is not None:
            if type(rec) is not types.DictType:
                raise Exception('The search argument is not a dictionary')
            environmentlist = \
                self._proxy.dc2.configuration.environments.find(rec)
            return environmentlist

    def list(self):
        environmentlist = self.find()
        return environmentlist

    def get(self, *args, **kwargs):
        rec = {}
        if 'id' in kwargs:
            rec['_id'] = kwargs.get('id', None)
        environments = self._proxy.dc2.configuration.environments.find(rec)
        if len(environments) > 0 and len(environments) < 2:
            return environments[0]
        return None

    def add(self, *args, **kwargs):
        rec = None
        if 'environment' in kwargs:
            rec = kwargs['environment']
        if rec is not None:
            doc_id = self._proxy.dc2.configuration.environments.add(rec)
            return doc_id
        return None

    def update(self, *args, **kwargs):
        rec = None
        if 'environment' in kwargs:
            rec = kwargs['environment']
        if rec is not None:
            doc_id = self._proxy.dc2.configuration.environments.update(rec)
            return doc_id
        return None

    def new(self):
        rec = {}
        rec['name'] = ''
        rec['description'] = ''
        rec['variables'] = []
        return rec

    def delete(self, *args, **kwargs):
        rec = None
        if 'environment' in kwargs:
            rec = kwargs['environment']
        if rec is not None:
            result = self._proxy.dc2.configuration.environments.delete(rec)
            return result
        return None
