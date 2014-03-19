# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
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

import sys
import xmlrpclib
import types
import datetime

try:
    import web
except ImportError:
    print "You don't have web.py installed"
    sys.exit(1)

from helpers import rpc_datetime_isoformat
from helper import parse_output


def xenserver_get_vms(xenhost=None, session_id=None, vmtype=None):
    if xenhost is None:
        return False
    if session_id is None:
        return False
    if vmtype is None:
        return False
    if vmtype != "template" and vmtype != "vms" and vmtype != "both":
        return False
    s = xmlrpclib.ServerProxy("https://%s/" % xenhost, allow_none=True)
    vmlist = parse_output(s.VM.get_all(session_id))
    vmlist_dict = []
    if len(vmlist) > 0:
        for vm in vmlist:
            if not parse_output(s.VM.get_is_control_domain(session_id, vm)) and parse_output(s.VM.get_is_a_template(session_id, vm)) and (vmtype == "template" or vmtype == "both"):
                vmlist_dict.append({"session_id":session_id, "xen_host":xenhost, "vm_name":parse_output(s.VM.get_name_label(session_id, vm)), "vm_description":parse_output(s.VM.get_name_description(session_id, vm)), "vm_id":vm})
            if not parse_output(s.VM.get_is_control_domain(session_id, vm)) and not parse_output(s.VM.get_is_a_template(session_id, vm)) and (vmtype == "vms" or vmtype == "both") :
                vmlist_dict.append({"session_id":session_id, "xen_host":xenhost, "vm_name":parse_output(s.VM.get_name_label(session_id, vm)), "vm_description":parse_output(s.VM.get_name_description(session_id, vm)), "vm_id":vm})
        return vmlist_dict
    return None

def xenserver_get_vms_record(xenhost=None, session_id=None, vm_id=None):
    if xenhost is None:
        return None
    if session_id is None:
        return None
    if vm_id is None:
        return None
    try:
        s = xmlrpclib.ServerProxy("https://%s/" % xenhost, allow_none=True)
        vm_record = parse_output(s.VM.get_record(session_id, vm_id))
        for key in vm_record.keys():
            if isinstance(vm_record[key], xmlrpclib.DateTime):
                vm_record[key] = rpc_datetime_isoformat(vm_record[key])
        return vm_record
    except Exception, e:
        raise Exception(e)



