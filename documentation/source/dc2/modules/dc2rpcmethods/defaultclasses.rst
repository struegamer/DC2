DefaultClasses Methods
======================

.. py:module:: dc2rpcmethods

Global Data
-----------

.. py:data:: tbl_server

Methods
-------

.. py:function:: dc2_deployment_defaultclasses_list(search=None)

   :param search: Search Record of type :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`
   :type search: dict
   
   :rtype: list of dicts
   :returns: list of  :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`

.. py:function:: dc2_deployment_defaultclasses_add(defclass_rec=None)

   :param defclass_rec: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`
   :type defclass_rec: dict
   
   :rtype: dict
   :returns: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`

.. py:function:: dc2_deployment_defaultclasses_update(defclass_rec=None)

   :param defclass_rec: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`
   :type defclass_rec: dict
   
   :rtype: dict
   :returns: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`

.. py:function:: dc2_deployment_defaultclasses_delete(defclass_rec=None)

   :param defclass_rec: :doc:`DC² DefaultClasses Record </dc2/db-structure/dc2-defaultclasses>`
   :type defclass_rec: dict
   
   :rtype: bool
   :returns: True or False
