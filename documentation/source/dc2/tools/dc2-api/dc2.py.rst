dc2.py
======

.. code-block:: bash

./dc2.py --help
Usage: dc2.py [options]

Options:
  --help                Show this help
  -s, --server          All commands are server related
  -h, --host            All commands are host related
  -e, --environment     All options are environment related
  -i, --installstatus   All Options are installstate related
  -u, --utilities       All following options are now utilities related
  --do-inventory        Do the inventory, for unknown servers
  --dc2-backend-url=<url to your dc2 backend server>
                        DC2 Backend URL (e.g. http://dc2db.domain.tld/RPC)

  Server Related Options:
    --server-find=[mac,serial]
                        Find a server by MACs or serial numbers
    --server-find-value=SERVER_FIND_VALUE
                        Value for --server-find
    --server-output-value=<key of server record>
                        Output the server value <key of server record>

  Host Related Options:
    --host-find=[mac,serial,hostname+domainname]
                        Find a host by MACs or server serial numbers or
                        host+domainname
    --host-find-value=HOST_FIND_VALUE
                        Value for --host-find
    --host-output-value=<key of server record>
                        Output the server value <key of server record>

  Environment Related Options:
    --environment-find=NAME
                        Find an environment by NAME
    --environment-variable=NAME
                        Print the value of the variable NAME

  Install Status Related Options:
    --installstatus-find=[mac,serial,host]
                        How to find the install status by server or host
    --installstatus-find-value=[server serial number, host+domainname]
                        Find the server with serial number or the host with
                        host+domainname
    --installstatus-update-status=[localboot,deploy]
                        Update Install Status for host or server
    --installstatus-update-progress=[None,PXEBoot,Deployment]
                        Update Install Progress for host or server

  Utilities Related Options:
    --write-udev-rules-file=FILENAME
                        Write udev rules file to FILE
    --utils-find-mac=MAC ADDR
                        Set MAC address for finding servers udev file
