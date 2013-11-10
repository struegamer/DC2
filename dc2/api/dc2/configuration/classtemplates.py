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


class ClassTemplates(RPCClient):
    def find(self, rec=None):
        if rec is None:
            datalist = self._proxy.dc2.configuration.classtemplates.list()
            return datalist
        if rec is not None:
            if type(rec) is not types.DictType:
                raise Exception('The search argument is not a dictionary')
            datalist = self._proxy.dc2.configuration.classtemplates.find(rec)
            return datalist

    def list(self):
        datalist = self.find()
        return datalist

    def new(self):
        rec = {}
        rec['name'] = ''
        rec['description'] = ''
        rec['classes'] = []
        return rec

    def add(self, *args, **kwargs):
        rec = {}
        if 'classtemplate' in kwargs:
            rec = kwargs.get('classtemplate', None)
        doc_id = self._proxy.dc2.configuration.classtemplates.add(rec)
        return doc_id

    def get(self, *args, **kwargs):
        id = ''
        if 'id' in kwargs:
            id = kwargs.get('id', None)
        result = self._proxy.dc2.configuration.classtemplates.get(id)
        return result

    def update(self, *args, **kwargs):
        rec = {}
        if 'classtemplate' in kwargs:
            rec = kwargs.get('classtemplate', None)
        doc_id = self._proxy.dc2.configuration.classtemplates.update(rec)
        return doc_id

    def delete(self, *args, **kwargs):
        rec = {}
        if 'id' in kwargs:
            rec['_id'] = kwargs.get('id', None)
        result = self._proxy.dc2.configuration.classtemplates.remove(rec)
        return result
