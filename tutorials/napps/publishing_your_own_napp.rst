:tocdepth: 2
:orphan:

.. _tutorial-publishing_your_own_napp:

########################
Publishing your own Napp
########################

********
Overview
********

For this tutorial you will learn how to describe better about your NApp and
who to store this using the |napps_server|_ repository. After this you will
upload, install and uninstall you NApp published.

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will need
===================

* Your |dev_env|_ already setup
* How to create a basic NApp - Refer to |Tutorial_01|_

What you will learn
===================

* How to provide informations your own NApp
* How upload your NApp
* How to install a NApp from |napps_server|

************
Introduction
************

Now that you have learned how to install the environment and how to create your
own Napp you can publish that using the |napps_server|_.

|napps_server|_ is a repository used to store NApps package,that can be used to
everyone interested. The |napps_server|_ web page provide several informations
about the NApps stored. Before follow the step used by this tutorial you must
|napps_server_sign_up| using the |napps_server|_ web page.

*****************************************
How to provide informations your own NApp
*****************************************

First of all, you must create a NApp.So, let's start creating a new NApp using
your **username**.

.. code-block:: bash

  $ mkdir ~/tutorials
  $ cd ~/tutorials
  $ kytos napps create
  --------------------------------------------------------------
  Welcome to the bootstrap process of your NApp.
  --------------------------------------------------------------
  In order to answer both the author name and the napp name,
  You must follow this naming rules:
   - name starts with a letter
   - name contains only letters, numbers or underscores
   - at least three characters
  --------------------------------------------------------------

The first question is related to your author name, let's answer with
your **username** for now:

.. code:: bash

  Please, insert your NApps Server username: <username>

Then, you will insert the NApp name (**published_napp**):

.. code:: bash

  Please, insert you NApp name: published_napp

If you want upload your Napp to |napps_server|_ you must edit the **kytos.json**
and **README.rst**. These files are used by |napps_server| to show the main
informations about you NApp.

Kytos.json
==========

Inside the **kytos.json** we have a json with the fields *author*, *name*,
*description*, *long_description*, *version*, *napp_dependencies*,
*license*, *url* and *tags*.All these fields are metadata used by
|napps_server|_ or the ``kytos-utils`` tools. After built the NApp
tutoral/published_napp as shown above, you must edit the file changing the
default values.

.. code-block:: json

  {
    "author": "tutorial",
    "name": "published_napp",
    "description": "# TODO: <<<< Insert here your NApp description >>>>",
    "long_description": "",
    "version": "",
    "napp_dependencies": [],
    "license": "",
    "tags": [],
    "url": ""
  }

- *author*: is a metadata used by |napps_server|_ to identify the author of a Napp, *Only* the author used in this field can upload that Napp.
- *name*: is a metadata used by |napps_server|_ to identify the Napp name.
- *description*: is a metadata used to show a short description about the Napp.
- *long_description*: is a metadata used to show a long description about the Napp.
- *version*: is a metadata to identify the version of your NApp.
- *license*: is a metadata used to describe the license about your NApp, for instance if you have a MIT license you must to use "MIT".
- *tags*: is a metadata used to create tags by |napps_server|_, for instance if your NApps is in an experimental, you should to use the tag *Experimental*.
- *url*: is a metadata to store the url where there is the source code of your NApp.

For this tutorial you must fill in the fields like this:

.. code-block:: json

  {
    "author": "<username>",
    "name": "published_napp",
    "description": "Short description about my published Napp",
    "long_description": "Long description about my published NApp.",
    "version": "0.0.1",
    "napp_dependencies": ["kytos/of_core"],
    "license": "MIT",
    "tags": ["Experimental", "published"],
    "url": "https://github.com"
  }

README.rst
==========

**README.rst** is used to store more informations about your NApp. By default,
after created this file will be filled with:

.. code-block:: rst

    Overview
    ========
    # TODO: <<<< Insert here your NApp description >>>>

    Requirements
    ============

You must edit this file using the description below:

.. code-block:: rst

    Overview
    ========

    This Napp is a example of how to publish a simple NApp.

    Requirements
    ============

    * python3.6
    * python3-openflow
    * kytos-utils

    How to install My Published NApp.
    =================================

    To install this napp you must to use the command below, provided by
    kytos-utils.

    .. code-block:: bash

    $ kytos napps install <username>/published_napp

********************
How upload your NApp
********************

Now that your NApp is ready to be uploaded, you must to use ``kytos-utils``
command.

.. code-block:: bash

  $ kytos napps upload <username>/published_napp

Or if you current directory has a kytos.json you can use:

.. code-block:: bash

  $ kytos napps upload
  Enter the username: <username>
  Enter the password for <username>: <password>
  SUCCESS: NApp <username>/published_napp uploaded.

You must fill the **username** and **password** registered using the
|napps_server|_ web page. After that your Napp is uploaded and you can find
that using the command below or acessing |napps_server|_  web page.

.. code-block:: bash

  $ kytos napps search "<username>/published"

  Status |       NApp ID        |                     Description
  =======+======================+====================================================
   [--]  | <username>/published | Short description about my published Napp

  Status: (i)nstalled, (e)nabled


If you want search all napps stored by |napps_server|_ you should to use:

.. code-block:: bash

  $ kytos napps search ""
  Status |          NApp ID          |                   Description
  =======+===========================+================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsib...
   [--]  | kytos/of_flow-manager     | NApp that manages switches flows.
   [i-]  | kytos/of_flow_manager     | NApp that manages switches flows.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all sw...
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFl...
   [i-]  | kytos/of_l2lsloop         | A L2 learning switch application for openflo...
   [i-]  | kytos/of_lldp             | App responsible by send packet with lldp pro...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | A simple app that update links between machi...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interfac...
   [--]  | <username>/published_napp | Short description about my published Napp

  Status: (i)nstalled, (e)nabled

*****************************************
How to install a NApp from |napps_server|
*****************************************

Now that you published you first Napp, you must install them.To do this is very
simple, using the command provide by ``kytos-utils``.You can download the Napp
from |napps_server|_ and install this.

.. code-block:: bash

  $kytos napps install <username>/published_napp
  INFO  NApp <username>/published_napp:
  INFO    Searching local NApp...
  INFO    Installed.
  INFO    Enabling...
  INFO    Enabled.

Now if you list all NApps uploaded the output below will be displayed:

.. code-block:: bash

  $ kytos napps search ""
  Status |          NApp ID          |                   Description
  =======+===========================+================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsib...
   [--]  | kytos/of_flow-manager     | NApp that manages switches flows.
   [i-]  | kytos/of_flow_manager     | NApp that manages switches flows.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all sw...
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFl...
   [i-]  | kytos/of_l2lsloop         | A L2 learning switch application for openflo...
   [i-]  | kytos/of_lldp             | App responsible by send packet with lldp pro...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | A simple app that update links between machi...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interfac...
   [ie]  | <username>/published_napp | Short description about my published Napp

  Status: (i)nstalled, (e)nabled


If you want uninstall a Napp you must to use the command below.

.. code-block:: bash

  $ kytos napps uninstall <username>/published_napp
  INFO  NApp <username>/published_napp:
  INFO    Uninstalling...
  INFO    Disabled.
  INFO    Uninstalled.

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. include:: ../back_to_list.rst

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |napps_server_sign_up| replace:: **sign_up**
.. _napps_server_sing_up: https://napps.kytos.io/signup/

.. |mininet| replace:: *Mininet*
.. _mininet:  http://mininet.org/overview/
