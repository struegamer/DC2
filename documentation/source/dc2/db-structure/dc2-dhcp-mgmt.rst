DC² DHCP Mgmt Table Structure
=============================


Database: dc2db

Tablename: dhcp_mgmt

.. code-block:: json

   {
      "_id":"<string uuid>"
      "dcname":"<string>,
      "cluster_no":"<string>", 
      "rack_no":"<string>"
      "ipspace": "<string in ip cidr format>"
   }

Example:

.. code-block:: json

   {
     "dcname": "laxa",
     "cluster_no": "01",
     "rack_no": "r1",
     "ipspace": "192.168.1.0/24"
   }
