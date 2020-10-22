Installing
==========

In order to use this software please install python version 3.6 or 
greater into your environment beforehand.

We are doing a huge effort to make Kytos and its components available on all
common distros. So, we recommend you to download it from your distro
repository.

But if you are trying to test, develop or just want a more recent version of
our software no problem: Download now, the latest release (it still a beta
software), from our repository:

First you need to clone *kytos* repository:

.. code-block:: shell

   $ git clone https://github.com/kytos/kytos.git

After cloning, the installation process is done by standard `setuptools`
install procedure:

.. code-block:: shell

   $ cd kytos
   $ sudo python3 setup.py install

Configuring
===========

After *kytos* installation, all config files will be located at
``/etc/kytos/``.

*Kytos* also accepts a configuration file as argument to change its default
behaviour. You can view and modify the main config file at
``/etc/kytos/kytos.conf``.

For more information about the config options please visit the `Kytos's
Administrator Guide
<https://docs.kytos.io/kytos/administrator/#configuration>`__.
