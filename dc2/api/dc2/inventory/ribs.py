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

from dc2.api import RPCClient

class Ribs(RPCClient):

    def find(self,rec=None):
        if rec is None:
            datalist=self._proxy.dc2.inventory.servers.rib.list()
            return datalist
        if rec is not None:
            if type(rec) is not types.DictType:
                # TODO: Add Real Exception
                raise Exception('The search argument is not a dictionary')
            datalist=self._proxy.dc2.inventory.servers.rib.find(rec)
            return datalist

    def list(self):
        datalist=self.find()
        return datalist

    def count(self):
        # TODO: Add a rpc call to appserver for counting
        datalist=self.find()
        return len(datalist)

    def get(self,*args,**kwargs):
        rec={}
        if 'id' in kwargs:
            rec['_id']=kwargs.get('id',None)
        if 'server_id' in kwargs:
            rec['server_id']=kwargs.get('server_id',None)
        datalist=self._proxy.dc2.inventory.servers.rib.find(rec)
        return datalist
    
    def add(self,*args,**kwargs):
        rib_rec=None
        if 'rib' in kwargs:
            rib_rec = kwargs.get('rib',None)
        if rib_rec is not None:
            return self._proxy.dc2.inventory.servers.rib.add(rib_rec)
        return false
    def update(self,*args,**kwargs):
        rib_rec=None
        if 'rib' in kwargs:
            rib_rec = kwargs.get('rib',None)
        if rib_rec is not None:
            return self._proxy.dc2.inventory.servers.rib.update(rib_rec)
        return False
    def delete(self,*args,**kwargs):
        rib_rec={}
        if 'id' in kwargs:
            rib_rec['_id'] = kwargs.get('id',None)
        if len(rib_rec)>0:
            return self._proxy.dc2.inventory.servers.rib.delete(rib_rec)
        return False

