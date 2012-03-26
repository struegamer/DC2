SSL CERT Methods
================

.. py:module:: cs2rpcmethods



Global Data
-----------

.. py:data:: tbl_certs
   :noindex:
.. py:data:: tbl_crls



Module Methods
--------------

.. py:function:: cs2_ssl_crls_list()

   :rtype: list of dict
   :returns: list of :doc:`SSL CRL Records </cs2/db-structure/cs2-ssl-crls>`
   
.. py:function:: cs2_ssl_crls_get(ca_name=None)

   :param ca_name: Name of the CA
   :type ca_name: string
   
   :rtype: dict
   :returns: :doc:`SSL CRL Records </cs2/db-structure/cs2-ssl-crls>`
   
.. py:function:: cs2_ssl_crls_revoke_cert(commonname=None,reason=None)

   :param commoname: Commonname
   :type commonname: string
   
   :param reason: Revoke Reason
   :type reason: string
   
   :rtype: dict
   :returns: :doc:`SSL CRL Records </cs2/db-structure/cs2-ssl-crls>`
   
   
   
   
