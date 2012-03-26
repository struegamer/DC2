DefaultClasses Methods
======================

.. py:module:: dc2rpcmethods

Global Data
-----------

.. py:data:: tbl_templates

Methods
-------

.. py:function:: dc2_deployment_classtemplates_list(search=None)

   :param search: Search Record of type :doc:`DC² ClassTemplates Record </dc2/db-structure/dc2-classtemplates>`
   :type search: dict
   
   :rtype: list of dicts
   :returns: list of  :doc:`DC² ClassTemplates Record </dc2/db-structure/dc2-classtemplates>`

.. py:function:: dc2_deployment_classtemplates_add(record=None)

   :param record: :doc:`DC² ClassTemplates Record </dc2/db-structure/dc2-classtemplates>`
   :type record: dict
   
   :rtype: dict
   :returns: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-classtemplates>`

.. py:function:: dc2_deployment_classtemplates_update(record=None)

   :param record: :doc:`DC² ClassTemplates Record </dc2/db-structure/dc2-classtemplates>`
   :type record: dict
   
   :rtype: dict
   :returns: :doc:`DC² ClassTemplates Record </dc2/db-structure/dc2-classtemplates>`

.. py:function:: dc2_deployment_classtemplates_delete(record=None)

   :param record: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-classtemplates>`
   :type record: dict
   
   :rtype: bool
   :returns: True or False
