DC² SSL Key Table Structure
===========================


Database: cs2broker

Tablename: csrs

.. code-block:: javascript

   {
      "_id":<string uuid UNIQUE>
      "commonname":<string commonname UNIQUE>
      "csr_with_key":<string keyname UNIQUE>
      "date_created":<string isoformat date>
      "time_created":<string isoformat time>
      "csr_pem":<string PEM formatted key>
   }
