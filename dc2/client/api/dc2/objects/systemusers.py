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
import os
import os.path
import subprocess

class SystemUser(object):
    def __init__(self,rpcurl=None):
        self._rpcurl=rpcurl
        self._proxy=xmlrpclib.ServerProxy(self._rpcurl,allow_none=True)
    
    def create_all_users(self):
        userlist=[]
        userlist=self._proxy.dc2.configuration.systemusers.list()
        for user in userlist:
            self._create_user(user)
            
    def _create_user(self,user=None):
        if user is not None:
            call_args=[]
            if os.environ.has_key("ROOTCMD"):            
                call_args.append(os.environ["ROOTCMD"].split(" ")[0])
                call_args.append(os.environ["ROOTCMD"].split(" ")[1])
                
            if os.path.exists("/usr/sbin/useradd"):
                call_args.append("/usr/sbin/useradd")
                if user.has_key("username"):
                    call_args.append("-m")
                    call_args.append("--home")
                    call_args.append("/home/%s" % user["username"])
                    call_args.append("--shell")
                    call_args.append("/bin/bash")
                    if user.has_key("uid") and user["uid"]!="-1":
                        call_args.append("-u")
                        call_args.append("%s" % user["uid"])
                    if user.has_key("gid") and user["gid"]!="-1":
                        call_args.append("-g")
                        call_args.append("%s" % user["gid"])
                    if user.has_key("realname") and user["realname"] != "" and user["realname"] is not None:
                        call_args.append("-c")
                        call_args.append("%s" % user["realname"])
                    if user.has_key("cryptpw") and user["cryptpw"] != "" and user["cryptpw"] is not None:
                        call_args.append("-p")
                        call_args.append('%s' % user["cryptpw"])
                    call_args.append('%s' % user["username"])
                    subprocess.call(call_args)

                                    
                                
                
            
        
