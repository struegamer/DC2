***************************
RPC Interface dc2.dhcp.mgmt
***************************

.. py:function:: dc2.dhcp.mgmt.list()

   :rtype: list
   :returns: list of :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`


.. py:function:: dc2.dhcp.mgmt.find(search=None)

	:param search: search record of type :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`
	:type search: dict

	:rtype: list
	:returns: list of :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`

.. py:function:: dc2.dhcp.mgmt.add(record=None)

	:param record: record to be added of type :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`
	:type record: dict

	:rtype: string
	:returns: _id of the last added record

.. py:function:: dc2.dhcp.mgmt.update(record=None)

	:param record: record to be updated, '_id' needs to be in the record, needs to be type of :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`
	:type record: dict

	:rtype: string
	:returns: _id of the last updated record

.. py:function:: dc2.dhcp.mgmt.get(record=None)

	:param record: should include necessary fields of type :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`
	:type record: dict

	:rtype: dict
	:returns: found document of type :doc:`DC² DHCP Mgmt Record </dc2/db-structure/dc2-dhcp-mgmt>`

.. py:function:: dc2.dhcp.mgmt.delete(record=None)

	:param record: record should only consists of '_id' field
	:type record: dict

	:rtype: Boolean
	:returns: True or False
	