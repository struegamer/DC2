#!/usr/bin/env python

from dc2.web.client.lib.client import DC2SocketClient
from dc2.web.client.lib.commands import Commands



if __name__ == '__main__':
    foo = Commands(DC2SocketClient())
    foo.send_discovered({
        'cluster_no': '01',
        'rack_no': 'r1',
        'dcname': 'laxa'
    })
