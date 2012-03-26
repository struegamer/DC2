DC² SSL Key Table Structure
===========================


Database: cs2broker

Tablename: keys

.. code-block:: javascript

   {
      "_id":<string uuid UNIQUE>
      "keyname":<string keyname UNIQUE>
      "description":<string description>
      "date_created":<string isoformat date>
      "time_created":<string isoformat time>
      "key_pem":<string PEM formatted key>
   }
