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

# settings.py
import logging
import os
import os.path

# 
# MongoDB Server and Database Collections
#

MONGOS = {
             "admincenter": {
                "host":"localhost",
                "port":27017,
                "dbname":"admincenter",
                "database":None
             }
}

#LIBVIRT_SERVER= {
#        "xenserver01": {
#            "host":"xenserver01",
#            "method":"tls",
#            "conn":None
#        }
#}


#
# HTTP Access Headers
#
ACCESS_CONTROL_ALLOW_ORIGIN="*"
ACCESS_CONTROL_ALLOW_METHODS="GET,POST,OPTIONS,PUT,DELETE"

#
# HTTP Access Headers
#
ACCESS_CONTROL_ALLOW_ORIGIN="*"
ACCESS_CONTROL_ALLOW_METHODS="GET,POST,OPTIONS,PUT,DELETE"

#
# RPC Modules for RPCDispatcher
#
KERBEROS_AUTH_ENABLED=False
GRP_NAME_DC2ADMINS='dc2admins'

# 
# DC² Settings for PXE Boot
#
FREEIPA_SERVER_URL=''
TEMPLATE_DIR="%s/templates" % os.path.dirname(__file__)

CONTROLLER_MAPPINGS={
        '/':'MainController',
        '/login':'SessionController',
        '/backends':'BackendsCtrl',
        '/backends/servers':'ServerController',
        '/backends/hosts':'HostController',
        '/backends/installstate':'InstallStateController',
        '/admin':'admin.MainAdminController',
        '/admin/backends':'admin.BackendsController',
        '/admin/backends/environments':'admin.BackendEnvironmentController',
        '/admin/backends/defaultclasses':'admin.BackendDefaultClassesController',
        '/admin/backends/classtemplates':'admin.BackendClassTemplatesController',
        '/admin/backends/sysgroups':'admin.BackendSysGroupController',
        '/admin/backends/sysusers':'admin.BackendSysUserController',
        '/admin/backends/pxemethods':'admin.BackendPXEMethodController',
        '/admin/ribs':'admin.AdminRIBController',
        '/admin/ifacetypes':'admin.AdminInterfaceTypesController',
        '/admin/inettypes':'admin.AdminInetTypesController',
        '/admin/pxe':'admin.AdminPXEController',
        '/json/backends':'jsonctrl.JSONBackendController',
        '/json/backends/servers':'jsonctrl.JSONServerBackendController',
        '/json/backends/hosts':'jsonctrl.JSONHostBackendController',
        '/json/backends/deployments':'jsonctrl.JSONDeploymentBackendController',
        '/json/backends/macs':'jsonctrl.JSONMacBackendController',
        '/json/backends/ribs':'jsonctrl.JSONRibBackendController',
        }

#
# LOGFILE settings
#
if os.path.exists("/var/log/dc2-admincenter"):
    LOGFILE = "/var/log/dc2/dc2-admincenter.log"
else:
    LOGFILE = "dc2-admincenter.log"    
LOGLEVEL = logging.DEBUG


APPNAME = "dc2-admincenter"

