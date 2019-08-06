:tocdepth: 2
:orphan:

.. _tutorial-publishing_your_napp:

####################
Publishing your NApp
####################

********
Overview
********

On this tutorial you will learn how to publish your NApp on the |napps_server|_
repository in order to share you NApp with the Kytos Community and also make
easier for you to install it on your **Kytos** instance.

The average time to go throught it is: ``5 min``

What you will need
===================

* Your |dev_env|_ already setup
* How to create a basic NApp - Refer to |Tutorial_01|_

What you will learn
===================

* How to publish your NApp on the |napps_server|
* How to install a NApp from |napps_server|

************
Introduction
************

Now that you have learned how to install the environment and how to create your
own NApp, you can publish it on the |napps_server|_. The |napps_server|_ works
similarly to the application stores for mobile operating systems, or packages
repositories for linux distributions.

The |napps_server|_ is a repository, provided by Kytos Team, used to publish
NApps packages. It can be used by anyone interested. The |napps_server|_ web
page provide several information about the published NApps.

Before proceeding to the next section of this tutorial, go to the
|napps_server_sign_up| in order to create a user for you on our
|napps_server|_. After you submit the form you will receive an email to confirm
your registration. Click on the link present on the email body and, after
seeing the confirmation message on the screnn, go to the next section.

******************
Your NApp metadata
******************

First of all, you need to create a NApp. So, let's start creating a new NApp
using your **username** (the one you have just registered).

.. code-block:: console

  $ mkdir -p ~/tutorials
  $ cd ~/tutorials
  $ kytos napps create
  --------------------------------------------------------------
  Welcome to the bootstrap process of your NApp.
  --------------------------------------------------------------
  In order to answer both the username and the napp name,
  You must follow this naming rules:
   - name starts with a letter
   - name contains only letters, numbers or underscores
   - at least three characters
  --------------------------------------------------------------

The first question is related to your **username**. The second question is the
name of your NApp, and, for now,
we will just use ``my_first_napp`` as NApp name. The third question is related
to your NApp description. Let's put some meaningful information over there.

.. code:: console

  Please, insert your NApps Server username: <username>
  Please, insert your NApp name: my_first_napp
  Please, insert a brief description for your NApp [optional]: This is my first NApp, I have built it while doing a Kytos Tutorial.

The NApps contains two important metadata files. The first one is the
**kytos.json**, that will be used by the uploader. The second one is the
**README.rst**. It is pretty important that you take some time on them since
this information will be used by other users to find your NApp.

We are going to start with the **kytos.json** file.

kytos.json
==========

The **kytos.json** file contains the fields *username*, *name* (NApp name),
*description*, *version*, *napp_dependencies*, *license*,
*url* and *tags*. Some of these fields are mandatory, such as **username**,
**name** and **license**, while other aren't, despite them being as important
as the mandatory ones. They also accept different values.

- **username**: String with the username of the NApp creator. While uploading your
  NApp this field must match your username on the napps server.

- **name**: String with the name of the NApp.

- **description**: String with a small description of the NApp. One or two
  sentences.

- **version**: String with the version of your NApp. We suggest you to use the
  `Semantic Versioning <http://semver.org/>`_.

- **napp_dependencies**: A list of other NApps that are required by your NApp,
  on the form ``["<username>/<name>", "<other_username>/<other_name>", ...]``

- **license**: The license of your NApp (*GPL*, *MIT*, *APACHE*, etc).

- **url**: If your NApp source code is maintained on a public repository, here
  comes its url.

- **tags**: A list of tags to help catalog your NApp on the |napps_server|_ on
  the form ``["tag1", "tag2", ...]``

So, here is the **kytos.json** that we have initially generated.

.. code-block:: json

  {
    "username": "<username>",
    "name": "my_first_napp",
    "description": "This is my first NApp, I have built it while doing a Kytos Tutorial.",
    "version": "",
    "napp_dependencies": [],
    "license": "",
    "tags": [],
    "url": ""
  }

And here are an example of how we can complete this file:

.. code-block:: json

  {
    "username": "<username>",
    "name": "my_first_napp",
    "description": "This is my first NApp, I have built it while doing a Kytos Tutorial.",
    "version": "0.0.1",
    "napp_dependencies": [],
    "license": "MIT",
    "tags": ["experimental", "tutorial", "trial"],
    "url": "https://github.com/"
  }

README.rst
==========

Among other things, the **README.rst** will be presented as the main content of
the NApp page on the NApps Server (https://napps.kytos.io/<username>/<name>).

We recommend two initial sections, **Overview** and **Requirements**. The first
will contain a more complete description of your NApp, while the latter will
hold any non-NApp requirement of your NApp.

.. code-block:: rst

    Overview
    ========
    This is my first NApp, I have built it while doing the Kytos Tutorial on
    how to upload a NApp.

    This NApp, for now, is just a 'mock' NApp that does nothing. May be, on the
    future, I'll play with it while doing some more tests on how NApps work.

    Requirements
    ============
    For now this NApp does not have any external requirement beyond *Kytos*
    itself.

******************
Uploading the NApp
******************

Your NApp is now ready to be uploaded. 
Before that, if you do not want to send some files to the server, add them to .gitignore.
To upload your Napp, use the following command:

.. code-block:: console

  $ cd ~/tutorials/<username>/my_first_napp
  $ kytos napps upload
  Enter the username: <username>
  Enter the password for <username>: <password>
  SUCCESS: NApp <username>/my_first_napp uploaded.

You must fill **username** and **password** with the values you used to
register your user on the |napps_server|_.

Your NApp is now uploaded. You can see it on the web
(`<https://napps.kytos.io/<username>/my_first_napp`) or search for it through
the command line with the following command:

.. code-block:: bash

  $ kytos napps search <username>/my_first_napp

  Status |       NApp ID            |                     Description
  =======+==========================+====================================================
   [--]  | <username>/my_first_napp | This is my first NApp. I've built it as an examp...


  Status: (i)nstalled, (e)nabled

************************************
Search for and Install a remote NApp
************************************

Now that you have published your NApp, you can install it by using the command
``kytos napps install <username>/my_first_napp``.

You can also look for other NApps published on the |napps_server|_, by using
the command ``kytos napps search`` followed by some keyword to match against
the username, NApp name, description or tags.

.. code-block:: bash

  $ kytos napps search kytos

  Status |          NApp ID          |                     Description
  =======+===========================+======================================================
   [i-]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for...
   [i-]  | kytos/flow_manager        | Manage switches' flows through a REST API.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swi...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using ...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/topology            | Keeps track of links between hosts and switches. R...

  Status: (i)nstalled, (e)nabled

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. include:: ../back_to_list.rst

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |napps_server_sign_up| replace:: **sign_up**
.. _napps_server_sign_up: https://napps.kytos.io/signup/

.. |mininet| replace:: *Mininet*
.. _mininet:  http://mininet.org/overview/
