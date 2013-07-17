# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################


#
# Standard Python libs
#
import sys
import os
import xmlrpclib
import re

#
# web.py module
#

try:
    import web
except ImportError:
    print "You need to install web.py"
    sys.exit(1)

#
# DC² own modules
#
try:
    from dc2.appserver.globals import connectionpool
    from dc2.appserver.globals import requestdispatcher
except ImportError:
    print "You are missing necessary DC² modules"
    sys.exit(1)

try:
    from settings import DOWNLOAD_SERVER_URL
    from settings import XMLRPC_BACKEND_SERVER_URL
    from settings import XMLRPC_BACKEND_SERVER_IP

except ImportError:
    print "You don't have a settings file in your Python path"
    sys.exit(1)


class BootServer:
    def GET(self, name):
        env_variables = None
        p = re.compile(r'01-(.*-.*-.*-.*-.*-.*)', re.VERBOSE)
        found = p.search(name)
        s = xmlrpclib.ServerProxy(XMLRPC_BACKEND_SERVER_URL, allow_none=True)
        web.header("Content-Type", "text/plain")
        if found is not None and len(found.groups()) > 0:
            mac_addr = found.group(1).replace("-", ":")
            mac_list = s.dc2.inventory.servers.macaddr.find({"mac_addr":mac_addr})
            if len(mac_list) > 0 and mac_list[0] is not None:
                mac_rec = mac_list[0]
                host_list = s.dc2.inventory.hosts.list({"server_id":mac_rec["server_id"]})
                if host_list is not None and len(host_list) > 0:
                    host_rec = host_list[0]
                    installstate = s.dc2.deployment.installstate.get({"host_id":host_rec["_id"]})
                    if host_rec.has_key("environments"):
                        environ_rec = s.dc2.configuration.environments.list({"name":host_rec["environments"]})[0]
                        env_variables = self.convert_to_dict(environ_rec["variables"])
                    else:
                        pass
                    if installstate is not None:
                        if installstate.has_key("status") and installstate["status"] == "localboot":
                            servers = s.dc2.inventory.servers.find({"_id":host_rec["server_id"]})
                            server = None
                            if servers is not None and len(servers) > 0:
                                server = servers[0]
                            if server is not None and server.has_key("product_name") and server["product_name"] is not None and server["product_name"] != "":
                                bootmethods = s.dc2.configuration.bootmethods.list({"hardware_type":server["product_name"]})
                                bootmethod = None
                                if bootmethods is not None and len(bootmethods) > 0:
                                    bootmethod = bootmethods[0]["pxe_bootmethod"]
                                return self.write_pxefile(mac_addr, "localboot", bootmethod=bootmethod)
                            else:
                                return self.write_pxefile(mac_addr, "localboot")
                        if installstate.has_key("status") and installstate["status"] == "deploy":
                            result = self.write_pxefile(mac_addr, 'deploy', env_variables)
                            if result is None:
                                raise web.notfound()
                            return result
                        if installstate.has_key("status") and installstate["status"] == "xenserver":
                            pass
            else:
                environ_rec = s.dc2.configuration.environments.list({"name":"INVENTORY"})[0]
                env_variables = self.convert_to_dict(environ_rec["variables"])
                # return self.write_pxefile(mac_addr, "inventory", env_variables["LINUX_KERNEL_NAME"], env_variables["LINUX_INITRD_NAME"], env_variables["FAI_NFSROOT"], env_variables["DC2_BACKEND_URL"])
                result = self.write_pxefile(mac_addr, 'inventory', env_variables)
                if result is None:
                    raise web.notfound()
                return result
        else:
            return web.notfound()

    # def write_pxefile(self, filename, action=None, kernel_name=None, initrd_name=None, nfs_root=None, backend_url=None, bootmethod=None):
    def write_pxefile(self, filename, action=None, env_variables=None, bootmethod=None):
        if action is not None:
            if action == "localboot":
                result = "DEFAULT chain.c32 hd0 0\n"
                if bootmethod is None:
                    result = "DEFAULT chain.c32 hd0 0\n"
                if bootmethod is not None:
                    if bootmethod == "chain.c32":
                        result = "DEFAULT chain.c32 hd0 0\n"
                    if bootmethod == "localboot":
                        result = "DEFAULT generated\n"
                        result += "LABEL generated\n"
                        result += "LOCALBOOT 0\n"
                    if bootmethod == "localboot-1":
                        result = "DEFAULT generated\n"
                        result += "LABEL generated\n"
                        result += "LOCALBOOT -1\n"
                return result
            if action == "inventory":
                result = "DEFAULT generated\n"
                result += "LABEL generated\n"
                result += "IPAPPEND 2\n"
                result += "KERNEL {0}/{1}\n".format(DOWNLOAD_SERVER_URL, env_variables['LINUX_KERNEL_NAME'])
                if env_variables['DC2_ROOTFS_TYPE'] == 'squashfs':
                    result += 'APPEND initrd={0}/{1} ip=dhcp nomodeset fetch={0}/{2}  DEBUG=1  boot=live nofb FAI_ACTION={3} FAI_FLAGS="createvt,sshd" DC2_BACKEND_URL="{4}"\n'.format(DOWNLOAD_SERVER_URL, env_variables['LINUX_INITRD_NAME'], env_variables['DC2_ROOTFS_IMAGE'], action, env_variables["DC2_BACKEND_URL"])
                if env_variables['DC2_ROOTFS_TYPE'] == 'nfs':
                    result += 'APPEND initrd={0}/{1} ip=dhcp root=/dev/nfs nomodeset nfsroot={2}  DEBUG=1  boot=live nofb FAI_ACTION={3} FAI_FLAGS="createvt,sshd" DC2_BACKEND_URL="{4}"\n'.format(DOWNLOAD_SERVER_URL, env_variables['LINUX_INITRD_NAME'], env_variables['FAI_NFSROOT'], action, env_variables["DC2_BACKEND_URL"])
                return result
            if action == "deploy":
                action = "install"
                result = "DEFAULT generated\n"
                result += "LABEL generated\n"
                result += "IPAPPEND 2\n"
                result += "KERNEL {0}/{1}\n".format(DOWNLOAD_SERVER_URL, env_variables['LINUX_KERNEL_NAME'])
                if env_variables['DC2_ROOTFS_TYPE'] == 'squashfs':
                    result += 'APPEND initrd={0}/{1} ip=dhcp nomodeset fetch={0}/{2}  DEBUG=1  boot=live nofb FAI_ACTION={3} FAI_FLAGS="createvt,sshd" DC2_BACKEND_URL="{4}"\n'.format(DOWNLOAD_SERVER_URL, env_variables['LINUX_INITRD_NAME'], env_variables['DC2_ROOTFS_IMAGE'], action, env_variables["DC2_BACKEND_URL"])
                if env_variables['DC2_ROOTFS_TYPE'] == 'nfs':
                    result += 'APPEND initrd={0}/{1} ip=dhcp root=/dev/nfs nomodeset nfsroot={2}  DEBUG=1  boot=live nofb FAI_ACTION={3} FAI_FLAGS="createvt,sshd" DC2_BACKEND_URL="{4}"\n'.format(DOWNLOAD_SERVER_URL, env_variables['LINUX_INITRD_NAME'], env_variables['FAI_NFSROOT'], action, env_variables["DC2_BACKEND_URL"])
                return result

    def convert_to_dict(self, list_of_vars=None):
        if list_of_vars is not None:
            vars = {}
            for entry in list_of_vars:
                vars[entry["name"]] = entry["value"]
            return vars
        return None


