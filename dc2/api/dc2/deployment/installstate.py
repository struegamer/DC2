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

import types
from dc2.api import RPCClient


class InstallState(RPCClient):

    def find(self,rec=None):
        resultlist=[]
        if rec is None:
            resultlist=self._proxy.dc2.deployment.installstate.list()
        if rec is not None:
            if type(rec) is not types.DictType:
                # TODO: Add Real Exception
                raise Exception('The search argument is not a dictionary')
            resultlist=self._proxy.dc2.deployment.installstate.find(rec)
        return resultlist

    def list(self):
        resultlist=[]
        resultlist=self.find()
        return resultlist

    def count(self,status='localboot'):
        # TODO: Add a rpc call to appserver for counting
        resultlist=self.find({'status':status})
        return len(resultlist)


