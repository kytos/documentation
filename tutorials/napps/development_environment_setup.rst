:tocdepth: 2
:orphan:

.. _tutorial-setup-the-development-environment:

###############################
Setting up your dev environment
###############################

.. NOTE:: We tested this tutorial on Ubuntu, but feel free to adapt to your
  preferred Linux distribution.

********
Overview
********

This tutorial shows how to setup your development environment in order to run
the latest Kytos SDN Platform code (python-openflow, kytos, kytos NApps, ...) and
contribute to it.

.. DANGER:: Do not use this procedure in production environments.
   This setup is for development only.

.. CAUTION:: Code to be run in terminal begins with the dollar sign ($). If
  you copy and paste, don't forget to skip this symbol.

The average time to go through it is: ``10 min``.

What you will learn
===================

* How to create an isolated environment for development;
* How to install the Kytos Projects in a development environment;
* How to install Mininet.

********************************
Installing required dependencies
********************************

In order to start using and coding with Kytos, you need a few required
dependencies. One of them is Python 3.6. Note that an additional step is
needed for Ubuntu releases older than 16.10.

Python3.6 in old Ubuntu releases
================================

If are you using Ubuntu 16.04 or older, you must add a PPA to be able to
install Python 3.6 packages. To add this PPA, use the commands:

.. code-block:: bash

  $ sudo add-apt-repository ppa:jonathonf/python-3.6
  $ sudo apt update

Required packages
=================

The required Ubuntu packages can be installed by:

.. code-block:: bash

  $ sudo apt install git libpython3.6-dev python3.6 python3.6-venv

********************************
Setting up a virtual environment
********************************

First of all, to make changes to Kytos projects, we recommend you to use
|venv|_. The main reason for this recommendation is to keep the dependencies
required by different projects in separate places by creating virtual Python
environments for each one. It solves the “Project X depends on version 1.x, but
Project Y needs 4.x” dilemma, and keeps your global site-packages directory
clean and manageable.

In this tutorial, we will use the new built-in :mod:`venv` Python module,
but if you wish to use another tool to create isolated environments or install
libraries on your global system, feel free to do it your way.

Creating a new virtualenv
=========================

To create a new virtualenv, use the command below (you can replace ``test42``
by another name, if you wish):

.. code-block:: bash

   $ python3.6 -m venv test42

This command will create a virtualenv named *test42* and a folder with the same
name for it.
This environment will use 3.6 as the default Python version.

.. NOTE:: Kytos is using Python 3.6 to leverage some new features of the Python
  language.

Removing a virtualenv
---------------------

If you want to remove an existing virtualenv, just delete its folder
(e.g. ``rm -rf test42``).

Using the virtual environment
=============================

If you want to use an existing environment you can use the following command:

.. code-block:: bash

  $ source test42/bin/activate

After that, your console prompt will show the activated virtualenv name between
parenthesis. Now, update the *pip* package that is already installed in the
virtualenv, with setuptools and wheel as well:

.. code-block:: bash

  (test42) $ pip install --upgrade pip setuptools wheel

The parenthesis marker identifies that the test42 virtualenv is activated. If
you want leave this virtualenv you can use the command ``deactivate``.
After this, the virtualenv name will disappear from your prompt and you will be
using your regular Ubuntu environment.

.. note:: Inside the virtualenv, all pip packages will be installed within the
   *test42* folder. Outside the virtualenv, all pip packages will be installed
   into the default system environment (standard Ubuntu folder).

If you want to read more about it, please visit: |virtualenv|_ and
|virtualenv_docs|_ pages.

***********************************
Installing the latest Kytos release
***********************************

Installing from Source
======================

To install the latest Kytos from source, first you need to start your environment:

.. code-block:: bash

  $ source YOURENV/bin/activate

Then you need to run the commands below to clone the python-openflow, kytos-utils and kytos projects locally. 

.. code-block:: shell

  for repo in python-openflow kytos-utils kytos; do
    git clone https://github.com/kytos/${repo}
  done

After cloning, the Kytos installation process is done running setuptools installation procedure for each cloned repository, in order. Below we execute its commands.

.. code-block:: shell

    for repo in python-openflow kytos-utils kytos; do
      cd ${repo}
      python3 setup.py develop
      cd ..
    done

Installing the NApps from Kytos team
====================================

We will now install some NApps developed by the Kytos team, which will be used
later in the following tutorials. To enable NApps management, we need Kytos
running, so open another terminal window, make sure your virtualenv is active
and run:

.. code-block:: bash

  $ source test42/bin/activate
  $ kytosd -f

.. NOTE:: Don't worry about the Kytos main screen for now: we will have it
    explained, as well as NApp management, in the next tutorials.

Now that Kytos is running, switch back to the previous window and install the
NApps using the ``kytos`` command line utility. You will also disable the NApps,
just for now.

.. code-block:: bash

  $ kytos napps install kytos/of_core \
     kytos/flow_manager \
     kytos/of_l2ls \
     kytos/of_lldp \
     kytos/topology

  $ kytos napps disable all

That's it! Now, you can go back to the Kytos screen and type ``quit`` to exit
Kytos.
One more step: Mininet.

How to install Mininet
======================

Mininet is a network simulator that creates a network of virtual hosts,
switches, controller and the links among them. Mininet hosts run standard Linux
network software, and its switches support Openflow for highly flexible custom
routing and Software Defined Networking.

First, we need to install the mininet package. The `Mininet project
<http://mininet.org/>`_ lists a few methods for installing the simulator. For
instance, you can use a virtual machine or you can install it to you operating
system.

.. code-block:: bash

  $ sudo apt install mininet

To test if the mininet is working for you, run the command:

.. code-block:: console

  $ sudo mn --test pingall
  *** No default OpenFlow controller found for default switch!
  *** Falling back to OVS Bridge
  *** Creating network
  *** Adding controller
  *** Adding hosts:
  h1 h2
  *** Adding switches:
  s1
  *** Adding links:
  (h1, s1) (h2, s1)
  *** Configuring hosts
  h1 h2
  *** Starting controller

  *** Starting 1 switches
  s1 ...
  *** Waiting for switches to connect
  s1
  *** Ping: testing ping reachability
  h1 -> h2
  h2 -> h1
  *** Results: 0% dropped (2/2 received)
  *** Stopping 0 controllers

  *** Stopping 2 links
  ..
  *** Stopping 1 switches
  s1
  *** Stopping 2 hosts
  h1 h2
  *** Done
  completed in 0.154 seconds

To see more about Mininet, you can access the webpage `mininet.org
<http://mininet.org/walkthrough/>`_.

.. include:: ../back_to_list.rst

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |venv| replace:: *Virtual Environments*
.. _venv: https://en.wikipedia.org/wiki/Virtual_environment_software

.. |virtualenv| replace:: **virtualenv**
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. |virtualenv_docs| replace:: **virtualenv docs**
.. _virtualenv_docs: https://virtualenv.pypa.io/en/stable/
