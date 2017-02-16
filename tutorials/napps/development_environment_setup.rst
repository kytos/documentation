:tocdepth: 2
:orphan:

.. _tutorial-setup-the-development-environment:

###############################
Setting up your dev environment
###############################

.. NOTE:: We tested this tutorial on Ubuntu. But feel free to adapt to your
  preferred Linux distribution.

********
Overview
********

This tutorial shows how to setup your development environment to contribute to
Kytos Ecosystem code (python-openflow, kyco, kytos NApps and so on). With this
setup you will also be able to run the *Kytos Controller* (|kyco|_).

.. NOTE:: Do not use this method to install Kytos in production environments.
   This setup is not suitable for production.

.. CAUTION:: Code to be run in terminal begins with the dollar sign ($). If
  you copy and paste, don't forget to skip this symbol.

.. TODO:: Set the time

The average time to go through it is: XX min

What you will learn
===================

* How to create an isolated environment for development
* How to install the Kytos Projects in a development environment
* How to install Mininet

********************************
Installing required dependencies
********************************

In order to start using and coding with Kytos, you need a few required
dependencies. One of them is Python 3.6 and it has a special procedure for
Ubuntu older than 16.10.

Python3.6 in old Ubuntu releases
================================

If are you using Ubuntu older than 16.10, you must add a PPA to be able to
install Python 3.6 packages. To add this PPA use the command:

.. code-block:: bash

  $ sudo add-apt-repository ppa:jonathonf/python-3.6
  $ sudo apt-get update


Required packages
=================

The required Ubuntu packages can be installed by:

.. code-block:: bash

  $ sudo apt-get install git rrdtool librrd-dev libpython3.6-dev python3.6


********************
Virtual Environments
********************

First of all, to make changes to Kytos projects we recommend you to use |venv|_.
The main reason for this recommendation is to keep the dependencies required by
different projects in separate places by creating virtual Python environments
for each one. It solves the “Project X depends on version 1.x, but Project Y
needs 4.x” dilemma, and keeps your global site-packages directory clean and
manageable.

In this tutorial we will use the |virtualenv|_ package, but if you are used to
use another tool to create isolated environments or to install every library on
your global system, feel free to do it your way.

********************************
Setting up a virtual environment
********************************

To setup an isolated environment, we need to install virtualenv. Virtualenv is a
tool used to build an isolated environment. In the following sections you will
learn how to create and manage virtualenvs.

.. code-block:: bash

  $ sudo apt-get install python3.6-venv

Configuring Virtualenv
======================

Creating a new virtualenv
-------------------------

If you want create a new virtualenv, you must use the command below:

.. code-block:: bash

   $ python3.6 -m venv test42

This command will create a virtualenv named *test42* and to use the
python3.6 as a default python into the environment.

.. NOTE:: Kytos is using python3.6 to leverage some new features of the Python
  language.

Removing a virtualenv
---------------------

If you want to remove an existing virtualenv, just delete its folder:

.. code-block:: bash

  $ rm -rf test42

After this the virtualenv named *test42* will be removed.

Using the virtual environment
-----------------------------

If you want to use an existing environment you can use the following command:

.. code-block:: bash

  $ source test42/bin/activate

After that, your console will show the activated virtualenv name between
parenthesis. Now, update the *pip* package that is installed in every
virtualenv:

.. code-block:: bash

  (test42) $ pip install --upgrade pip

This mean that the test42 is already activated. When you want leave this
virtualenv you can use the command below:

.. code-block:: bash

  $ deactivate

After this you will use your regular environment and the virtualenv name will
disappear from your prompt.

.. note:: Inside the virtualenv, all pip packages will be installed within the
   test42 folder. Outside the virtualenv, all pip packages will be installed
   into the default system environment (standard Ubuntu folders).

If you want to read more about it, please visit: |virtualenv|_ and
|virtualenv_docs|_ pages.


******************************
Using latest Kytos from Github
******************************


Cloning existing projects
=========================

If you want contribute with a kytos project, you must clone a project found in
`GitHub group <https://github.com/kytos>`_ to make your changes. Here we are
going to clone all important repositories (python-openflow, kyco, kytos-utils
and kyco-core-napps) using the development branch.

.. code-block:: bash

  $ for project in python-openflow kyco kyco-core-napps kytos-utils; do
      git clone --branch develop https://github.com/kytos/$project.git; \
    done

After this command, a folder will be created for each project with the latest
version of the source code.


Installing Python dependencies
==============================

Each project requires a set of Python packages that are installed through
virtualenv. The list of packages are available in files named like
*requirements\*.txt*. Let's install all of them at once:

.. code-block:: bash

  $ for project in python-openflow kyco kyco-core-napps kytos-utils; do
      cd $project; \
      python setup.py develop || break; \
      pip install -r requirements.txt -r requirements-dev.txt || break; \
      cd -; \
    done

Cool! Now you have all dependencies and repositories cloned into your machine.
One more step: mininet.

How to install mininet
======================

Mininet is a network simulator which creates a network of virtual hosts,
switches, controller and the links among them. Mininet hosts run standard Linux
network software, and its switchs support Openflow for highly flexible custom
routing and Software Defined Networking.

First we need to install the mininet package. The `mininet project
<http://mininet.org/>`_ lists a few methods for installing the simulator. For
instance, you can use a virtual machine or you can install it to you operating
system.

.. code-block:: bash

  $ sudo apt-get install mininet

To test if the mininet is working you must run the command:

.. code-block:: bash

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

To see more about mininet you can access the webpage `mininet.org
<http://mininet.org/walkthrough/>`_.

.. include:: ../back_to_list.rst

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |venv| replace:: *Virtual Environments*
.. _venv: https://en.wikipedia.org/wiki/Virtual_environment_software

.. |virtualenv| replace:: **virtualenv**
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. |virtualenv_docs| replace:: **virtualenv docs**
.. _virtualenv_docs: https://virtualenv.pypa.io/en/stable/
