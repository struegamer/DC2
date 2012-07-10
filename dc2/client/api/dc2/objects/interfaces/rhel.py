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

import sys
import os
from dc2.client.api.dc2 import MACs

def running_in_fai():
    if os.environ.has_key('FAI_VERSION'):
        return True
    return False

def write_interface_file(interface_name=None,contents=None):
    if running_in_fai():
        target_dir=os.environ['target']
    fp=open('%s/etc/sysconfig/network-scripts/ifcfg-%s' % (target_dir,interface_name),'wb')
    fp.write('#\n')
    fp.write('# This file was created by (DC)²\n')
    fp.write('#\n\n')
    fp.write(contents)
    fp.close()

def write_interface_route_file(interface_name=None, contents=None):
    if running_in_fai():
        target_dir=os.environ['target']
    fp=open('%s/etc/sysconfig/network-scripts/route-%s' % (target_dir, interface_name),'wb')
    fp.write('#\n')
    fp.write('# This file was created by (DC)²\n')
    fp.write('#\n\n')
    fp.write(contents)
    fp.close()
	
def write_interface_slave_file(interface_name=None,bond_name=None):
    if running_in_fai():
        target_dir=os.environ['target']
    fp=open('%s/etc/sysconfig/network-scripts/ifcfg-%s' % (target_dir,interface_name),'wb')
    fp.write('#\n')
    fp.write('# This file was created by (DC)²\n')
    fp.write('#\n\n')
    fp.write('DEVICE=%s\n' % interface_name)
    fp.write('BOOTPROTO=none\n')
    fp.write('ONBOOT=yes\n')
    fp.write('MASTER=%s\n' % bond_name)
    fp.write('SLAVE=yes\n')
    fp.write('USERCTL=no\n')
    fp.close()


def write_host_network_configuration(host=None):
    if host is not None:
        if host.has_key('interfaces'):
            for interface in host['interfaces']:
                contents=''
                contents+='DEVICE=%s\n' % interface['name']
                if interface['type']=='loopback':
                    if interface['inet']=='loopback':
                        contents+='IPADDR=127.0.0.1\n'
                        contents+='NETMASK=255.0.0.0\n'
                        contents+='NETWORK=127.0.0.0\n'
                        contents+='BROADCAST=127.255.255.255\n'
                        contents+='ONBOOT=yes\n'
                        contents+='NAME=loopback\n'
                    if interface['inet']!='loopback':
                        contents+='IPADDR=%s\n' % interface['ip']
                        contents+='NETMASK=%s\n' % interface['netmask']
                        contents+='ONBOOT=yes\n'
                        contents+='NAME=%s\n' % interface['name']
                    write_interface_file(interface['name'],contents)
                if interface['type']=='ethernet':
                    contents+='ONBOOT=yes\n'
                    contents+='NAME=%s\n' % interface['name']
                    if interface['inet']=='static':
                        contents+='IPADDR=%s\n' % interface['ip']
                        contents+='NETMASK=%s\n' % interface['netmask']
                        contents+='BOOTPROTO=none\n'
                    if interface['inet']=='dhcp':
                        contents+='BOOTPROTO=dhcp'					
                    write_interface_file(interface['name'],contents)
                if interface['type']=='bond_1' or interface['type']=='bond_2':
                    contents+='ONBOOT=yes\n'
                    contents+='NAME=%s\n' % interface['name']
                    if interface['type']=='bond_1':
                        contents+='BONDING_OPTS="mode=1 miimon=100 updelay=200"\n'
                    if interface['type']=='bond_2':
                        contents+='BONDING_OPTS="mode=2 miimon=100 xmit_hash_policy=2"\n'
                    if interface['inet']=='static':
                        contents+='IPADDR=%s\n' % interface['ip']
                        contents+='NETMASK=%s\n' % interface['netmask']
                        contents+='BOOTPROTO=none\n'
                    write_interface_file(interface['name'],contents)
                    if interface.has_key('slaves'):
                        for slave in interface['slaves']:
                            write_interface_slave_file(slave,interface['name'])
                    if interface['inet']=='dhcp':
                        contents+='BOOTPROTO=dhcp\n'
                if interface['type']=='vlan':
                    contents+='VLAN=yes\n'
                    contents+='VLAN_NAME_TYPE=VLAN_PLUS_VID_NO_PAD\n'
                    contents+='BOOTPROTO=none\n'
                    contents+='PHYSDEV=%s\n' % interface['vlan_raw_device']
                    write_interface_file(interface['name'],contents)
                if interface.has_key('gateway') and interface['gateway'] is not None and interface['gateway']!='':
                    write_interface_route_file(interface['name'],'default via %s dev %s\n' % (interface['gateway'],interface['name']))
