:tocdepth: 2
:orphan:

.. _tutorial-create-ping-pong-napps:

###################################
How to create your own NApp: Part 3
###################################

********
Overview
********

In this tutorial, you will learn how to create NApps that use events
(|KytosEvents|_). You will build a NApp that generates periodic events (*Ping*)
and another one that listens to a specific event and executes an action (*Pong*)
whenever the listened event occurs.

The average time to go through this is: ``15 min``.

What you will need
===================

* How to create a basic NApp: Part 1 - Refer to |Tutorial_01|_;
* How to create a basic NApp: Part 2 - Refer to |Tutorial_02|_.

What you will learn
====================

* How KytosEvents works;
* Create a Ping NApp (generate events);
* Create a Pong NApp (listen to events);
* Running your Ping and Pong NApps.


************
Introduction
************

Now that you have learned `how to build a simple NApp
</napps/create_your_napp/>`_ and `how to implement a loop behavior on your NApp
</napps/create_looping_napp/>`_, you will understand how *Kytos* deals with
Events (|KytosEvents|_) by creating two NApps that use those events,
sending and receiving them to/from the Controller (*Kytos*).

The communication between the NApps and the Controller is done through what we
call Events (|KytosEvents|_). Events have specific naming rules, and we use
a |pydeco|_ (``listen_to``) in order to define a method as a listener of a
specific event.

The basic naming rule for events will help you define which event you want to
listen to and also help others to listen to events that your NApp generates. Here is
an example of an event name: ``kytos/of_core.messages.in.ofpt_stats_reply``. It
is composed by two mandatory parts, ``username`` (*kytos*) and ``napp_name``
(*of_core*), and another part defined by the NApp developer, the ``event_description``
(*messages.in.ofpt_stats_reply*). The first two parts help us identify the
NApp that generated the event, while the last helps identifying the event
itself - a single NApp can generate many different events.

Back to the tutorial, the first NApp will be called **ping**, and it will send
ping events periodically. While the second NApp will be called **pong**, and it
will listen to the ping events and register a pong message in the Kytos logger.

*****************
The **Ping** NApp
*****************

Bootstrapping your NApp
=======================
First, you will create the basic structure of the NApp by using the ``kytos``
command from the ``kytos-utils`` project. So, on the command line, write the
following commands:

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


The first question is related to your username, let's answer with
**tutorial** for now, since we are on our third tutorial:

.. code:: console

  Please, insert your NApps Server username: tutorial


Then, you will insert the NApp name (**ping**):

.. code:: console

  Please, insert your NApp name: ping

At last, but not least, you will be asked for a description for the NApp. This
is an optional argument and you can just hit Enter to pass it if you do not want
to insert a description right now (later, you can edit the *kytos.json* file).

.. code-block:: console

  Please, insert a brief description for your NApp [optional]: This NApp sends a Ping event every N seconds (see settings.py for N).

.. code-block:: console

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/ping and begin to code your NApp.
  Have fun!

Now your NApp has been created. You can enter its directory by typing:

.. code:: console

  $ cd tutorial/ping

The next step is editing the ``settings.py`` and ``main.py`` files.

settings.py
===========
In order to define the ping frequency, add a constant ``PING_INTERVAL`` to the
settings file. Start with a 5 seconds interval for now. Later on you can change
it and see the difference.

.. code-block:: python

    # interval to send a new ping event (in seconds)
    PING_INTERVAL = 5

main.py
=======

On the *main.py* file you will start by doing some initial setup.

Setup
-----

In the `setup()` method you will define that this NApp will run the `execute`
method every ``PING_INTERVAL`` seconds, previously defined in the
``settings.py`` file.

.. code-block:: python

   def setup(self):
       self.execute_as_loop(settings.PING_INTERVAL)

Sending the ping
----------------
As you want a periodical routine to be executed, you must define your code
inside the the `execute()` method.

The routine will consist on creating a new event, an instance of ``KytosEvent``
class and, later on, putting this event into the controller buffer.

As said in the introduction, the event name must start with a composition
of the username name and the NApp name. In this case, it is
``tutorial/ping``. Then, you must add a complement to it in such a way that
the full name of the event will be ``tutorial/ping.periodic_ping``.

.. NOTE:: You can choose another name at your will, but just remember that this
    name will be used in the **Pong NApp**, later on this tutorial).

Just to better identify each ping event, we will also add a *message* on the
event with the *timestamp* of the event creation. This *message* must be added
inside the ``content`` argument (``dict``) of the event.

So, the code to create your ping event will be:

.. code-block:: python

  ping_event = KytosEvent(name='tutorial/ping.periodic_ping',
                         content={'message': datetime.now()})

.. NOTE:: As we are using ``datetime.now()``, we must import the datetime module
    in our ``main.py`` file. See the final version of this file in the end of
    this tutorial.

After creating the event, now add it into the controller buffer. The event will
be exchanged between NApps, so we will put it in the ``app`` buffer:

.. NOTE:: For now every NApp, when loaded by the controller, receives a
    reference to the controller itself, so we can access its buffers. On the
    future this access will be handled in another way.

.. code:: python

    self.controller.buffers.app.put(ping_event)

Summing up, the ``execute()`` method will be:

.. code-block:: python

    def execute(self):
        ping_event = KytosEvent(name='tutorial/ping.periodic_ping',
                               content={'message': datetime.now()})
        self.controller.buffers.app.put(ping_event)
        log.info('%s Ping sent.', ping_event.content['message'])

In the last line, log a message to inform that a ping has been sent and its
timestamp.

And your ``main.py`` file will look like:

.. code-block:: python

    """App responsible for send ping events."""
    from datetime import datetime

    from kytos.core import KytosEvent, KytosNApp, log

    from napps.tutorial.ping import settings


    class Main(KytosNApp):

            def setup(self):
                self.execute_as_loop(settings.PING_INTERVAL)

            def execute(self):
                ping_event = KytosEvent(name='tutorial/ping.periodic_ping',
                                        content={'message': datetime.now()})
                self.controller.buffers.app.put(ping_event)
                log.info('%s Ping sent.', ping_event.content['message'])

            def shutdown(self):
               pass


*****************
The **Pong** NApp
*****************

Bootstrapping your NApp
=======================

Similarly to what you did on the Ping NApp, use the ``kytos`` command to create
your **Pong** NApp's structure:

.. code-block:: console

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

Use the same username, **tutorial**:

.. code:: console

  Please, insert your NApps Server username: tutorial

And **pong** and NApp name.

.. code:: console

  Please, insert your NApp name: pong

And the NApp description

.. code-block:: console

  Please, insert a brief description for your NApp [optional]: This NApp answers to a Ping event.

.. code-block:: console

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/pong and begin to code your NApp.
  Have fun!

Now your NApp has been created, and you can enter its directory by typing:

.. code:: console

  $ cd tutorial/pong


Since this napp will not define any special variable, you just have to edit the
``main.py`` file.

main.py
=======

In ``main.py``, you will define a new method ``pong``, that will be called
whenever the controller consumes a ping event from its buffers. The ``pong``
method will receive the event as an argument and then log its timestamp and the
current timestamp also.

First, define your new ``pong`` method inside the ``Main`` class:

.. code:: python

    def pong(self, event):
        message = 'Hi, here is the Pong NApp answering a ping.'
        message += 'The current time is {}, and the ping was dispatched '
        message += 'at {}.'
        log.info(message.format(datetime.now(), event.content['message']))

Now, you must use the ``listen_to`` decorator do define the method that will
respond to ``tutorial/ping.periodic_ping`` events.

.. code:: python

    @listen_to('tutorial/ping.periodic_ping')
    def pong(self, event):
        message = 'Hi, here is the Pong NApp answering a ping.'
        message += 'The current time is {}, and the ping was dispatched '
        message += 'at {}.'
        log.info(message.format(datetime.now(), event.content['message']))

This decorator ensures that the controller is aware that the method must be
called whenever the given event happens.

So, the ``main.py`` file of the ``pong`` napp will be:

.. code-block:: python

    """App for answering ping events."""
    from datetime import datetime

    from kytos.core import KytosNApp, log
    from kytos.core.helpers import listen_to

    from napps.tutorial.pong import settings


    class Main(KytosNApp):

        def setup(self):
            pass

        def execute(self):
           pass

        @listen_to('tutorial/ping.periodic_ping')
        def pong(self, event):
            message = 'Hi, here is the Pong NApp answering a ping.'
            message += 'The current time is {}, and the ping was dispatched '
            message += 'at {}.'
            self.log.info(message.format(datetime.now(),
                                         event.content['message']))

        def shutdown(self):
            pass

*********************************
Running your Ping and Pong NApps
*********************************

In order to install and enable your NApp, you have to first run the Kytos controller. Kytos will then be
able to recognize and manage installed/enabled NApps. In another terminal window, activate the virtual environment and run:

.. code-block:: console

  $ kytosd -f
  2017-07-18 10:09:51,644 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-07-18 10:09:51,646 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-07-18 10:09:51,648 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-07-18 10:09:51,649 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6633
  2017-07-18 10:09:51,651 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-07-18 10:09:51,652 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-07-18 10:09:51,653 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-07-18 10:09:51,654 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-07-18 10:09:51,654 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-07-18 10:09:51,722 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-07-18 10:09:51,730 - INFO [kytos.core.controller] (MainThread) Loading NApp tutorial/loopnapp
  2017-07-18 10:09:51,938 - INFO [tutorial/loopnapp] (MainThread) Loop NApp Loaded!
  2017-07-18 10:09:51,957 - INFO [root] (loopnapp) Running NApp: <Main(loopnapp, started 139640979838720)>
  2017-07-18 10:09:51,960 - INFO [tutorial/loopnapp] (loopnapp) Controller Uptime: 0:00:00.018828
  
  (...)
  
  kytos $>

If you are following the tutorials, you can see that ``tutorial/loopnapp`` is enabled. You can disable it by running:

.. code-block:: console

  $ kytos napps disable tutorial/loopnapp
  INFO  NApp tutorial/loopnapp:
  INFO    Disabling...
  INFO    Disabled.

Only the new NApps will run this time.
Yes, we are not running any other NApp for now, we are disabling everything,
including OpenFlow NApps.


.. NOTE::
    For this demo, you don't want any other NApp running except those
    created during this tutorial. So if your setup has multiple NApps enabled,
    please, disable them with the command:
    ``kytos napps disable <NApp ID>``


In order to run your NApps, first you have to install them. Once more use the
``kytos`` command line from the ``kytos-utils`` package.

To install and enable your NApps, run the commands below:

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps install tutorial/ping tutorial/pong

.. NOTE:: This will try to get the NApps from the current directory and then
   install and enable them into your system. The NApps will be executed as soon
   as they are enabled.

Now, your Ping and Pong NApps are installed, enabled, and being executed. You can see this
by running the command:

.. code:: bash

  $ kytos napps list
  Status |          NApp ID          |                     Description                                                       
  =======+===========================+======================================================
   [i-]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for ...
   [i-]  | kytos/of_flow_manager     | Manage switches' flows through a REST API.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all switches.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swit...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using t...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | Keeps track of links between hosts and switches. Re...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interface setti...
   [i-]  | tutorial/helloworld       | Hello, world!
   [i-]  | tutorial/loopnapp         | Loop NApp
   [ie]  | tutorial/ping             | This NApp sends a Ping event every N seconds (see s...
   [ie]  | tutorial/pong             | This NApp answers to a Ping event.
 
  Status: (i)nstalled, (e)nabled

Testing your NApp
=================

Let's see our controller logs in the console:

.. code-block:: console

  2017-07-18 10:23:05,578 - INFO [root] (ping) Running NApp: <Main(ping, started 139640979838720)>
  2017-07-18 10:23:05,604 - INFO [root] (pong) Running NApp: <Main(pong, started 139640954660608)>
  2017-07-18 10:23:05,608 - INFO [tutorial/ping] (ping) 2017-07-18 10:23:05.580778 Ping sent.
  2017-07-18 10:23:10,618 - INFO [tutorial/ping] (ping) 2017-07-18 10:23:10.610590 Ping sent.
  2017-07-18 10:23:10,772 - INFO [tutorial/pong] (Thread-31) Hi, here is the Pong NApp answering a ping.The current time is 2017-07-18 10:23:10.772534, and the ping was dispatched at 2017-07-18 10:23:10.61.
  2017-07-18 10:23:15,622 - INFO [tutorial/ping] (ping) 2017-07-18 10:23:15.618841 Ping sent.
  2017-07-18 10:23:15,624 - INFO [tutorial/pong] (Thread-32) Hi, here is the Pong NApp answering a ping.The current time is 2017-07-18 10:23:15.624875, and the ping was dispatched at 2017-07-18 10:23:15.61.
  2017-07-18 10:23:20,627 - INFO [tutorial/ping] (ping) 2017-07-18 10:23:20.624353 Ping sent.
  2017-07-18 10:23:20,627 - INFO [tutorial/pong] (Thread-33) Hi, here is the Pong NApp answering a ping.The current time is 2017-07-18 10:23:20.627384, and the ping was dispatched at 2017-07-18 10:23:20.62.
  2017-07-18 10:23:25,633 - INFO [tutorial/ping] (ping) 2017-07-18 10:23:25.628697 Ping sent.
  2017-07-18 10:23:25,635 - INFO [tutorial/pong] (Thread-35) Hi, here is the Pong NApp answering a ping.The current time is 2017-07-18 10:23:25.634935, and the ping was dispatched at 2017-07-18 10:23:25.62.
  2017-07-18 10:23:30,639 - INFO [tutorial/ping] (ping) 2017-07-18 10:23:30.634607 Ping sent.
  2017-07-18 10:23:30,638 - INFO [tutorial/pong] (Thread-36) Hi, here is the Pong NApp answering a ping.The current time is 2017-07-18 10:23:30.637920, and the ping was dispatched at 2017-07-18 10:23:30.63.


Note the ping NApp sending its timestamps each five seconds, and the pong NApp
logging them when received.

.. NOTE:: To stop your controller, just run the *quit* command.

.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |Tutorial_02| replace:: *Tutorial 02*
.. _Tutorial_02: https://tutorials.kytos.io/napps/create_looping_napp/

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |kytosevents| replace:: *KytosEvents*
.. _kytosevents: https://docs.kytos.io/kytos/developer/listened_events/

.. |pydeco| replace:: *decorator*
.. _pydeco: https://wiki.python.org/moin/PythonDecorators#What_is_a_Decorator
