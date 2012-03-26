DC² DefaultClasses Table Structure
==================================


Database: dc2db

Tablename: hosts

.. code-block:: javascript

   {
      "_id":"<string uuid>"
      "server_id":"<string uuid of server>,
      "hostname":"<string hostname>", 
      "domainname":"<string domainname>",
      "hostclasses":"<array of strings of classnames>"
      "interfaces":"<array of dicts of interface structure>"
   }
   
Structure: interfaces

.. code-block:: javascript

   {
      "name":<string interface name e.g. eth0>
      "type":<string interface type choice of "loopback","ethernet","bond_1","bond_2","vlan">
      "inet":<string interface inet type choice of "loopback","dhcp","static","manual">
      "ip":<string ip address>
      "netmask":<string netmask>
      "gateway":<string gateway ip>
      "slaves":<array of slave interfaces, when interface type == bond_1 || interface type == bond_2>
      "vlan_raw_device":<string device name of vlan_raw_device when interface_type == vlan>
      "pre_up":<string>
      "pre_down":<string>
      "post_up":<string>
      "post_down":<string>
   }
      
