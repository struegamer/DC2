# -*- coding: utf-8 -*-
#
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014  Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import sys
import xmlrpclib

try:
    from dc2.lib.db.mongo import Table
    from dc2.appserver.helpers import check_record
    from dc2.appserver.rpc import rpcmethod
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    import netaddr
except ImportError:
    print "You need to have the python-netaddr module installed"
    sys.exit(1)

try:
    from settings import MONGOS
except ImportError as e:
    print(e)
    sys.exit(1)

try:
    from dc2.dhcp.appserver.dhcp_server_config import\
        dc2_dhcp_mgmt_write_config
except ImportError as e:
    print(e)
    sys.exit(1)


tbl_dhcp_mgmt = Table(MONGOS['dc2db']['database'].get_table('dhcp_mgmt'))

DHCP_RECORD = {
    'dcname': True,
    'cluster_no': True,
    'rack_no': True,
    'ipspace': True
}


@rpcmethod(
    name='dc2.dhcp.mgmt.find',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True
)
def dc2_dhcp_mgmt_find(search=None):
    result = []
    if search is not None and isinstance(search, dict):
        result = tbl_dhcp_mgmt.find(search)
    else:
        result = tbl_dhcp_mgmt.find()
    return result


@rpcmethod(
    name='dc2.dhcp.mgmt.list',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True
)
def dc2_dhcp_mgmt_list():
    return dc2_dhcp_mgmt_find()


@rpcmethod(
    name='dc2.dhcp.mgmt.add',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True
)
def dc2_dhcp_mgmt_add(record=None):
    if record is not None and isinstance(record, dict):
        if (check_record(record, DHCP_RECORD) and
                tbl_dhcp_mgmt.find_one({
                    'ipspace': record['ipspace']}) is None):
            try:
                ip = netaddr.IPNetwork(record['ipspace'])
                if ip.size == 256:
                    doc_id = tbl_dhcp_mgmt.save(record)
                    return doc_id
            except netaddr.core.AddrFormatError as e:
                return xmlrpclib.Fault(-32501, e)
    return xmlrpclib.Fault(-32501, 'Record was not added')


@rpcmethod(
    name='dc2.dhcp.mgmt.update',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True)
def dc2_dhcp_mgmt_update(record=None):
    if record is not None and isinstance(record, dict):
        if ('_id' in record and
                check_record(record, DHCP_RECORD) and
                tbl_dhcp_mgmt.find_one({'_id': record['_id']}) is not None and
                tbl_dhcp_mgmt.find_one({
                    'ipspace': record['ipspace']}) is None):
            try:
                ip = netaddr.IPNetwork(record['ipspace'])
                if ip.size == 256:
                    doc_id = tbl_dhcp_mgmt.save(record)
                    return doc_id
            except netaddr.core.AddrFormatError as e:
                return xmlrpclib.Fault(-32501, e)
    return xmlrpclib.Fault(-32504, 'Record was not updated')


@rpcmethod(
    name='dc2.dhcp.mgmt.get',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True)
def dc2_dhcp_mgmt_get(record=None):
    if record is not None and isinstance(record, dict):
        if '_id' in record:
            doc = tbl_dhcp_mgmt.find_one({'_id': record['_id']})
            if doc is not None:
                return doc
            return xmlrpclib.Fault(-32500, 'Record not found')
    return xmlrpclib.Fault(-32500, 'Record not found')


@rpcmethod(
    name='dc2.dhcp.mgmt.delete',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True)
def dc2_dhcp_mgmt_delete(record=None):
    if record is not None and isinstance(record, dict):
        if '_id' in record:
            response = tbl_dhcp_mgmt.remove(record)
            if response is False:
                return xmlrpclib.Fault(-32503, 'Record was not removed')
            return True
    return xmlrpclib.Fault(-32503, 'Record was not removed')


@rpcmethod(
    name='dc2.dhcp.mgmt.writeconfig',
    returns={},
    params={},
    is_xmlrpc=True,
    is_jsonrpc=True)
def dc2_dhcp_mgmt_writeconfig(record=None):
    if record is not None and isinstance(record, dict):
        rec = None
        if '_id' in record:
            rec = tbl_dhcp_mgmt.find_one({'_id': record['_id']})
        elif 'ipspace' in record:
            rec = tbl_dhcp_mgmt.find_one({'ipspace': record['ipspace']})
        if rec is not None:
            if dc2_dhcp_mgmt_write_config(rec['ipspace']) is not False:
                return True
    return False
