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
(|KycoEvents|_). You will buid one NApp that generate periodic events (*Ping*)
and another one that listens to a specific event and execute an action (*Pong*)
whenever the listened event occurs.

The average time to go through this is: ``15 min``.

What you will need
===================

* How to create a basic NApp: Part 1 - Refer to |Tutorial_01|_;
* How to create a basic NApp: Part 2 - Refer to |Tutorial_02|_.

What you will learn
====================

* How KycoEvents works;
* Create a Ping NApp (generate events);
* Create a Pong NApp (listens to events);
* Running your Ping and Pong Napps.


************
Introduction
************

Now that you have learned `how to build a simple NApp
</napps/create_your_napp/>`_ and `how to implement a loop behavior on your NApp
</napps/create_looping_napp/>`_, you will understand how *Kyco* deals with
Events (|KycoEvents|_) by creating two NApps that use these events for both
sending and receiving them to/from the Controller (*Kyco*).

The communication between the NApps and the Controller is done through what we
call Events (|KycoEvents|_). These events have specific naming rules, and we use
a |pydeco|_ (``listen_to``) in order to define a method as a listener of a
specific event.

The basic naming rule for events will help you define which event you want to
listen to and also help others to listen to events that your NApp generates. Here is
an example of an event name: ``kytos/of_core.messages.in.ofpt_stats_reply``. It
is composed by two mandatory parts, ``username`` (*kytos*) and ``napp_name``
(*of_core*), and another part defined by the NApp author, the ``event_description``
(*messages.in.ofpt_stats_reply*). The first two parts help us identify the
NApp that generated the event, while the last helps identifying the event
itself - a NApp can generate many different events.

Back to the tutorial, the first NApp will be called **ping**, and it will send
ping events periodically. While the second NApp will be called **pong**, and it
will listen to the ping events and register a pong message in the Kyco logger.

*****************
The **Ping** NApp
*****************

Bootstrapping your NApp
=======================
First, you will create the basic structure of the NApp by using the ``kytos``
command from the ``kytos-utils`` project. So, on the command line, write the
following commands:

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


The first question is related to your username, let's answer with
**tutorial** for now, since we are on our third tutorial:

.. code:: bash

  Please, insert your NApps Server username: tutorial


Then, you will insert the NApp name (**ping**):

.. code:: bash

  Please, insert your NApp name: ping

At last, but not least, you will be asked for a description for the NApp. This
is an optional argument and you can just hit Enter to pass it if you do not want
to insert a description right now (later, you can edit the *kytos.json* file).

.. code-block:: bash

  Please, insert a brief description for your NApp [optional]: This NApp sends a Ping event every N seconds (see settings.py for N).

.. code-block:: bash

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/ping and begin to code your NApp.
  Have fun!

Now that your NApp has been created, and you can enter in its directory by typing:

.. code:: bash

  $ cd tutorial/ping

The next step is editing the ``settings.py`` and ``main.py`` files.

settings.py
===========
In order to define the ping frequency, add a constant ``PING_INTERVAL`` on the
settings file. Start with a 5 seconds interval for now. Later on you can change
it and see the difference.

.. code-block:: python

    import logging

    # Log Registry Type
    log = logging.getLogger(__name__)

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

The routine will consist on creating a new event, an instance of ``KycoEvent``
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

  ping_event = KycoEvent(name='tutorial/ping.periodic_ping',
                         content={'message': datetime.now()})

.. NOTE:: As we are using ``datetime.now()``, we must import the datetime module
    in our ``main.py`` file. See the final version of this file in the end of
    this tutorial.

After creating the event, now add it into the controller buffer.

.. NOTE:: For now, every NApp, when loaded by the controller, receives a
    reference to the controller itself, so we can access its buffers. On the
    future this access will be handled in another way.

.. code:: python

    self.controller.buffers.app.put(ping_event)

Summing up, the ``execute()`` method will be:

.. code-block:: python

    def execute(self):
        ping_event = KycoEvent(name='tutorial/ping.periodic_ping',
                               content={'message': datetime.now()})
        self.controller.buffers.app.put(ping_event)
        log.info('%s Ping sent.', ping_event.content['message'])

In the last line, log a message to inform that a ping has been sent and its
timestamp.

And your ``main.py`` file will look like:

.. code-block:: python

    """App responsible for send ping events."""
    from datetime import datetime

    from kyco.core.events import KycoEvent
    from kyco.core.napps import KycoNApp

    from napps.tutorial.ping import settings

    log = settings.log


    class Main(KycoNApp):

            def setup(self):
                self.execute_as_loop(settings.PING_INTERVAL)

            def execute(self):
                ping_event = KycoEvent(name='tutorial/ping.periodic_ping',
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

.. code-block:: bash

  $ cd ~/tutorials
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

Use the same author name, **tutorial**:

.. code:: bash

  Please, insert your author name (username on the Napps Server): tutorial

And **pong** and NApp name.

.. code:: bash

  Please, insert your NApp name: pong

And the NApp description

.. code-block:: bash

  Please, insert a brief description for your NApp [optional]: This NApp answers to a Ping event.

.. code-block:: bash

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/pong and begin to code your NApp.
  Have fun!

Now your NApp has been created, and you can enter on its directory by typing:

.. code:: bash

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

    """App responsible for answering to ping events."""
    from datetime import datetime

    from kyco.core.events import KycoEvent
    from kyco.core.napps import KycoNApp
    from kyco.utils import listen_to

    from napps.tutorial.pong import settings

    log = settings.log


    class Main(KycoNApp):

        def setup(self):
            pass

        def execute(self):
           pass

        @listen_to('tutorial/ping.periodic_ping')
        def pong(self, event):
            message = 'Hi, here is the Pong NApp answering a ping.'
            message += 'The current time is {}, and the ping was dispatched '
            message += 'at {}.'
            log.info(message.format(datetime.now(),
                                    event.content['message']))

        def shutdown(self):
            pass

*********************************
Running your Ping and Pong NApps
*********************************

In order to run your NApps, first you have to install them. Once more use the
``kytos`` command line from the ``kytos-utils`` package.

To install and enable your NApps, run the commands below:

.. code-block:: bash

  $ cd ~/tutorials
  $ kytos napps install tutorial/ping
  $ kytos napps install tutorial/pong

.. NOTE:: This will try to get the NApps from the current directory and then
   install and enable them into your system.

Now, your Ping and Pong NApps are ready to be executed.

You can also see if your NApp is installed and enabled, by running the command:

.. code:: bash

  $ kytos napps list

.. NOTE::
    For this demo, you don't want any other NApp running except those
    created during this tutorial. So if your setup has multiple NApps enabled,
    please, disable them with the command:
    ``kytos napps disable <NApp ID>``

Testing your NApp
=================

Let's start our controller:

.. code-block:: bash

   $ kyco
   2017-02-15 19:44:06,583 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller
   2017-02-15 19:44:06,586 - INFO [kyco.core.tcp_server] (TCP server) Kyco listening at 0.0.0.0:6633
   2017-02-15 19:44:06,586 - INFO [kyco.controller] (RawEvent Handler) Raw Event Handler started
   2017-02-15 19:44:06,587 - INFO [kyco.controller] (MsgInEvent Handler) Message In Event Handler started
   2017-02-15 19:44:06,598 - INFO [kyco.controller] (MsgOutEvent Handler) Message Out Event Handler started
   2017-02-15 19:44:06,598 - INFO [kyco.controller] (AppEvent Handler) App Event Handler started
   2017-02-15 19:44:06,599 - INFO [kyco.controller] (MainThread) Loading kyco apps...
   2017-02-15 19:44:06,602 - INFO [kyco.controller] (MainThread) Loading NApp kytos/of_core
   2017-02-15 19:44:06,603 - INFO [werkzeug] (Thread-2)  * Running on http://0.0.0.0:8181/ (Press CTRL+C to quit)
   2017-02-15 19:44:06,634 - INFO [kyco.core.napps] (Thread-3) Running Thread-3 App
   2017-02-15 19:44:06,635 - INFO [kyco.controller] (MainThread) Loading NApp tutorial/ping
   2017-02-15 19:44:06,638 - INFO [kyco.core.napps] (Thread-4) Running Thread-4 App
   2017-02-15 19:44:06,638 - INFO [kyco.controller] (MainThread) Loading NApp tutorial/pong
   2017-02-15 19:44:06,639 - INFO [napps.tutorial.ping.settings] (Thread-4) 2017-02-15 19:44:06.639154 Ping sent.
   2017-02-15 19:44:06,642 - INFO [kyco.core.napps] (Thread-5) Running Thread-5 App

You will get into the controller terminal, and you can see your NApps outputs.

.. NOTE:: To stop your controller you must press CTRL+C

.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |Tutorial_02| replace:: *Tutorial 02*
.. _Tutorial_02: https://tutorials.kytos.io/napps/create_looping_napp/

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: https://docs.kytos.io/kyco/developer/listened_events/

.. |pydeco| replace:: *decorator*
.. _pydeco: https://wiki.python.org/moin/PythonDecorators#What_is_a_Decorator
