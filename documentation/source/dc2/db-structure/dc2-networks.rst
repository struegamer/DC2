DC² DefaultClasses Table Structure
==================================


Database: dc2db

Tablename: networks

.. code-block:: javascript

   {
      "_id":"<string uuid>"
      "network":"<string ip address in CIDR format>",
      "name":"<string name of the network>",
      "description":"<string description>",
      "gateway":"<string ip address of the IP gateway>",
      "broadcast":<string broadcast address of the network>",
      "blocked_ips":"<string/int number of blocked ips, aka ammount of not usable ips>",
      "first_ip":"<string/int number of the first ip>",
      "vlan_no":"<string/int vlan number>",
   }
