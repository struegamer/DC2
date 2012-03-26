DC² SSL Key Table Structure
===========================


Database: cs2broker

Tablename: crls

.. code-block:: javascript

   {
      "_id":<string uuid UNIQUE>
      "ca_name":<string ca_name UNIQUE>
      "date_created":<string isoformat date>
      "time_created":<string isoformat time>
      "crl_pem":<string PEM formatted>
   }
