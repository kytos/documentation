:tocdepth: 2
:orphan:

.. _tutorial-setup-the-development-environment:

########################################
How to setup the development environment
########################################

********
Overview
********

This tutorial shows how to setup your development environment to contribute to
Kytos Ecossystem code (python-openflow, kyco, kytos NApps and so on). With this
setup you will also be able to run the *Kytos Controller* (|kyco|_) [this setup
is not suitable for production].

.. TODO:: Set the time

The average time to go through it is: XX min

What you will learn
====================

* How to create an isolated environment
* How install the Kytos Projects on development environment
* How install mininet

********************
Virtual Environments
********************

First of all, in order code to Kytos projects we recommend you to use |venv|_.
This main reason for this recommendation is to keep the dependencies required
by different projects in separate places, by creating virtual Python
environments for them. It solves the “Project X depends on version 1.x but,
Project Y needs 4.x” dilemma, and keeps your global site-packages directory
clean and manageable. On this tutorial we will use the |virtualenv|_ package,
but if you are used to use another tool to create isolated environments or to
install every library on your global system, be confortable to do it your way.

If you want to read more about it, please visit: |virtualenv|_ and
|virtualenv_docs|_ pages.

.. Reviewed until here.... ASS: diraol

********************************
Setting up a virutal environment
********************************

To setup a isolated environment, we need install the tools virtualenvwrapper
and virtualenv. Virtualenv is a tool used to build a isolated environment and
the virtualenvwrapper is used to manager these environment. The following
sections you will learn how to create a virtualenv and how to use a
virtualenvwrapper.

On Ubuntu 16.10 do:

.. code-block:: bash

  $ sudo apt-get install python3.6 python3-pip git rrdtool libpython3.6-dev mininet

  $ sudo pip3 install virtualenvwrapper virtualenv

Configuring Virtualenv
======================

To configure the virtualenv we need set the variable *VIRTUALENVWRAPPER_PYTHON*
, update the *PATH* and load the file
**source /usr/local/bin/virtualenvwrapper.sh** before start a bash session. We
can do this using the commands below.

.. code-block:: bash

  $ echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
  $ echo "PATH=$PATH:$VIRTUALENVWRAPPER_PYTHON" >> ~/.bashrc
  $ echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc

Execute the command below to reload the current bash session:

.. code-block:: bash

  $ bash --login

Basics Virtualenvwrapper Commands
=================================

When you are using a virtulenvwrapper you can create, remove, list or use a
virtualenv.

Creating a new virtualenv
-------------------------

If you want create a new virtualenv, you must use the command below:

.. code-block:: bash

   $ mkvirtualenv VIRTUALENV_NAME -p python3.6

This command will create a virtualenv named VIRTUALENV_NAME and to use the
python3.6 as a default python into the environment. By default after created a
new virtualenv you will activate this environment.

Removing a virtualenv
---------------------

If you want to remove a existing virtualenv, you must to use the command below:

.. code-block:: bash

  $ rmvirtualenv VIRTUALENV_NAME

After this the virtualenv named VIRTUALENV_NAME will be removed.

Listing all virtualenv created
------------------------------

If you want to show all virtualenv created, you must use the command below:

.. code-block:: bash

  $ lsvirtualenv

Using a isolated environment
----------------------------

If you want to use a existing environment you can use the following command:

.. code-block:: bash

  $ workon VIRTUALENV_NAME

Where VIRTUALENV_NAME is the name of isolated enviroment that you can use.
After that you console will show the virtualenv activated between parenthesis,
like that:

.. code-block:: bash

  (VIRTUALENV_NAME) $

This mean that the VIRTUALENV_NAME is already activated.When
you want leave of this virtualenv you can use the command below:

.. code-block:: bash

  $ deactivate

After this you will use your system environment.

.. note:: Inside the virtualenv all pip packages will be installed within the ~/.virtualenvs/VIRTUALENV_NAME folder, outside the virtualenv all pip packages will be installed into the default system environment.


If you are interested in read more about the virtualenvwrapper commands you can
access the page `virtualenvwrapper commands
<http://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html>`_.

*************************************
How to clone the projects from Github
*************************************

What is GitHub?
================

GitHub is a web-based version control system and collaborative platform for
software developers.GitHub, which is delivered through a software-as-a-service
(SaaS) business model, was started in 2008 and was founded on Git.
Git is a open source version control system that was started by Linus Torvalds
- the same person who created Linux. Git is similar to other control version
system like Subversion(SVN), Mercurial and CSV.

Configuring git
===============

This configuration sub-section is based on the page `setup git configuration
<https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>`_, that
contain first time steps to setup your Git.

Your Identity
-------------

The first thing you should do when you install Git is to set your user name
and email address. This is important because every Git commit uses this
information, and it's immutably baked into the commits you start creating:

.. code-block:: bash

  $ git config --global user.name "John Doe"
  $ git config --global user.email johndoe@example.com

Your Editor
-----------

Now that your identity is set up, you can configure the default text editor
that will be used when Git needs you to type in a message. If not configured,
Git uses your system’s default editor.

If you want to use a different text editor, such as VIM,
you can do the following:

.. code-block:: bash

  $ git config --global core.editor vim


Checking your settings
----------------------

If you want to check your settings, you can use the command below to list all
the settings Git can find at that point:


.. code-block:: bash

  $ git config --list
  user.name=John Doe
  user.email=johndoe@example.com
  color.status=auto
  color.branch=auto
  color.interactive=auto
  color.diff=auto
  ...

Cloning the kytos projects
==========================

The basic commands listed below is the main commands used to contribute with a
existing Kytos projects.This sub-section is based on the page `basic-git-commands
<https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html>`_.

Cloning a existing project
--------------------------

If you want contribute with a kytos project, you must clone a project found
in `GitHub group <https://github.com/kytos>`_ to make your changes.The command
below will clone the project python-openflow.Below there is a example of how to
cloning a project, the project used is python-openflow.

.. code-block:: bash

  $ git clone https://github.com/kytos/python-openflow.git

After this command a folder called *python-openflow* was created and you find
all files of the project within it.

.. code-block:: bash

  $ cd python-openflow/
  $ ls
  pyof/                         requirements-dev.txt   setup.py
  requirements-docs.txt         tests/                 docs/
  raw/                          requirements.txt       LICENSE
  README.rst                    setup.cfg


*********************************************************
How to install the projects using development environment
*********************************************************

After cloned a project you must install the packages required to run the
project, you can do this running the commands below into the project folder.

.. code-block:: bash

  $ python setup.py develop
  $ pip install -r requirements.txt
  $ pip install -r requirements-dev.txt
  $ pip install -r requirements-docs.txt


The main projects used in this tutorial are python-openflow, kyco-core-napps,
kytos-utils, and kyco.For each project you can clone, and install the project
using the commands listed above.

How to install mininet
======================

Mininet is a network simulator which creates a network of virtual hosts,
switches, controller and links.Mininet hosts run standard Linux network
software , and its switchs support Openflow for highly flexible custom routing
and Software Defined Networking.

To test if the mininet is working you must to run the command:

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

If you can run mininet using a topology single with two hosts you can run this
with Kyco Controller locally using the command below.

.. code-block:: bash

  $ sudo mn --topo single,2 --mac --controller=remote,ip=127.0.0.1 --switch ovsk,protocols=OpenFlow10

To see more about mininet you can access the webpage
`mininet.org <http://mininet.org/walkthrough/>`_.

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |venv| replace:: *Virtual Environments*
.. _venv: https://en.wikipedia.org/wiki/Virtual_environment_software

.. |virtualenv| replace:: **virtualenv**
.. _virtualenv: http://docs.python-guide.org/en/latest/dev/virtualenvs/

.. |virtualenv_docs| replace:: **virtualenv docs**
.. _virtualenv_docs: https://virtualenv.pypa.io/en/stable/

