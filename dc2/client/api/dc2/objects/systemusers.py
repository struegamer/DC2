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
import sys
import os
import os.path
import subprocess

try:
    from dc2.client.api.helpers.checkfai import check_for_rootcmd
    from dc2.client.api.helpers.checkfai import get_callargs_rootcmd
except ImportError, e:
    print e
    sys.exit(1)

class SystemGroups(object):
    def __init__(self, rpcurl=None):
        self._rpcurl = rpcurl
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)
        self._has_rootcmd = check_for_rootcmd()

    def _check_groupname(self, group=None):
        if group is not None:
            call_args = []
            if self._has_rootcmd:
                call_args = get_callargs_rootcmd(call_args)

            call_args.append("/usr/bin/getent")
            call_args.append("group")
            if group.has_key("groupname"):
                call_args.append(group["groupname"])
            return_code = subprocess.call(call_args, stdout=None)
            if return_code > 0:
                return True
            else:
                return False
        return None

    def _check_groupid(self, group=None):
        if group is not None:
            call_args = []
            if self._has_rootcmd:
                call_args = get_callargs_rootcmd(call_args)
            call_args.append("/usr/bin/getent")
            call_args.append("group")
            if group.has_key("gid"):
                call_args.append(group["gid"])
                return_code = subprocess.call(call_args, stdout=None)
                if return_code > 0:
                    return True
                else:
                    return False
        return None
    def create_all_groups(self):
        grouplist = self._proxy.dc2.configuration.systemgroups.list()
        if len(grouplist) > 0:
            for i in grouplist:
                if i.has_key("groupname"):
                    if self._check_groupname(i):
                        call_args = []
                        if self._has_rootcmd:
                            call_args = get_callargs_rootcmd(call_args)
                        call_args.append("/usr/sbin/addgroup")
                        if i.has_key("is_system_group") and i["is_system_group"] == "1":
                            call_args.append("--system")
                        if i.has_key("gid") and i["gid"] != "-1":
                            call_args.append("--gid")
                            call_args.append(i["gid"])
                        call_args.append(i["groupname"])
                        subprocess.call(call_args)

class SystemUser(object):
    def __init__(self, rpcurl=None):
        self._rpcurl = rpcurl
        self._proxy = xmlrpclib.ServerProxy(self._rpcurl, allow_none=True)
        self._has_rootcmd = check_for_rootcmd()

    def _check_user(self, user=None):
        if user is not None:
            call_args = []
            if self._has_rootcmd:
                call_args = get_callargs_rootcmd(call_args)

            call_args.append("id")
            if user.has_key("username"):
                call_args.append(user["username"])
            if subprocess.call(call_args) == 0:
                return True
            else:
                return False
        return None

    def _change_user_password(self, user=None):
        if user is not None:
            call_args = []
            if self._has_rootcmd:
                call_args = get_callargs_rootcmd(call_args)
            if os.path.exists("/usr/sbin/usermod"):
                call_args.append("/usr/sbin/usermod")
                if user.has_key("cryptpw") and user.has_key("username"):
                    call_args.append("-p")
                    call_args.append(user["cryptpw"])
                    call_args.append(user["username"])
                    if subprocess.call(call_args) == 0:
                        return True
                    else:
                        return False
        return None


    def create_all_users(self):
        userlist = []
        userlist = self._proxy.dc2.configuration.systemusers.list()
        for user in userlist:
            user_check = self._check_user(user)
            if user_check is not None:
                if user_check is not True:
                    self._create_user(user)
                else:
                    self._change_user_password(user)

    def _create_user(self, user=None):
        if user is not None:
            call_args = []
            if self._has_rootcmd:
                call_args = get_callargs_rootcmd(call_args)
            if os.path.exists("/usr/sbin/useradd"):
                call_args.append("/usr/sbin/useradd")
                if user.has_key("username"):
                    call_args.append("-m")
                    call_args.append("--home")
                    call_args.append("/home/%s" % user["username"])
                    call_args.append("--shell")
                    call_args.append("/bin/bash")
                    if user.has_key("uid") and str(user["uid"]) != "-1":
                        call_args.append("-u")
                        call_args.append("%s" % user["uid"])
                    if user.has_key("gid") and str(user["gid"]) != "-1":
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
                    if user.has_key("is_admin") and user["is_admin"] == "1":
                        admingroups = self._proxy.dc2.configuration.systemgroups.list({"is_admin_group":"1"})
                        admingroupstr = ""
                        if len(admingroups) > 0:
                            for i in admingroups:
                                call_args = []
                                if self._has_rootcmd:
                                    call_args = get_callargs_rootcmd(call_args)
                                call_args.append("/usr/sbin/adduser")
                                call_args.append(user["username"])
                                call_args.append(i["groupname"])
                                subprocess.call(call_args)
