:tocdepth: 2
:orphan:

.. _tutorial-create-your-napp:

###################################
How to create your own NApp: Part 1
###################################

********
Overview
********
This tutorial covers the basics on how to create your own Netwok Application
(**NApp**) for *Kytos Controller* (|kyco|_).

.. TODO:: Set the time

The average time to go throught it is: ``XX min``

What you will learn
====================
* How to create a basic NApp
* How your NApp comunicate with the Controller
* How to install, test and debug your NApp

What you will need
===================
* Your |dev_env|_ already setup

************
Introduction
************
Most of Kytos ecossystem functionalities are delivered by the Network
Applications (NApps). These applications comunicate with the controller, and
between themselves, throught events (KycoEvents), and they can also expose REST
endpoints to the world.

If you are developing a basic SDN application, you should be able to do
everything inside a Napp, without having to patch the controller core.

.. NOTE:: If you found something that is limiting your napp development, don't
   shy away from reporting us this issue on our |controller_github|_.

The idea of a NApp is to be as atomic as it can be, solving a small and specific
problem, in a way that NApps can work togheter to solve a bigger problem,
following the |dotdiw|_.

Moreover, you can see the NApps developped by the Kytos Community on our NApps
Server: http://napps.kytos.io.

.. CAUTION:: Kytos Napps repository is still in beta stage.

.. _napp_naming:

Naming your NApp
================
The first thing that you should do is create a name for your napp. We use a
namespace based on author name, in that way two authors can have applications
with the same name. For instance: ``john/switchl2`` and ``mary/switchl2`` are
both valid napps unique identifiers.

..  [proto][repo]/[author]/[napp]:[tag]

Since your NApp will work as a Python Module, its name must follow the same
naming rules from python modules, defined by `PEP8
<https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_, which
states that:

  Modules should have short, all-lowercase names. Underscores can be used in
  the module name if it improves readability. Python packages should also have
  short, all-lowercase names, although the use of underscores is discouraged.

Understanding the NApp structure
================================
Here you can see the basic NApp structure. You can create it by hand or you can
use our ``kytos`` command line that we are going to describe during the next
section::

  <author_name>
  ├── __init__.py
  └── <napp_name>
      ├── __init__.py
      ├── kytos.json
      ├── main.py
      ├── README.rst
      └── settings.py

- **kytos.json**: This file has your NApp metadata. You can edit the attributes
  on it. Those attributes are used by the |napps_server|_ to distribute your
  NApp.
- **settings.py**: Main settings parameters of your NApp
- **main.py**: Main source code of your NApp
- **README.rst**: Main description and informations about your NApp

During this tutorial we are going to use only the ``main.py`` file to code our
NApp. But if your code is big enought feel free to split your NApp into
multiples modules.

*************************
Creating your first NApp
*************************
Now that we understand the basic structure of a |kyco|_ NApp, lets start
building our own, the |nn| NApp.

You can create the napp structure manually, but the Kytos project has an
``kytos-utils`` package with few command line utilities that can help you to
create this.

.. NOTE:: Make sure that you had completed your |dev_env|_  setup.

During this first tutorial we are going to create a very dummy application. This
application will print a message when is loaded and another message when it is
unloaded from the controller.

Let's create the structure:

.. code-block:: bash

   $ mkdir ~/tutorial01/
   $ cd ~/tutorial01/
   $ kytos napp init .

.. TODO:: We need to code the kytos napp init. Using jinja2 templates.

.. Template should be inserted here: /etc/skell/kytos/napp-structre/ with the
.. structure and template files.

You will be asked a few questions. Answer them according to your needs, they are
very basic questions like author and napp name.

For this tutorial, when asking for the author and NApp name, answer **tutorial**
and **helloworld**, respectively.

.. TIP:: If you want to change the answers on the future, just edit the
   ``kytos.json`` file, and rename the directories if necessary.

Now you have a bootstrap NApp structure to work on it.

During this tutorial, the only file that we need to worry about is the
``main.py``.  Open it with your preferred editor and let's code.

.. TIP:: ``main.py`` is located inside your NApp folder.

.. code-block:: python

  from kyco.core.napps import KycoNApp
  from napps.tutorial.helloworld import settings

  log = settings.log


  class Main(KycoNApp):

      def setup(self):
          pass

      def execute(self):
          pass

      def shutdown(self):
          pass


In this file, we have a class entry point (``Main``) to execute our NApp.
This class has 3 basic methods: ``setup``, ``execute`` and ``shutdown``.

First, let's discuss the ``setup`` method.

The ``setup`` method replaces the '__init__' method for the KycoNApp subclass
and it is automatically called by the controller when our application is loaded.

For this dummy napp, let's just print some log message (edit the file to match
the following code):

.. code-block:: python

      def setup(self):
          log.info("Hello world! Now, I'm loaded!")

.. important::
   Do not override ``__init__``. Instead, use ``setup``.

Right after the setup, there is the ``execute`` method. But we are going to
cover it deeper on part 2 of this tutorial.

.. code-block:: python

      def execute(self):
          log.info("Hello world! I'm being executed!")


And, finnally we have the ``shutdown`` method. That is executed when the NApp is
unloaded.

.. code-block:: python

      def shutdown(self):
          log.info("Bye world!")


Here are the final result after all changes:

.. code-block:: python

  from kyco.core.napps import KycoNApp
  from napps.tutorial.helloworld import settings

  log = settings.log


  class Main(KycoNApp):

      def setup(self):
          log.info("Hello world! Now, I'm loaded!")

      def execute(self):
          log.info("Hello world! I'm being executed!")

      def shutdown(self):
          log.info("Bye world!")

*****************
Running your NApp
*****************

In order to run your NApp, first your have to install it. Again, we are going to
use the ``kytos`` command line from the ``kytos-utils`` package.

.. code-block:: bash

  $ sudo kytos napps install tutorial/heloworld

.. NOTE:: This will try to get this NApp from your current directory, then
   install it into your system. This NApp will also be enable.

Now, your NApp is ready to be executed. You can also see if your NApp is
installed and enabled, by running the command:

.. code-block:: bash

  $ kytos napps list

For this demo, we don't need to have any other NApp loaded except this created
during this tutorial. So if your setup has multiple NApps, please disable them,
with the command:

.. code-block:: bash

  $ kytos napps disable <author_name>/<napp_name>


Yes, we are not running any NApp for now. We are disabling everything including
OpenFlow NApps.

Testing your NApp
=================

Let's start our controller:

.. code-block:: bash

  $ kytos-kyco start

You will get into the controller terminal, and you can see your NApp output.

.. TODO:: Execute all the steps on this tutorial, and paste here the console
   output.

Congratulations!! You have created your first Kytos NApp!!

.. CAUTION:: Currently you have to restart the controller in order to have your
   napp running. Very soon kytos will support auto reload.

.. TODO:: How to **load** the napp on a running Kyco instance? (Future, low
   priority)

.. include:: ../back_to_list.rst

.. |controller_github| replace:: *Controller Github page*
.. _controller_github: https://github.com/kytos/kyco/issues/

.. |nn| replace:: ``hello_world``

.. |pyof| replace:: *python3-openflow*
.. _pyof: http://docs.kytos.io/pyof

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. TODO:: Where does the Kyco Events documentation will be hosted?
    Should we link to the main kyco documentation? Or we will have a Tutorial
    explaining the KycoEvents?

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: http://docs.kytos.io/kyco/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |dotdiw| replace:: "*Do one thing, do it well*" Unix philosophy
.. _dotdiw: https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well

.. |napp_ipv6| replace:: *kytos/of_ipv6drop* napp
.. _napp_ipv6: http://napps.kytos.io/kytos/of.ipv6drop/
