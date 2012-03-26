CS² SSL Key Table Structure
===========================


Database: cs2broker

Tablename: certs

.. code-block:: javascript

   {
      "_id":<string uuid UNIQUE>
      "commonname":<string commonname UNIQUE>
      "date_created":<string isoformat date>
      "time_created":<string isoformat time>
      "cert_pem":<string PEM formatted key>
   }
