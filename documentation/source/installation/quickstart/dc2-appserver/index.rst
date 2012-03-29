DC² Application Server Installation
===================================

When you installed the **dc2-server** package, there is also the **dc2-appserver** package installed on your system.

This Application server is a `WSGI <http://www.wsgi.org>`_ application running under Apache2 with `mod_wsgi <http://code.google.com/p/modwsgi/>`_.

Let's take some steps to configure this application server.

Apache Configuration
--------------------

With the **dc2-appserver** package a new file under **/etc/apache2/sites-available/** will be installed.
The file with the name "**/etc/apache2/sites-available/dc2db.hosts**" needs to be adjusted.

This is the original contents of the file:

.. code-block:: apacheconf
   :linenos:
   
   <VirtualHost _default_:80>
           ServerAdmin root@localhost
           ServerName dc2db
           WSGIScriptAlias / /usr/share/dc2-appserver/dc2db_new.py
           WSGIDaemonProcess dc2-ng user=www-data group=www-data processes=5 threads=10 display-name=dc2-ng
           WSGIProcessGroup dc2-ng
   </VirtualHost>

   <VirtualHost _default_:80>
           ServerAdmin root@localhost
           DocumentRoot /srv/tftp/fai/
   </VirtualHost>

You have to replace the following lines:

1. **Line 01**: Replace the value "**__default__:80**" with "**192.168.100.100:80**"
2. **Line 09**: Replace the value "**__default__:80**" with "**192.168.1001.101:80**"
3. **Line 11**: Add a new line with the contents "ServerName download"

The resulting file should look like this:

.. code-block:: apacheconf
   :linenos:

   <VirtualHost 192.168.100.100:80>
           ServerAdmin root@localhost
           ServerName dc2db
           WSGIScriptAlias / /usr/share/dc2-appserver/dc2db_new.py
           WSGIDaemonProcess dc2-ng user=www-data group=www-data processes=5 threads=10 display-name=dc2-ng
           WSGIProcessGroup dc2-ng
   </VirtualHost>

   <VirtualHost 192.168.100.101:80>
           ServerAdmin root@localhost
           DocumentRoot /srv/tftp/fai/
           ServerName download
   </VirtualHost>
        
When you changed the file, execute

.. code-block:: bash
   :linenos:

   user@home: ~> sudo a2ensite dc2db.hosts

This command will symlink the file from sites-available to sites-enabled, so with your next start you should access http://download/ without a problem.


DC² Application Server configuration
------------------------------------

As you could read in the **/etc/apache2/sites-available/dc2db.hosts** file, the real WSGI application is installed under **/usr/share/dc2-appserver/**.
In this directory, there is also the configuration file for the DC² Application Server located, named "**settings.py**".

Let's take a look at some options you can adjust or need to.

MongoDB Configuration
^^^^^^^^^^^^^^^^^^^^^


.. code-block:: python
   :linenos:

   # 
   # MongoDB Server and Database Collections
   #

   MONGOS = {
               "dc2db": {
                   "host":"localhost",
                   "port":27017,
                   "dbname":"dc2db",
                   "database":None
               },
               "cs2db": {
                   "host":"localhost",
                   "port":27017,
                   "dbname":"cs2db",
                   "database":None
               },
               "xendb": {
                   "host":"localhost",
                   "port":27017,
                   "dbname":"xendb",
                   "database":None
                },
                "userdb": {
                   "host":"localhost",
                   "port":27017,
                   "dbname":"userdb",
                   "database":None
                }
   }
   

This is a standard python dictionary. The "root" keys of the *MONGOS* dict are used to address the mongodb instance in the DC² Applications.
The keys in the default MONGOS dict are hard set. If you are going to rename them, you need to change the names as well in the DC² Application Server code.
Therefore, the following keynames should not be changed:

* dc2db
* cs2db
* xendb
* userdb

The values of the keys are as well a python dict.
The keys of this dict are:

**host** (mandatory)
     The hostname of the MongoDB instance you want to put the database

**port** (mandatory)
     The default port of your MongoDB (Default: **27017**)

**dbname** (mandatory)
     The name of the database (collection) in your MongoDB

**database** (optional)
     This will be used for holding the database instance when the application is connecting to the MongoDB instance.


CORS Configuration
^^^^^^^^^^^^^^^^^^

CORS is an abbreviation for `Cross-Origin Resource Sharing <http://www.w3.org/TR/cors/>`_ and these settings are needed when you want to use 
the DC² Web Frontend Application.

The default settings shown below, we won't change them for now.

.. code-block:: python
   :linenos:

   #
   # HTTP Access Headers
   #
   ACCESS_CONTROL_ALLOW_ORIGIN="*"
   ACCESS_CONTROL_ALLOW_METHODS="GET,POST,OPTIONS,PUT,DELETE"


RPC Modules
^^^^^^^^^^^

The DC² Application Server is handling RPC calls in the known formats of `XMLRPC <http://xmlrpc.scripting.com/>`_ and `JSON-RPC <http://json-rpc.org/>`_.
All RPC methods are written in `Python <http://www.python.org/>`_ and stored in Python Modules.

There are several modules supported by DC²:

1. DC² Standard RPC Methods
2. CS² RPC Methods
3. XEN RPC Methods

If you want to add another addon RPC module  you need to enable it here:

.. code-block:: python
   :linenos:

   #
   # RPC Modules for RPCDispatcher
   #
   CS2_ENABLED=False
   XEN_ENABLED=False

   RPCMODULES = ['dc2.appserver.rpcmethods']
   if CS2_ENABLED:
       RPCMODULES.append('cs2.rpcmethods')
   if XEN_ENABLED:
      pass

A documentation for adding more modules is **TBD**


DC² PXE Configuration Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DC² application server needs some informations about IPs and hostnames to give it back to the clients during PXE boot.

.. code-block:: python
   :linenos:

   # 
   # DC² Settings for PXE Boot
   #
   DOWNLOAD_SERVER_URL="http://172.20.0.101/"
   XMLRPC_BACKEND_SERVER_URL="http://dc2db.net/RPC"
   XMLRPC_BACKEND_SERVER_IP="172.20.0.100"

**DOWNLOAD_SERVER_URL**
   This will be set to the download vhost.
   In this quickstart example this will be "**http://192.168.100.101/**"

**XMLRPC_BACKEND_SERVER_URL**
   This will be the URL to the DC² Application Server
   In this quickstart example this will be "**http://dc2db/RPC**"

**XMLRPC_BACKEND_SERVER_IP**
   This needs to set to the IP address of the DC² Application Server, some clients don't do nameserver resolving very good, so we will
   fallback to HTTP/1.0.
   In this quickstart this will be set to "**192.168.100.100**"


Last Steps
^^^^^^^^^^

There is one last step we need to do. The logfile of the DC² Application Server will be written to "**/var/log/dc2**".
This needs to be created manually. Just execute:

.. code-block:: bash
   :linenos:

   user@home: ~> sudo mkdir -p /var/log/dc2
   user@home: ~> sudo chown www-data:www-data /var/log/dc2


