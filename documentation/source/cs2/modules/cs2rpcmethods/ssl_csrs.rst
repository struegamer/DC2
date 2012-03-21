SSL CSR Methods
===============

.. py:module:: cs2rpcmethods



Global Data
-----------

.. py:data:: tbl_keys
   :noindex:
.. py:data:: tbl_csrs


Module Methods
--------------

.. py:function:: cs2_ssl_csrs_list()

   :rtype: list of dict
   :returns: list of :doc:`SSL CSR Records </cs2/db-structure/cs2-ssl-csrs>`

.. py:function:: cs2_ssl_csrs_get(commonname=None)

   :param commonname: Commonname for CSR
   :type commonname: string
   
   :rtype: dict
   :returns: :doc:`SSL CSR Records </cs2/db-structure/cs2-ssl-csrs>`
   
.. py:function:: cs2_ssl_csrs_create(commonname=None,keyname=None,passphrase=None,digest="sha1",subjects=None)

   :param commonname: Commonname for CSR
   :type commonname: string
   
   :param keyname: Keyname
   :type keyname: string
    
   :param passphrase: Passphrase
   :type passphrase: string or None
   
   :param digest: Digest for CSR
   :type digest: string or None
   
   :param subjects: CSR Subjects
   :type subjects: dict 
   
   :rtype: dict
   :returns: :doc:`SSL CSR Records </cs2/db-structure/cs2-ssl-csrs>`

.. py:function:: cs2_ssl_csrs_remove(commonname=None)

   :param commonname: Commonname
   :type commonname: string
   
   :rtype: bool
   :returns: True or False
   
   
