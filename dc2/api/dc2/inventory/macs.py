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

class Macs(RPCClient):

    def find(self,rec=None):
        if rec is None:
            datalist=self._proxy.dc2.inventory.servers.macaddr.list()
            return datalist
        if rec is not None:
            if type(rec) is not types.DictType:
                # TODO: Add Real Exception
                raise Exception('The search argument is not a dictionary')
            datalist=self._proxy.dc2.inventory.servers.macaddr.find(rec)
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
        macs=self._proxy.dc2.inventory.servers.macaddr.find(rec)
        if len(macs)>0 and len(macs)==1:
            return macs[0]
        elif len(macs)>0:
            return macs
        return None
    def add(self,*args,**kwargs):
        mac_rec=None
        if 'mac' in kwargs:
            mac_rec = kwargs.get('mac',None)
        if mac_rec is not None:
            return self._proxy.dc2.inventory.servers.macaddr.add(mac_rec)
        return False
    def update(self,*args,**kwargs):
        mac_rec=None
        if 'mac' in kwargs:
            mac_rec = kwargs.get('mac',None)
        if mac_rec is not None:
            return self._proxy.dc2.inventory.servers.macaddr.update(mac_rec)
        return False
    def delete(self,*args,**kwargs):
        mac_rec={}
        if 'id' in kwargs:
            mac_rec['_id'] = kwargs.get('id',None)
        if 'mac_addr' in kwargs:
            mac_rec['mac_addr'] = kwargs.get('mac_addr',None)
        if len(mac_rec)>0:
            return self.proxy.dc2.inventory.servers.macaddr.delete(mac_rec)
        return False

