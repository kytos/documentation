:tocdepth: 2
:orphan:

.. _tutorial-create-your-napp:

###################################
How to create your own NApp: Part 1
###################################

********
Overview
********
This tutorial covers the basics on how to create your own Network Application
(**NApp**) for *Kytos* (|kytos|_).

The average time to go through this is: ``15 min``

What you will learn
====================
* How to create a basic NApp;
* How your NApp communicates with the Kytos Controller;
* How to install, test, and debug your NApp.

What you will need
===================
* Your |dev_env|_ already up and running.

************
Introduction
************
Most of the Kytos Platform functionalities are delivered by Network
Applications, **NApps** for short.
These applications communicate with the controller and with each other through
events (|KytosEvents|_), and they can also expose REST endpoints to the world.

If you are developing a basic SDN application, you should be able to do
everything inside a NApp, without having to patch the controller core.

.. NOTE:: If you find something that is limiting your NApp development, don't
   shy away from reporting us this issue in our |controller_github|_.

The idea of a NApp is to be as atomic as it can be, solving a small and specific
problem, in a way that NApps can work together to solve a bigger problem,
following the |dotdiw|_.

Moreover, you can use and learn from NApps developed by the Kytos Community that
are available at the NApps Server: http://napps.kytos.io.

.. CAUTION:: Kytos NApps repository is still in beta stage.

.. _napp_naming:

Naming your NApp
================
The first thing that you should do is to create a name for your NApp.
We use a namespace based on username and NApp name.
Thus, two usernames can use the same NApp name.
For instance: ``john/switchl2`` and ``mary/switchl2`` are both valid NApps
*unique identifiers*.

..  [proto][repo]/[username]/[napp]:[tag]

Since your NApp will work as a Python module, its name must follow the same
naming rules of Python modules, defined by `PEP8
<https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_, which
states that:

  Modules should have short, all-lowercase names. Underscores can be used in
  the module name if it improves readability.

Understanding the NApp structure
================================
Here you can see the basic NApp structure. A minimal working NApp must have the
files **kytos.json** and **main.py**. Don't worry about creating these folders
and files. We provide a tool to generate this structure for you! ::

  <username>
  ├── __init__.py
  └── <napp_name>
      ├── __init__.py
      ├── kytos.json
      ├── main.py
      ├── README.rst
      └── settings.py

- **kytos.json**: This file contains your NApp's metadata. **username**
  and **name** are required. Other attributes are
  used by the |napps_server|_ to publish and distribute your NApp worldwide.
- **settings.py**: Main settings parameters of your NApp (if applicable).
- **main.py**: Main source code of your NApp.
- **README.rst**: Main description and information about your NApp.

During this tutorial we are going to use only the ``main.py`` file
(``kytos.json`` content will be automatically created by our tool).
If your code is big enough, feel free to split your NApp into multiples files.

************************
Creating your first NApp
************************
Now that we understand the basic structure of a |kytos|_ NApp, let's start
building our own, the |nn| NApp.

You can create the NApp structure manually or use the command line utilities
of the ``kytos-utils`` project.

.. NOTE:: Make sure that you had completed your |dev_env|_ setup and the
   virtual environment is active.

During this first tutorial we are going to create a very dummy application.
This application will print a message when loaded and another message when
unloaded by the controller.

Let's create the NApp structure:

.. code-block:: bash

   $ cd
   $ mkdir tutorials
   $ cd tutorials
   $ kytos napps create


You will be asked a few questions. Answer them according to your needs, they are
very basic questions like username and NApp name. For this tutorial purpose,
answer **tutorial** and **helloworld**, respectively.

The output should be something like this:

.. code-block:: bash

  --------------------------------------------------------------
  Welcome to the bootstrap process of your NApp.
  --------------------------------------------------------------
  In order to answer both the username and the napp name,
  You must follow this naming rules:
   - name starts with a letter
   - name contains only letters, numbers or underscores
   - at least three characters
  --------------------------------------------------------------

  Please, insert your NApps Server username: tutorial
  Please, insert your NApp name: helloworld
  Please, insert a brief description for your NApp [optional]: Hello, world!

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/helloworld and begin to code your NApp.
  Have fun!

.. TIP:: If you want to change the answers provided in the future, just edit
         the ``kytos.json`` file, and rename the directories if necessary.

Now, we have a bootstrap NApp structure to work with.

During this tutorial, the only file that we need to worry about is the
``main.py``. Open it with your preferred editor and let's code.

.. code-block:: bash

  $ cd ~/tutorials
  $ gedit tutorial/helloworld/main.py

.. NOTE::
  The code below is a simplified version of yours. You don't have to delete any
  other line, just replace the ``pass`` statement as described below.

.. code-block:: python

  from kytos.core import KytosNApp, log
  from napps.tutorial.helloworld import settings


  class Main(KytosNApp):

      def setup(self):
          pass

      def execute(self):
          pass

      def shutdown(self):
          pass

In this file, we have an entry point class (``Main``) to execute our NApp.
This class has 3 basic methods: ``setup``, ``execute`` and ``shutdown``.

.. IMPORTANT:: A valid NApp must have the 3 methods above. If you don't use a
  method, let the ``pass`` statement as its only content.

For this dummy NApp, let's just print some log messages. To do so, edit the file
and replace ``pass`` (meaning "do nothing") by ``log.info(...)`` as
detailed below:

.. ATTENTION::
  In Python, you must be careful about indentation. The ``log.info(...)`` lines
  should start in the same column of ``pass`` (4 spaces after the beginning of
  ``def ...(self)``). Do not use tab to indent.

The ``setup`` method is automatically called by the controller when our
application is loaded.

.. DANGER::
   For Python programmers: do not override ``__init__``. A KytosNApp subclass
   must use the ``setup`` method instead.

.. code-block:: python

      def setup(self):
          log.info("Hello world! Now, I'm loaded!")


Right after the setup there is the ``execute`` method, which we will cover in a
deeper way on part 2 of the tutorial.

.. code-block:: python

      def execute(self):
          log.info("Hello world! I'm being executed!")


Finally we have the ``shutdown`` method. This method is executed when the NApp
is unloaded.

.. code-block:: python

      def shutdown(self):
          log.info("Bye world!")



After making the suggested modifications, the ``Main`` file should look like
this (simplified, without comments):

.. code-block:: python

  from kytos.core import KytosNApp, log
  from napps.tutorial.helloworld import settings


  class Main(KytosNApp):

      def setup(self):
          log.info("Hello world! Now, I'm loaded!")

      def execute(self):
          log.info("Hello world! I'm being executed!")

      def shutdown(self):
          log.info("Bye world!")

*****************
Running your NApp
*****************

In order to install and enable your NApp, you have to first run the Kytos controller. Kytos will then be
able to recognize and manage installed/enabled NApps.

Let's start our controller. When it is executed, it loads all of the previously enabled NApps.
At this point, only the kytos/of_core NApp shall be loaded. The Kytos controller runs by default as a
daemon. The ``-f`` option runs it in foreground. Open another terminal window, make sure to activate
your virtual environment and execute:

.. code-block:: console

  $ kytosd -f
  2017-07-04 14:47:57,429 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-07-04 14:47:57,430 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-07-04 14:47:57,431 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-07-04 14:47:57,432 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6633
  2017-07-04 14:47:57,435 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-07-04 14:47:57,436 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-07-04 14:47:57,439 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-07-04 14:47:57,440 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-07-04 14:47:57,441 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-07-04 14:47:57,450 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-07-04 14:47:57,452 - INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_core
  2017-07-04 14:47:57,898 - INFO [root] (of_core) Running NApp: <Main(of_core, started 139884996060928)>

  (...)

  kytos $>


In the Kytos console, you can see a log line pointing out that kytos/of_core is running.
You can list all installed and enabled NApps by switching back to the previous terminal and
running the command:

.. code-block:: bash

  $ kytos napps list

  Status |          NApp ID          |                      Description
  =======+===========================+=======================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for ...
   [i-]  | kytos/of_flow_manager     | Manage switches' flows through a REST API.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all switches.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swit...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using t...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | Keeps track of links between hosts and switches. Re...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interface setti...

  Status: (i)nstalled, (e)nabled

For this demo, we don't need to have any other NApp loaded except the one we
just created. So, if your setup has multiple enabled NApps, you can disable them
with the command:

.. code-block:: console

  $ kytos napps disable <NApp ID>

As just seen before, the ``kytos/of_core`` NApp is installed and enabled. If so,
disable it with:

.. code-block:: console

  $ kytos napps disable kytos/of_core
  INFO  NApp kytos/of_core:
  INFO    Disabling...
  INFO    Disabled.

Yes, we are not running any other NApp for now. We are disabling everything
including OpenFlow NApps.

In order to run your NApp, you have to install it first. Again, we are going to
use the ``kytos`` command line from the ``kytos-utils`` project.

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps install tutorial/helloworld
  INFO  NApp tutorial/helloworld:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

.. NOTE:: This will look for the *helloworld* NApp inside the
   *tutorial/helloworld* directory (and also the current one), then
   install it into your system. This NApp will also be enabled and
   immediately executed by Kytos.


Testing your NApp
=================

You can check the logs in the Kytos console to verify your NApp working! The log messages are presented
as follows:


.. code-block:: console

  2017-07-04 14:51:59,931 - INFO [tutorial/helloworld] (Thread-1) Hello world! Now, I'm loaded!
  2017-07-04 14:51:59,935 - INFO [root] (helloworld) Running NApp: <Main(helloworld, started 139884979275520)>
  2017-07-04 14:51:59,938 - INFO [tutorial/helloworld] (helloworld) Hello world! I'm being executed!

Congratulations! You have created your first Kytos NApp!
To see the shutdown message, type ``quit`` in the Kytos console:

.. code-block:: console

  kytos $> quit
  Stopping Kytos daemon... Bye, see you!
  (...)
  2017-07-04 14:54:28,511 - INFO [kytos.core.controller] (MainThread) Shutting down NApp tutorial/helloworld...
  2017-07-04 14:54:28,515 - INFO [tutorial/helloworld] (MainThread) Bye, world!


.. include:: ../back_to_list.rst

.. |controller_github| replace:: *Controller Github page*
.. _controller_github: https://github.com/kytos/kytos/issues/

.. |nn| replace:: ``hello_world``

.. |pyof| replace:: *python-openflow*
.. _pyof: http://docs.kytos.io/python-openflow

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |kytosevents| replace:: *KytosEvents*
.. _kytosevents: https://docs.kytos.io/kytos/developer/listened_events/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |dotdiw| replace:: "*Do one thing, do it well*" Unix philosophy
.. _dotdiw: https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well

.. |napp_ipv6| replace:: *kytos/of_ipv6drop* napp
.. _napp_ipv6: http://napps.kytos.io/kytos/of.ipv6drop/
