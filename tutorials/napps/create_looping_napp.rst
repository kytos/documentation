:tocdepth: 2
:orphan:

.. _tutorial-napps-create-loop:

###################################
How to create your own NApp: Part 2
###################################

********
Overview
********

This tutorial covers the basics on how to create a Network Application (NApp)
with an execution loop for *Kytos Controller* (|kytos|_).

The average time to go throught it is: ``10 min``

What you will learn
====================
* How to Create a NApp with a loop;
* How to adjust `settings.py` file for your NApp.

What you will need
===================
* How to create a basic NApp - Refer to |Tutorial_01|_.

************
Introduction
************

Now that you have learned how to build a simple NApp, in this tutorial we will
help you to develop a more sophisticated one.

Suppose that you need an application that gather some data periodically from
the controller or from the switches. In this situation, it is desirable to have
a NApp that can run repeatedly without creating complex loops. Kytos provides
the necessary tools to quick and easily create such a NApp.

Before proceeding to the next section of this tutorial, go to the
|napps_server_sign_up| in order to create a user for you on our
|napps_server|_. After you submit the form you will receive an email to confirm
your registration. Click on the link present on the email body and, after
seeing the confirmation message on the screnn, go to the next section.

***********************
Creating a looping NApp
***********************

In this tutorial, we will create a simple NApp, for learning purposes.
This NApp will get the controller uptime from time to time and display it.

Also, we are going to introduce you to the NApps settings, a basic Python module
where you can store, for example, configuration constants used by your NApp.
This way, it is easier to maintain, understand and customize your code.

You can create the NApp structure manually, but Kytos has the ``kytos-utils``
project with a few command line utilities that can help you to create it.

.. NOTE:: Make sure that you have completed your |dev_env|_  setup and that
    you have enabled your virtual environment in order to have all kytos
    projects available to you.

Let's create the structure:

.. code-block:: console

   $ cd
   $ mkdir tutorials
   $ cd tutorials
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

   Please, insert your NApps Server username: <username>
   Please, insert your NApp name: loopnapp
   Please, insert a brief description for your NApp [optional]: Loop NApp

   Congratulations! Your NApp have been bootstrapped!
   Now you can go to the directory <username>/loopnapp and begin to code your NApp.
   Have fun!

You will be asked a few questions. Answer them according to your needs, they are
very basic questions like username and NApp name. For this tutorial purpose, use
your **<username>** (the one you have just registered) and **loopnapp**,
respectively.

.. TIP:: If you want to change the answers in the future, just edit the
   ``kytos.json`` file and rename the directories if necessary.

Now you have a bootstrap NApp structure to work on.

During this tutorial, the only files that we need to worry about are the
``main.py`` and ``settings.py``.  Open with your preferred editor and let's
code. See an example using nano:

.. code-block:: console

  $ cd ~/tutorials/<username>/loopnapp
  $ nano main.py settings.py

settings.py
===========

In order to adjust the polling frequency, let's define a variable in
`settings.py`. For instance, `UPTIME_INTERVAL` will store a number, in
seconds, that we will use to determine our polling interval. In this
example, our NApp will get the controller uptime every fifteen seconds.

.. code-block:: python3

    # Polling frequency
    UPTIME_INTERVAL = 15


main.py
=======

Setup
^^^^^

In `main.py` file, we have to adjust the `setup()` method. We will add a
line to tell the controller that this NApp will run repeatedly.

.. code-block:: python3

   def setup(self):
       log.info("Loop NApp Loaded!")
       self.execute_as_loop(settings.UPTIME_INTERVAL)


The method execute_as_loop(x) is a Kytos NApp built-in method that instructs
the controller to execute the method `execute` every *x* seconds.

If you don't call `execute_as_loop`, the `execute` method will be executed
only once, right after the `setup` method is finished.

Execute
^^^^^^^

In the `execute` method we code what will be executed every fifteen seconds. In
this case, we gather the controller's uptime and print it in the logs.

.. code-block:: python3

   def execute(self):
       uptime = self.controller.uptime()
       log.info("Controller Uptime: %s", uptime)


Running Periodically
~~~~~~~~~~~~~~~~~~~~

The entire NApp's source code of the looping NApp follows:

.. code-block:: python3

    from kytos.core import KytosNApp, log
    from napps.<username>.loopnapp import settings


    class Main(KytosNApp):

        def setup(self):
            log.info("Loop NApp Loaded!")
            self.execute_as_loop(settings.UPTIME_INTERVAL)

        def execute(self):
            uptime = self.controller.uptime()
            log.info("Controller Uptime: %s", uptime)

        def shutdown(self):
            log.info("Loop NApp Unloaded!")

*****************
Running your NApp
*****************

In order to install and enable your NApp, you have to first run the Kytos controller.
Kytos will then be able to recognize and manage installed/enabled NApps. In another
terminal window, activate the virtual environment and run:

.. code-block:: console

  $ kytosd -f

  2017-07-04 16:57:59,351 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-07-04 16:57:59,352 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-07-04 16:57:59,353 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-07-04 16:57:59,354 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6653
  2017-07-04 16:57:59,356 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-07-04 16:57:59,358 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-07-04 16:57:59,359 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-07-04 16:57:59,361 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-07-04 16:57:59,362 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-07-04 16:57:59,371 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-07-04 16:57:59,373 - INFO [kytos.core.controller] (MainThread) Loading NApp <username>/helloworld
  2017-07-04 16:57:59,507 - INFO [<username>/helloworld] (MainThread) Hello world! Now, I'm loaded!
  2017-07-04 16:57:59,520 - INFO [root] (helloworld) Running NApp: <Main(helloworld, started 139775231104768)>
  2017-07-04 16:57:59,527 - INFO [<username>/helloworld] (helloworld) Hello world! I'm being executed!

  (...)

  kytos $>

You can now list all NApps, verify which ones are enabled and disable them. Only
the new NApp will run this time. Yes, we are not running any other NApp for now,
we are disabling everything, including OpenFlow NApps.

.. code-block:: console

  $ kytos napps list

  Status |          NApp ID          |                      Description
  =======+===========================+=======================================================
   [i-]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for ...
   [i-]  | kytos/flow_manager        | Manage switches' flows through a REST API.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swit...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using t...
   [i-]  | kytos/topology            | Keeps track of links between hosts and switches. Re...
   [ie]  | <username>/helloworld     | Hello, world!

  Status: (i)nstalled, (e)nabled

  $ kytos napps disable <username>/helloworld
  INFO  NApp <username>/helloworld:
  INFO    Disabling...
  INFO    Disabled.


In order to run your NApp, you can install it locally or remotely:

To install locally, you have to run the following commands:

.. code-block:: console

  $ cd ~/tutorials/<username>/loopnapp
  $ python3 setup.py develop

To install remotely, you have to publish it first:

.. code-block:: console

  $ cd ~/tutorials/<username>/loopnapp
  $ kytos napps upload
  Enter the username: <username>
  Enter the password for <username>: <password>
  SUCCESS: NApp <username>/loopnapp uploaded.

Now that you have published your NApp, you can access |napps_server|_ and see
that it was sent. After that, you can install it using the ``kytos`` command
line from the ``kytos-utils`` package:

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps install <username>/loopnapp
  INFO  NApp <username>/loopnapp:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

.. NOTE:: This will try to get this napp from your current directory, then
   install it into your system. The NApp will also be enabled and immediately
   executed.

You can now see your NApp installed and enabled by running the command:

.. code-block:: console

  $ kytos napps list

  Status |          NApp ID          |                      Description
  =======+===========================+=======================================================
   [i-]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for ...
   [i-]  | kytos/flow_manager        | Manage switches' flows through a REST API.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swit...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using t...
   [i-]  | kytos/topology            | Keeps track of links between hosts and switches. Re...
   [i-]  | <username>/helloworld     | Hello, world!
   [ie]  | <username>/loopnapp       | Loop NApp


Testing your NApp
=================

Back to the Kytos console, we can check the log messages. After seeing several
lines with ``Controller Uptime``, type ``quit`` to stop the controller.

.. code-block:: console

  kytos $> 2017-07-17 23:24:53,128 - INFO [<username>/loopnapp] (Thread-1) Loop NApp Loaded!
  2017-07-17 23:24:53,131 - INFO [root] (loopnapp) Running NApp: <Main(loopnapp, started 140460012750592)>
  2017-07-17 23:24:53,134 - INFO [<username>/loopnapp] (loopnapp) Controller Uptime: 0:01:14.565704
  2017-07-17 23:25:08,138 - INFO [<username>/loopnapp] (loopnapp) Controller Uptime: 0:01:29.569314
  2017-07-17 23:25:23,141 - INFO [<username>/loopnapp] (loopnapp) Controller Uptime: 0:01:44.572042
  kytos $> quit
  Stopping Kytos daemon... Bye, see you!
  2017-07-17 23:25:29,729 - INFO [kytos.core.controller] (MainThread) Stopping Kytos
  (...)


As you can see, the uptime was reported several times, at 23:24:53, 23:25:08 and
23:25:23 with an interval of 15 seconds, as expected.

That's it! With only one line added to the `setup` method, your code will be
running periodically. If you want to change the interval later, modify only the
`settings.py` file and the new value will be used next time the NApp is loaded.

.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |napps_server_sign_up| replace:: **sign_up**
.. _napps_server_sign_up: https://napps.kytos.io/signup/
