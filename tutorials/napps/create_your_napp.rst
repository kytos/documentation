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
(**NApp**) for *Kytos Controller* (|kyco|_).

The average time to go through this is: ``15 min``

What you will learn
====================
* How to create a basic NApp;
* How your NApp communicate with the Kytos Controller;
* How to install, test, and debug your NApp.

What you will need
===================
* Your |dev_env|_ already setup.

************
Introduction
************
Most of the Kytos Ecosystem functionalities are delivered by Network
Applications, **NApps** for short.
These applications communicate with the controller and with each other through
events (|KycoEvents|_), and they can also expose REST endpoints to the world.

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

..  [proto][repo]/[author]/[napp]:[tag]

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

- **kytos.json**: This file contains your NApp's metadata. **author** (soon to
  be changed to *username*) and **name** are required. Other attributes are
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
Now that we understand the basic structure of a |kyco|_ NApp, let's start
building our own, the |nn| NApp.

You can create the NApp structure manually or use the command line utilities
of the ``kytos-utils`` project.

.. NOTE:: Make sure that you had completed your |dev_env|_ setup and its venv
   is active.

During this first tutorial we are going to create a very dummy application.
This application will print a message when loaded and another message when
unloaded from the controller.

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
  In order to answer both the author name and the napp name,
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

  from kyco.core.napps import KycoNApp
  from napps.tutorial.helloworld import settings


  class Main(KycoNApp):

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
and replace ``pass`` (meaning "do nothing") by the ``self.log.info(...)`` as
detailed below:

.. ATTENTION::
  In Python, you must be careful about indentation. The ``self.log.info(...)`` lines
  should start in the same column of ``pass`` (4 spaces after the beginning of
  ``def ...(self)``). Do not use tab to indent.

The ``setup`` method is automatically called by the controller when our
application is loaded.

.. DANGER::
   For Python programmers: do not override ``__init__``. A KycoNApp subclass
   must use the ``setup`` method instead.

.. code-block:: python

      def setup(self):
          self.log.info("Hello world! Now, I'm loaded!")


Right after the setup, there is the ``execute`` method that we are going to
cover it deeper on part 2 of this tutorial.

.. code-block:: python

      def execute(self):
          self.log.info("Hello world! I'm being executed!")


Finally we have the ``shutdown`` method. This method is executed when the NApp
is unloaded.

.. code-block:: python

      def shutdown(self):
          self.log.info("Bye world!")



After making the suggested modifications, the ``Main`` file should look like
this (simplified, without comments):

.. code-block:: python

  from kyco.core.napps import KycoNApp
  from napps.tutorial.helloworld import settings


  class Main(KycoNApp):

      def setup(self):
          self.log.info("Hello world! Now, I'm loaded!")

      def execute(self):
          self.log.info("Hello world! I'm being executed!")

      def shutdown(self):
          self.log.info("Bye world!")

*****************
Running your NApp
*****************

In order to run your NApp, you have to install it first. Again, we are going to
use the ``kytos`` command line from the ``kytos-utils`` project.

.. code-block:: bash

  $ cd ~/tutorials
  $ kytos napps install tutorial/helloworld
  INFO  NApp tutorial/helloworld:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

.. NOTE:: This will look for the *helloworld* NApp inside the
   *tutorial/helloworld* directory (and also the current one), then
   install it into your system. This NApp will also be enabled.

Now, your NApp is ready to be executed. You can also see if your NApp is
installed and enabled, by running the command:

.. code-block:: bash

  $ kytos napps list

  Status |          NApp ID          |                      Description
  =======+===========================+=======================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for ...
   [i-]  | kytos/of_flow_manager     | NApp that manages switches flows.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all switches.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swit...
   [i-]  | kytos/of_l2lsloop         | A L2 learning switch application for openflow switc...
   [i-]  | kytos/of_lldp             | App responsible by send packet with lldp protocol t...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | A simple app that update links between machines and...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interface setti...
   [ie]  | tutorial/helloworld       | Hello, World!

  Status: (i)nstalled, (e)nabled

For this demo, we don't need to have any other NApp loaded except the one we
just created. So, if your setup has multiple enabled NApps, please, disable them
with the command:

.. code-block:: bash

  $ kytos napps disable <NApp ID>

As default, the ``kytos/of_core`` NApp may be installed and enabled. If so,
disable it with:

.. code-block:: bash

  $ kytos napps disable kytos/of_core
  INFO  NApp kytos/of_core:
  INFO    Disabling...
  INFO    Disabled.

Yes, we are not running any other NApp for now. We are disabling everything
including OpenFlow NApps.

Testing your NApp
=================

Let's start our controller:

.. code-block:: bash

  $ kyco
  2017-02-16 20:28:57,624 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller
  2017-02-16 20:28:57,628 - INFO [kyco.core.tcp_server] (TCP server) Kyco listening at 0.0.0.0:6633
  2017-02-16 20:28:57,629 - INFO [kyco.controller] (RawEvent Handler) Raw Event Handler started
  2017-02-16 20:28:57,630 - INFO [kyco.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-02-16 20:28:57,630 - INFO [kyco.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-02-16 20:28:57,631 - INFO [kyco.controller] (AppEvent Handler) App Event Handler started
  2017-02-16 20:28:57,631 - INFO [kyco.controller] (MainThread) Loading kyco apps...
  2017-02-16 20:28:57,632 - INFO [kyco.controller] (MainThread) Loading NApp tutorial/helloworld
  2017-02-16 20:28:57,647 - INFO [werkzeug] (Thread-2)  * Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)
  2017-02-16 20:28:57,648 - INFO [kyco.core.napps] (Thread-3) Running Thread-3 App
  2017-02-16 20:28:57,650 - INFO [napps.tutorial.helloworld.settings] (Thread-3) Hello world! Now, I'm loaded!
  2017-02-16 20:28:57,650 - INFO [napps.tutorial.helloworld.settings] (Thread-3) Hello world! I'm being executed!

Congratulations! You have created your first Kytos NApp! The last 2 lines show
you NApp is working. To see the shutdown message, hit ``CTRL+C``::

  (...)
  2017-02-16 22:02:48,168 - INFO [napps.tutorial.helloworld.settings] (Thread-6) Bye world!
  (...)

.. NOTE:: You may see more than one shutdown message depending on how many
   threads the controller was using for your NApp.

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

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: https://docs.kytos.io/kyco/developer/listened_events/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |dotdiw| replace:: "*Do one thing, do it well*" Unix philosophy
.. _dotdiw: https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well

.. |napp_ipv6| replace:: *kytos/of_ipv6drop* napp
.. _napp_ipv6: http://napps.kytos.io/kytos/of.ipv6drop/
