#!/usr/bin/env python

from dc2.web.client.lib.client import DC2SocketClient
from dc2.web.client.lib.commands import Commands



if __name__ == '__main__':
    foo = Commands(DC2SocketClient())
    foo.send_discovered_rack([{
        'cluster_no': '01',
        'rack_no': 'r{0}'.format(i+1),
        'dcname': 'laxa'
    } for i in range(0,10)])

    for i in range(0,10):
        foo.send_discovered_device([{
            'cluster_no':'01',
            'rack_no':'r{0}'.format(i+1),
            'dcname':'laxa',
            'device_type':'konan{0}'.format(d+1)
        } for d in range(0,39)])

