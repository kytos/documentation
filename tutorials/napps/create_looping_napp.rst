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
with an execution loop for *Kytos Controller* (|kyco|_).

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

.. code-block:: bash

   $ cd
   $ mkdir tutorials
   $ cd tutorials
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

   Please, insert your NApps Server username: tutorial
   Please, insert your NApp name: loopnapp
   Please, insert a brief description for your NApp [optional]: Loop NApp

   Congratulations! Your NApp have been bootstrapped!
   Now you can go to the directory tutorial/loopnapp and begin to code your NApp.
   Have fun!

You will be asked for few questions. Answer them according to your needs, they
are very basic questions like username and NApp name. For this tutorial, answer
**tutorial** and **loopnapp**, respectively.

.. TIP:: If you want to change the answers in the future, just edit the
   ``kytos.json`` file and rename the directories if necessary.

Now you have a bootstrap NApp structure to work on.

During this tutorial, the only files that we need to worry about are the
``main.py`` and ``settings.py``.  Open with your preferred editor and let's
code::

  $ cd ~/tutorials/tutorial/loopnapp
  $ gedit main.py settings.py

settings.py
===========

In order to adjust the polling frequency, let's define a variable in
`settings.py`. For instance, `STATS_INTERVAL` will store a number, in
seconds, that we will use to determine our polling interval. In this
example, our NApp will get the controller uptime every five seconds.

.. code-block:: python

    # Polling frequency
    STATS_INTERVAL = 5


main.py
=======

Setup
^^^^^

In `main.py` file, we have to adjust the `setup()` method. We will add a
line to tell the controller that this NApp will run repeatedly.

.. code-block:: python

   def setup(self):
       self.log.info("Loop NApp Loaded!")
       self.execute_as_loop(settings.STATS_INTERVAL)


The method execute_as_loop() is a Kytos NApp built-in method that instructs
the controller to execute the method `execute` every *x* seconds.

If you don't call `execute_as_loop`, the `execute` method will be executed
only once, right after the `setup` method is finished.

Execute
^^^^^^^

In the `execute` method, we code what will be execute every fifteen seconds. In
this case, we gather the controller's uptime and print it in the logs.

.. code-block:: python

   def execute(self):
       uptime = self.controller.uptime()
       self.log.info("Controller Uptime: %s", uptime)


Running Periodically
~~~~~~~~~~~~~~~~~~~~

The entire NApp's source code of the looping NApp follows:

.. code-block:: python

    from kyco.core.napps import KycoNApp
    from napps.tutorial.loopnapp import settings


    class Main(KycoNApp):

        def setup(self):
            self.log.info("Loop NApp Loaded!")
            self.execute_as_loop(settings.STATS_INTERVAL)

        def execute(self):
            uptime = self.controller.uptime()
            self.log.info("Controller Uptime: %s", uptime)

        def shutdown(self):
            self.log.info("Loop NApp Unloaded!")

*****************
Running your NApp
*****************

In order to run your NApp, first you have to install it. Again, we are going
to use the ``kytos`` command line from the ``kytos-utils`` package.

.. code-block:: bash

  $ cd ~/tutorials
  $ kytos napps install tutorial/loopnapp
  INFO  NApp tutorial/loopnapp:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

.. NOTE:: This will try to get this napp from your current directory, then
   install it into your system. This napp it will also be enable.

Now, your Napp is ready to be executed.

You can also see if your Napp is installed and enabled, by running the command:

.. code-block:: bash

  $ kytos napps list

  Status |          NApp ID          |                      Description
  =======+===========================+=======================================================
   [i-]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for ...
   [i-]  | kytos/of_flow_manager     | NApp that manages switches flows.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all switches.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swit...
   [i-]  | kytos/of_l2lsloop         | A L2 learning switch application for openflow switc...
   [i-]  | kytos/of_lldp             | App responsible by send packet with lldp protocol t...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | A simple app that update links between machines and...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interface setti...
   [i-]  | tutorial/helloworld       | Hello, World!
   [ie]  | tutorial/loopnapp         | Loop NApp

For this demo, we don't need to have any other NApp loaded except the one we've
just created. So, if your setup has multiple enabled NApps, please, disable them
with the command:

.. code-block:: bash

  $ kytos napps disable <NApp ID>

Yes, we are not running any other NApp for now, we are disabling everything,
including OpenFlow NApps.

Testing your NApp
=================

Let's start our controller and check the log messages. After seeing several
lines with ``Controller Uptime``, press ``ctrl+c`` to stop the controller.

.. code-block:: bash

  $ kyco
  2017-02-16 02:21:41,530 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller
  2017-02-16 02:21:41,536 - INFO [kyco.core.tcp_server] (TCP server) Kyco listening at 0.0.0.0:6633
  2017-02-16 02:21:41,540 - INFO [kyco.controller] (RawEvent Handler) Raw Event Handler started
  2017-02-16 02:21:41,545 - INFO [kyco.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-02-16 02:21:41,546 - INFO [kyco.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-02-16 02:21:41,547 - INFO [kyco.controller] (AppEvent Handler) App Event Handler started
  2017-02-16 02:21:41,547 - INFO [kyco.controller] (MainThread) Loading kyco apps...
  2017-02-16 02:21:41,555 - INFO [kyco.core.napps] (Thread-3) Running Thread-3 App
  2017-02-16 02:21:41,556 - INFO [kyco.controller] (MainThread) Loading NApp tutorial/loopnapp
  2017-02-16 02:21:41,556 - INFO [werkzeug] (Thread-2)  * Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)
  2017-02-16 02:21:41,559 - INFO [kyco.core.napps] (Thread-4) Running Thread-4 App
  2017-02-16 02:21:41,563 - INFO [napps.tutorial.loopnapp.settings] (Thread-4) NApp Loop Loaded!
  2017-02-16 02:21:41,563 - INFO [napps.tutorial.loopnapp.settings] (Thread-4) Controller Uptime: -1 day, 23:59:59.996963
  2017-02-16 02:21:56,564 - INFO [napps.tutorial.loopnapp.settings] (Thread-4) Controller Uptime: -1 day, 23:59:44.996224
  2017-02-16 02:22:11,565 - INFO [napps.tutorial.loopnapp.settings] (Thread-4) Controller Uptime: -1 day, 23:59:29.995061
  ^CStopping controller...
  2017-02-16 02:22:14,614 - INFO [kyco.controller] (MainThread) Stopping Kyco
  2017-02-16 02:22:15,110 - INFO [kyco.core.buffers] (MainThread) Stop signal received by Kyco buffers.
  2017-02-16 02:22:15,110 - INFO [kyco.core.buffers] (MainThread) Sending KycoShutdownEvent to all apps.
  2017-02-16 02:22:15,111 - INFO [kyco.core.buffers] (MainThread) [buffer: raw_event] Stop mode enabled. Rejecting new events.
  2017-02-16 02:22:15,114 - INFO [kyco.core.buffers] (MainThread) [buffer: msg_in_event] Stop mode enabled. Rejecting new events.
  2017-02-16 02:22:15,117 - INFO [napps.tutorial.loopnapp.settings] (Thread-7) NApp Loop Unloaded!
  2017-02-16 02:22:15,117 - INFO [napps.tutorial.loopnapp.settings] (Thread-4) Controller Uptime: -1 day, 23:59:26.442766
  2017-02-16 02:22:15,118 - INFO [kyco.core.buffers] (MainThread) [buffer: msg_out_event] Stop mode enabled. Rejecting new events.
  2017-02-16 02:22:15,123 - INFO [kyco.core.buffers] (MainThread) [buffer: app_event] Stop mode enabled. Rejecting new events.
  2017-02-16 02:22:15,121 - INFO [napps.tutorial.loopnapp.settings] (Thread-8) NApp Loop Unloaded!
  2017-02-16 02:22:15,129 - INFO [werkzeug] (Thread-10) 127.0.0.1 - - [16/Feb/2017 02:22:15] "GET /kytos/shutdown HTTP/1.1" 200 -
  2017-02-16 02:22:15,130 - INFO [napps.tutorial.loopnapp.settings] (Thread-11) NApp Loop Unloaded!
  2017-02-16 02:22:15,134 - INFO [kyco.controller] (MainThread) Stopping thread: Thread-2
  2017-02-16 02:22:15,629 - INFO [kyco.controller] (MainThread) Stopping thread: TCP server
  2017-02-16 02:22:15,630 - INFO [kyco.controller] (MainThread) Stopping thread: RawEvent Handler
  2017-02-16 02:22:15,630 - INFO [kyco.controller] (MainThread) Stopping thread: MsgInEvent Handler
  2017-02-16 02:22:15,630 - INFO [kyco.controller] (MainThread) Stopping thread: MsgOutEvent Handler
  2017-02-16 02:22:15,630 - INFO [kyco.controller] (MainThread) Stopping thread: AppEvent Handler
  2017-02-16 02:22:15,631 - INFO [napps.tutorial.loopnapp.settings] (MainThread) NApp Loop Unloaded!

As you can see, the uptime was reported several times, at 02:21:41, 02:21:56 and
02:22:11 with an interval of 15 seconds, as expected.

That's it! With only one line added in the `setup` method, your code will be
running periodically. If you want to change the interval later, modify only the
`settings.py` file and the new value will be used next time the NApp is loaded.

.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/
