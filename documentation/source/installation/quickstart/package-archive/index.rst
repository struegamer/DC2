Package Archive
===============

Debian Package Archives
-----------------------

You may know about the tools mirroring a Debian Package Archive. But some people do not.
When you are one of the latter this documentation will help you to get started.

Installation of DC² Distrotools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you added the DC² Personal Package Archive you are ready to install the DC² Distrotools. Just execute::

     user@home: ~> sudo apt-get install dc2-distrotools

After this is finished, you will find a new tool: **dc2-mirror**.

To use dc2-mirror, we need to create a configuration file. An example you can find under **/usr/share/doc/dc2-distrotools/**. 
To get things starting we are creating now a Ubuntu package mirror of Ubuntu 11.10.

Start your favorite editor and create a file named **.dc2-mirror.yaml** in your home directory with the following contents:

.. code-block:: yaml
   :linenos:

     config:
       mirror_directory: /srv/archive
     distributions:
       ubuntu:
         defaults:
           sections: main,restricted
           arch: amd64
           host: archive.ubuntu.com
           rootdir: ubuntu
           stable: true
           method: http
         releases:
           oneiric:
             sections: main,restricted,universe,multiverse
             arch: amd64,i386
             host: archive.ubuntu.com
             rootdir: ubuntu
             stable: true
             method: http
             mirror_directory: /srv/archive/oneiric


The contents of the .dc2-mirror.yaml file means:

1. your default archive mirror path is **/srv/archive**
2. you want to mirror an ubuntu archive
3. for ubuntu there is a default section which defines some values which will be used when there is not a more specific value.
4. you want to mirror the Ubuntu release 11.10 which nickname is "Oneiric Ocelot" and the distro name of this release is "oneiric".
5. you want to mirror the sections: main, restricted, universe, multiverse
6. you want to mirror the two default supported archs: amd64, i386
7. you want to mirror from the main archive site of Ubuntu: archive.ubuntu.com
8. the root dir to the real files is: ubuntu
9. you are mirroring a stable release, which includes also the pockets: oneiric-updates and oneiric-security
10. you are mirroring with the http client method
11. and your destination path where you want to store all files: **/srv/archive/oneiric**

So, we need to create the directory where the archive will be stored, to do this just fire these commands [#f1]_ ::

     user@home: ~> sudo mkdir -p /srv/archive/oneiric
     user@home: ~> sudo chown -Rvf user:user /srv/archive/oneiric

Now you can fire up dc2-mirror and grab a coffee or two or just configure your webserver to serve your archive later on.

The time for finishing the mirror task can be between minutes or hours, depending on your line speed and bandwidth. Mostly the archive size will be round about 70GB of space.

This list is my local mirror archive, so you can determine at least what you need later on for capacity planning of your storage device::

     /dev/mapper/archive-repository_lucid            70G   62G  8.2G  89% /srv/archive/lucid
     /dev/mapper/archive-repository_oneiric          70G   66G  4.6G  94% /srv/archive/oneiric
     /dev/mapper/archive-repository_precise          70G   61G  9.3G  87% /srv/archive/precise
     /dev/mapper/archive-repository_debian_squeeze   70G   52G   19G  75% /srv/archive/debian/squeeze

As you can see, I'm using LVM for storing the archive. This has some advantages to separate the distro archives, you can clean up easier later on, when for example one release is End Of Life. More on archive management later.

Webserver Configuration
^^^^^^^^^^^^^^^^^^^^^^^

While you grabbed a coffee and eventually you are still waiting for the mirror to finish downloading, we can go on to configure the needed webserver, which serves your archive during deployment.

When you installed the "dc2-server" package an Apache HTTP Version 2.x server should be installed by default. It is also configured for the usual "It Works!" page.
**Let's change it.**

The configuration for the apache httpd on a Debian based system you'll find under **/etc/apache2**. Let's create a new virtual host configuration file, to get the archive running.

Start your editor and create a file with the name: **/etc/apache2/sites-available/archive.vhost**.

When you followed the introduction, we will use the IP from the host (eth1) which is **192.168.100.10** and we will use as hostname (how obvious) "archive".

So use the contents below to add it to your created file:

.. code-block:: apacheconf
   :linenos:

     <VirtualHost 192.168.100.10:80>
        ServerAdmin user@archive
        ServerName archive
        DocumentRoot /srv/archive/
     </VirtualHost>

Now we need to add a NameVirtualHost statement. This will be done in the file **/etc/apache2/ports.conf**.

So, the default **/etc/apache2/ports.conf** looks like this:

.. code-block:: apacheconf
   :linenos:

     # If you just change the port or add more ports here, you will likely also
     # have to change the VirtualHost statement in
     # /etc/apache2/sites-enabled/000-default
     # This is also true if you have upgraded from before 2.2.9-3 (i.e. from
     # Debian etch). See /usr/share/doc/apache2.2-common/NEWS.Debian.gz and
     # README.Debian.gz

     NameVirtualHost *:80

     Listen 80

     <IfModule mod_ssl.c>
        # If you add NameVirtualHost *:443 here, you will also have to change
        # the VirtualHost statement in /etc/apache2/sites-available/default-ssl
        # to <VirtualHost *:443>
        # Server Name Indication for SSL named virtual hosts is currently not
        # supported by MSIE on Windows XP.
        Listen 443
     </IfModule>

     <IfModule mod_gnutls.c>
        Listen 443
     </IfModule>

The changed **ports.conf** file has to look like this:

.. code-block:: apacheconf
   :linenos:

     # If you just change the port or add more ports here, you will likely also
     # have to change the VirtualHost statement in
     # /etc/apache2/sites-enabled/000-default
     # This is also true if you have upgraded from before 2.2.9-3 (i.e. from
     # Debian etch). See /usr/share/doc/apache2.2-common/NEWS.Debian.gz and
     # README.Debian.gz

     NameVirtualHost *:80
     NameVirtualHost 192.168.100.10:80

     Listen 80

     <IfModule mod_ssl.c>
        # If you add NameVirtualHost *:443 here, you will also have to change
        # the VirtualHost statement in /etc/apache2/sites-available/default-ssl
        # to <VirtualHost *:443>
        # Server Name Indication for SSL named virtual hosts is currently not
        # supported by MSIE on Windows XP.
        Listen 443
     </IfModule>

     <IfModule mod_gnutls.c>
        Listen 443
     </IfModule>


After you changed the **ports.conf** file you have to enable this vhost. To do this you execute this command::

     user@home: ~> sudo a2ensite archive.vhost

Furthermore, we disable the default site which was installed by the Ubuntu Apache httpd package::

     user@home: ~> sudo a2dissite default
     user@home: ~> sudo a2dissite default-ssl

Now you can restart your webserver, and you should see an index page with the contents of the archive. Eventually you have to adjust your hosts file of your workstation, but this is a task I'll leave to you.


.. rubric:: Footnotes

.. [#f1] Please replace "user" with your real userid
