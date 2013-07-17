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

from backends import BackendsController
from main import MainAdminController
from ribs import AdminRIBController
from interfacetypes import AdminInterfaceTypesController
from inettypes import AdminInetTypesController
from pxe import AdminPXEController
from backends_environments import BackendEnvironmentController
from backends_defaultclasses import BackendDefaultClassesController
from backends_classtemplates import BackendClassTemplatesController
from backends_sysgroups import BackendSysGroupController
from backends_sysusers import BackendSysUserController
from backends_pxemethods import BackendPXEMethodController
from installmethod import AdminInstallMethodController
