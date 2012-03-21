DC² DefaultClasses Table Structure
==================================


Database: dc2db

Tablename: environments

.. code-block:: javascript

   {
      "_id":<string uuid UNIQUE>
      "name":"<string name of the environment>",
      "description":"<string description>,
      "variables":[
         {  "name":"<string variable name>",
            "value":<string value of variable>"
         },
         ...
         ]
   }
