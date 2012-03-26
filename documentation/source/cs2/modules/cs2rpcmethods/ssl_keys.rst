SSL Key Methods
===============

.. py:module:: cs2rpcmethods


Global Data
-----------

.. py:data:: tbl_keys

Module Methods
--------------

.. py:function:: cs2_ssl_keys_list()

   Returns a list of SSL Key Entries

   :rtype: list of dict 
   :returns: list of type :doc:`SSL Key Record </cs2/db-structure/cs2-ssl-keys>`

.. py:function:: cs2_ssl_keys_get(keyname=None)

   Returns the SSL key with keyname

   :param keyname: string 

   :rtype: dict
   :returns: :doc:`SSL Key Record </cs2/db-structure/cs2-ssl-keys>`

.. py:function:: cs2_ssl_keys_create(keyname=None, description=None, key_type=TYPE_DSA, key_bits=2048, cipher="des3", passphrase=None)

   Creates an SSL key and persists in the Database.

   :param keyname: Name of Key in Database 
   :type keyname: string
   :param description: Description
   :type description: string | None
   :param key_type: Type of key
   :type key_type: TYPE_DSA | TYPE_RSA
   :param key_bits: Number of Bits of Key
   :type key_bits: int
   :param cipher: Cipher of encrypted key 
   :type cipher: string des|des3|aes128|aes192|aes256|None
   :param passphrase: Passphrase of the Key
   :type passphrase: string | None

   :rtype: Dict
   :returns: :doc:`SSL Key Record </cs2/db-structure/cs2-ssl-keys>`

.. py:function:: cs2_ssl_keys_remove(keyname=None)

   Removes a SSL Key from the database

   :param keyname: Name of key in Database
   :type keyname: string 

   :rtype: bool
   :returns: Success (True) or Failed (False)

.. py:function:: cs2_ssl_keys_import(keyname=None, key_pem=None)

   Imports an existing Key in PEM format into the database
   
   :param keyname: Name of the key in Database
   :type keyname: string
   
   :param key_pem: Key PEM Buffer
   :type key_pem: string
   
   :rtype: dict
   :returns: :doc:`SSL Key Record </cs2/db-structure/cs2-ssl-keys>`
   
