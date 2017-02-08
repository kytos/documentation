:tocdepth: 2
:orphan:

.. _tutorial-create-ping-pong-napps:

#############################
How to create ping-pong napps
#############################

********
Overview
********

This tutorial is focused in create two simple napps to send a event to
network and receive a event from network using your own Netwok Application
(NApp) for *Kytos Controller* (|kyco|_).

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will need
===================

* How to create a basic NApp: Part 1 - Refer to |Tutorial_01|_
* How to create a basic NApp: Part 2 - Refer to |Tutorial_02|_

What you will learn
====================

* Create a Ping NApp
* Create a Pong NApp
* Running your Ping and Pong Napps


************
Introduction
************

Now that you have learned how to build a simple NApp, in this tutorial we will
help you to develop Napps responsible to send and receive events.

The first NApp will be called **of_ping**, which is responsible to send a
``EchoRequest`` message to all connected switches each 5 seconds. The second Napp
will be called **of_pong**, which will listen a ``KycoEvent`` called
`kytos/of.core.messages.in.ofpt_echo_reply` sent by all switch. Each message
sent and listened by your own napps will shown into the Kyco loggers.

*********************
Create a Ping NApp
*********************

Start the NApp structure
========================

First step is create a new directory named **of_ping** and to use the kytos
command to create the NApp structure.

.. code-block:: bash

  $ mkdir -p ~/tutorial03/of_ping
  $ cd ~/tutorial03/of_ping
  $ kytos napp create

Then, after created the **of_ping** Napp you will edit the files `settings.py`
and `main.py` as described below.

settings.py
-----------

In order to adjust the ping frequency the file `settings.py` must be edited to
have a constant *PING_INTERVAL* with the value 5 and the *log* constant. After
modified the file will be like that:

.. code-block:: python

    import logging

    # Log Registry Type
    log = logging.getLogger(__name__)

    # interval to send a new ping event
    PING_INTERVAL = 5

main.py
-------

Setup
^^^^^

In `main.py` file, we have to adjust the `setup()` method. This adjust tells
the controller that this NApp will run repeatedly using the constant
*PING_INTERVAL* defined into `settings.py`.

.. code-block:: python

   def setup(self):
       self.execute_as_loop(settings.PING_INTERVAL)

Execute
^^^^^^^

In `execute()` method we code what will be execute every five seconds. In
this case, we ensure the Ping NApp will go through each switch and send a
EchoRequest message.

To create a event we will to use a ``KycoEvent`` class to represent a event
into Kyco. To send a message to switch we need put a ``KycoEvent`` instance
within the controller buffers with output messages, using the method
`self.controller.buffers.msg_out.put(event_out)`. The Kyco will get that
message and send the event to network. To send a message to each switch we
must to use the method `self.controller.switch.values()` to go through each
switch registered and create a new ``KycoEvent`` and put this within output
buffers.
Finally, the last line of the method `execute()` will create a new
log message to show that a new message was sent by the Ping Napp to the switch.

.. code-block:: python

   def execute(self):
      for switch in self.controller.switches.values():
          event_out = KycoEvent(name=('kytos/of_core.messages.out.ofpt_echo_request'),
                                content={'destination': switch.connection,
                                         'message': EchoRequest()})
          self.controller.buffers.msg_out.put(event_out)
          log.info('Seding ping message to switch {}'.format(switch.id))

Ping NApp
~~~~~~~~~

Following, the `main.py` implemented with the methods shown above.

.. code-block:: python

    """App responsible for send ping events."""

    from kyco.core.events import KycoEvent
    from kyco.core.napps import KycoCoreNApp
    from pyof.v0x01.symmetric.echo_request import EchoRequest
    from kyco.utils import listen_to

    from napps.kytos.of_ping import settings
    log = settings.log


    class Main(KycoCoreNApp):

            def setup(self):
                self.execute_as_loop(settings.INTERVAL)

            def execute(self):
                for switch in self.controller.switches.values():
                    event_out = KycoEvent(name=('kytos/of.core.messages.out.echo_request'),
                                          content={'destination': switch.connection,
                                                   'message': EchoRequest()})
                    self.controller.buffers.msg_out.put(event_out)
                    log.info('Seding ping message to switch {}'.format(switch.id))

            def shutdown(self):
               pass

*********************
Create a Pong NApp
*********************

Start the NApp structure
========================

First step is create a new directory named **of_pong** and to use the kytos
command to create the NApp structure.

.. code-block:: bash

  $ mkdir -p ~/tutorial03/of_pong
  $ cd ~/tutorial03/of_pong
  $ kytos napp create

Then, after created the **of_pong** Napp you will edit the file `main.py` as
described below.

main.py
-------

In `main.py` file we must code a new method called `listen_pong_event(self, event)`.
This method must have a decorator named `list_to` listening the ``KycoEvent``
named *kytos/of.core.messages.in.ofpt_echo_reply*.That method will receive a
``KycoEvent`` from each switch registered that receive the message sent by
Ping Napp. After received that message this method will write a new message
``Pong event was called.`` within Kyco loggers.

Pong Class
^^^^^^^^^^
.. code-block:: python

    """App responsible for receive ping events."""

    from kyco.core.events import KycoEvent
    from kyco.core.napps import KycoCoreNApp
    from pyof.v0x01.symmetric.echo_reply import EchoReply
    from kyco.utils import listen_to

    from napps.kytos.of_ping import settings
    log = settings.log


    class Main(KycoCoreNApp):

        def setup(self):
            self.execute_as_loop(settings.INTERVAL)

        def execute(self):
           pass

        @listen_to('kytos/of.core.messages.in.ofpt_echo_reply')
        def listen_pong_event(self, event):
           log.info('Pong event was called.')

        def shutdown(self):
            pass

*********************************
Running your Ping and Pong NApps
*********************************

In order to run your NApps, first your have to install it. Again, we are going
to use the ``kytos`` command line from the ``kytos-utils`` package.
To install and enable your NApps you must run the command below.

.. code-block:: bash

  $ cd ~/
  $ sudo kytos napps install tutorial03/of_ping
  $ sudo kytos napps install tutorial03/of_pong

.. NOTE:: This will try to get your napps from current directory,
   then install and enable it into your system.

Now, your Ping and Pong Napps are ready to be executed.

You can also see if your Napp is installed and enabled, by running the command:

.. code-block:: bash

  $ kytos napps list

For this demo, we don't wanna any other napp running except this created during
this tutorial. So if your setup has multiple napps, please disable them, with
the command:

.. code-block:: bash

  $ kytos napps disable <author_name>/<napp_name>


Yes, we are not running any napp for now, we are disabling everything including
OpenFlow Napps.

Testing your NApp
=================

Let's start our controller:

.. code-block:: bash

  $ kytos-kyco start

You will get into the controller terminal, and you can see your NApp output.

.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |Tutorial_02| replace:: *Tutorial 02*
.. _Tutorial_02: https://tutorials.kytos.io/napps/create_looping_napp/

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: http://docs.kytos.io/kyco/
