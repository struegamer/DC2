Environment Methods
===================

.. py:module:: dc2rpcmethods

Global Data
-----------

.. py:data:: tbl_environments
	:noindex:

Methods
-------

.. py:function:: dc2_deployment_environments_list(search=None)

   :param search: Search Record of type :doc:`DC² Environment Record </dc2/db-structure/dc2-environments>`
   :type search: dict
   
   :rtype: list of dicts
   :returns: list of :doc:`DC² Environment Record </dc2/db-structure/dc2-environments>`

.. py:function:: dc2_deployment_environments_add(env_rec=None)

   :param env_rec: :doc:`DC² Environment Record </dc2/db-structure/dc2-environments>`
   :type env_rec: dict
   
   :rtype: string
   :returns: doc_id


.. py:function:: dc2_deployment_environments_update(env_rec=None)

   :param env_rec: :doc:`DC² Environment Record </dc2/db-structure/dc2-environments>`
   :type env_rec: dict
   
   :rtype: string
   :returns: doc_id


.. py:function:: dc2_deployment_environments_delete(env_rec=None)

   :param env_rec: :doc:`DC² Environment Record </dc2/db-structure/dc2-environments>`
   :type env_rec: dict
   
   :rtype: bool
   :returns: True => record deleted, False => Record not deleted
   


