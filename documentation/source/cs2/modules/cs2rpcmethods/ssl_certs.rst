SSL CERT Methods
================

.. py:module:: cs2rpcmethods



Global Data
-----------

.. py:data:: tbl_certs
.. py:data:: tbl_csrs
     :noindex:


Module Methods
--------------

.. py:function:: cs2_ssl_certs_list()

   :rtype: list of dict
   :returns: list of :doc:`SSL CERT Record </cs2/db-structure/cs2-ssl-cert>`

.. py:function:: cs2_ssl_certs_get(commonname=None)

	:param commonname: Commonname
	:type commonname: string
	
	:rtype: dict
	:returns: :doc:`SSL CERT Record </cs2/db-structure/cs2-ssl-cert>`

.. py:function:: cs2_ssl_certs_create(commonname=None,serial_no=None,digest="sha1",notBefore=0,notAfter=0)

	:param commonname: Commonname
	:type commonname: string (can't be None)
	
	:param serial_no: Serial No
	:type serial_no: int
	
	:param digest: CERT Digest Type
	:type digest: string 
	
	:param notBefore: Date as Integer of when the certificate is being valid
	:type notBefore: int
	
	:param notAfter: Date as Integer of when the certificate will expire
	:type notAfter: int
	
	:rtype: dict
	:returns: :doc:`SSL CERT Record </cs2/db-structure/cs2-ssl-cert>`

.. py:function:: cs2_ssl_certs_import(commonname=None,cert_pem=None)

   :param commonname: Commonname
   :type commonname: string
   
   :param cert_pem: CERT Buffer in PEM Format
   :type cert_pem: string
   
   :rtype: dict
   :returns: :doc:`SSL CERT Record </cs2/db-structure/cs2-ssl-cert>`