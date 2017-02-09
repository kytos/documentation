:tocdepth: 2
:orphan:

.. _tutorial-create-ping-pong-napps:

############################
Creating ping and pong NApps
############################

********
Overview
********

In this tutorial you will lean how to create napps that uses events
(``KycoEvent``). You will buid one NApp that generate periodic events (*Ping*)
and another one that listen to a specific event and execute an action (*Pong*)
whenever the listened event occur.

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will need
===================

* How to create a basic NApp: Part 1 - Refer to |Tutorial_01|_
* How to create a basic NApp: Part 2 - Refer to |Tutorial_02|_

What you will learn
====================

* How KycoEvents works
* Create a Ping NApp
* Create a Pong NApp
* Running your Ping and Pong Napps


************
Introduction
************

Now that you have learned `how to build a simple NApp
</napps/create_your_napp/>`_ and `how to implement a loop behavior on your NApp
</napps/create_looping_napp/>`_, you will understand how *Kyco* deals with
Events (*KycoEvent*) by creating two NApps that use these events both sending
and receiving them to/from the Controller (*Kyco*).

The communication between the NApps and the Controller is done throught what we
call Events (*KycoEvents*). These events have specific naming rules, and we use
a |pydeco|_ (``listen_to``) in order to define a method as a listener of a
specific event.

The basic naming rule for events will help you define which event you want to
listen to and also help others to listen to events your NApp generate. Here is
an example of an event name: ``kytos/of_core.messages.in.ofpt_stats_reply``. It
is composed by two mandatory parts, ``napp_author`` (*kytos*) and ``napp_name``
(*of_core*), and another part defined by the NApp author, ``event_description``
(*messages.in.ofpt_stats_reply*). The first two parts helps us identify the
NApp that generated the event, while the last helps identifying the event
itself - a NApp can generate multiple different events.

Back to the tutorial, the first NApp will be called **ping**, and it will send
ping events periodically. While the second NApp will be called **pong**, and it
will listen to the ping events and register a pong message on the Kyco logger.

*****************
The **Ping** NApp
*****************

Bootstrapping your NApp
=======================
Firstly you will create the baisc structure of the NApp by using the ``kytos``
command from the ``kytos-utils`` package. So, on the command line write the
following commands:

.. code-block:: bash

  $ cd ~/sandbox
  ~/sandbox$ kytos napps create
  --------------------------------------------------------------
  Welcome to the bootstrap process of your NApp.
  --------------------------------------------------------------
  In order to answer both the author name and the napp name,
  You must follow this naming rules:
   - it cannot be empty
   - it cannot contain spaces
   - it cannot start with underscore or numbers
   - it cannot contain the following characters: -*.!@#$%&()[]\/
  --------------------------------------------------------------

The first question is related to your author name, let's answer with
**tutorial03** for now, since we are on our third tutorial:

.. code:: bash

  Please, insert you author name (username on the Napps Server): tutorial03

Then, you will insert the NApp name (**ping**):

.. code:: bash

  Please, insert you NApp name: ping

At last, but not least, you will be asked for a description for the NApp. This
is a optional argument and you can just hit Enter to pass it if you do not want
to insert a description.

.. code-block:: bash

  Please, insert a brief description for your NApp [optional]: This NApp sends a Ping event every N seconds (see settings.py for N).

.. code-block:: bash

  Congratulations! Your NApp have been bootsrapped!
  Now you can go to the directory tutorial03/ping and begin to code your NApp.
  Have fun!

Now your NApp has been created, and you can enter on its directory by typing:

.. code:: bash

  ~/sandbox$ cd tutorial03/ping

The next step is editing the ``settings.py`` and ``main.py`` files.

settings.py
===========
In order to define the ping frequency, add a constant ``PING_INTERVAL`` on the
settings file. Start with a 5 seconds interval for now. Later on you can change
it and see the differences.

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

In the `setup()` method you will defined that this NApp will run the execute
method repeatedly by the constant ``PING_INTERVAL``, previously defined on the
``settings.py``.

.. code-block:: python

   def setup(self):
       self.execute_as_loop(settings.PING_INTERVAL)

Sending the ping
----------------
As you want a peridical routine to be executed, you must defined your code
inside the the `execute()` method.

The routine will consist in creating a new event, an instance of ``KycoEvent``
class, and, later on, putting this even into the controller buffer.

As said on the introduction, the event name must start with a composition
between the napp author name and the napp name itself. In this case it is
``tutorial03/ping``. Then you must add a complement to it in such a way that
the full name of the event will be ``tutorial03/ping.periodic_ping``.

.. NOTE:: You can choose another name at your will, but just remember that this
    name will be used on the **Pong NApp** later on this tutorial).

Just to better identify each ping event, we will also add a *message* on the
event with the *timestamp* of the event creation. This *message* must be added
inside the ``content`` argument (``dict``) of the event.

So, the code to create your ping event will be:

.. code-block:: python

  ping_event = KycoEvent(name='tutorial03/ping.periodic_ping',
                         content={'message': datetime.now())

.. NOTE:: As we are using ``datetime.now()``, we must import the datetime on
    our ``main.py`` file. See the final version of this file on the end of this
    tutorial.

After creating the event, now add it into the controller buffer.

.. NOTE:: For now, every NApp, when loaded by the controller, receives a
    reference to the controller itself, so we can access its buffers. On the
    future this access will be handled in another way.

.. code:: python

    self.controller.buffers.app.put(ping_event)

Summing up, the ``execute()`` method will be:

.. code-block:: python

    def execute(self):
        ping_event = KycoEvent(name='tutorial03/ping.periodic_ping',
                               content={'message': datetime.now())
        self.controller.buffers.app.put(ping_event)
        log.info('{} Ping sent.'.format(ping_event.content['message']))

In the last line, log a message to inform that a ping has been sent and its
timestamp.

And your ``main.py`` file will looks like:

.. code-block:: python

    """App responsible for send ping events."""
    from datetime import datetime

    from kyco.core.events import KycoEvent
    from kyco.core.napps import KycoCoreNApp

    from napps.tutorial03.ping import settings

    log = settings.log


    class Main(KycoCoreNApp):

            def setup(self):
                self.execute_as_loop(settings.INTERVAL)

            def execute(self):
                ping_event = KycoEvent(name='tutorial03/ping.periodic_ping',
                                    content={'message': datetime.now())
                self.controller.buffers.app.put(ping_event)
                log.info('{} Ping sent.'.format(ping_event.content['message']))

            def shutdown(self):
               pass

*****************
The **Pong** NApp
*****************

Bootstrapping your NApp
=======================

Similarly to what you did on the Ping NApp, use the ``kytos`` command to create
your **Pong** NApp structure:

.. code-block:: bash

  $ cd ~/sandbox
  ~/sandbox$ kytos napps create
  --------------------------------------------------------------
  Welcome to the bootstrap process of your NApp.
  --------------------------------------------------------------
  In order to answer both the author name and the napp name,
  You must follow this naming rules:
   - it cannot be empty
   - it cannot contain spaces
   - it cannot start with underscore or numbers
   - it cannot contain the following characters: -*.!@#$%&()[]\/
  --------------------------------------------------------------

Use the same author name, **tutorial03**:

.. code:: bash

  Please, insert you author name (username on the Napps Server): tutorial03

And **pong** and NApp name.

.. code:: bash

  Please, insert you NApp name: pong

And the NApp description

.. code-block:: bash

  Please, insert a brief description for your NApp [optional]: This NApp answers to a Ping event.

.. code-block:: bash

  Congratulations! Your NApp have been bootsrapped!
  Now you can go to the directory tutorial03/pong and begin to code your NApp.
  Have fun!

Now your NApp has been created, and you can enter on its directory by typing:

.. code:: bash

  ~/sandbox$ cd tutorial03/pong


Since this napp will not define any special variable, you just have to edit the
``main.py`` file.

main.py
=======

In ``main.py`` file you will define a new method ``pong``, that will be called
whenever the controller consume a ping event from its buffers. The ``pong``
method will receive the event as argument and then log its timestamp and the
current timestamp also.

First define your new ``pong`` method inside the ``Main`` class:

.. code:: python

    def pong(self, event):
        message = 'Hi, here is the Pong NApp answering a ping.
        message += 'The current time is {}, and the ping was dispateched'
        message += 'at {}.'
        log.info(message.format(datetime.now(), ping_event.content['message']))

Now, the way you define your method to answers to
``tutorial03/ping.periodic_ping`` events, you must use the ``listen_to``
decorator:

.. code:: python

    @listen_to('tutorial03/ping.periodic_ping')
    def pong(self, event):
        message = 'Hi, here is the Pong NApp answering a ping.
        message += 'The current time is {}, and the ping was dispateched'
        message += 'at {}.'
        log.info(message.format(datetime.now(), ping_event.content['message']))

This decorator ensures that the controller is aware that the method must be
called whenever the given event happens.

So, the ``main.py`` file of the ``pong`` napp will be:

.. code-block:: python

    """App responsible for answering to ping events."""
    from datetime import datetime

    from kyco.core.events import KycoEvent
    from kyco.core.napps import KycoCoreNApp
    from kyco.utils import listen_to

    from napps.kytos.of_ping import settings

    log = settings.log


    class Main(KycoCoreNApp):

        def setup(self):
            pass

        def execute(self):
           pass

        @listen_to('tutorial03/ping.periodic_ping')
        def pong(self, event):
            message = 'Hi, here is the Pong NApp answering a ping.
            message += 'The current time is {}, and the ping was dispateched'
            message += 'at {}.'
            log.info(message.format(datetime.now(),
                                    ping_event.content['message']))

        def shutdown(self):
            pass

*********************************
Running your Ping and Pong NApps
*********************************

In order to run your NApps, first your have to install them. Once more use the
``kytos`` command line from the ``kytos-utils`` packagei.

To install and enable your NApps run the commands below:

.. code-block:: bash

  $ cd ~/sandbox
  $ kytos napps install tutorial03/ping
  $ kytos napps install tutorial03/pong

.. NOTE:: This will try to get the napps from the current directory and then
   install and enable them into your system.

Now, your Ping and Pong Napps are ready to be executed.

You can also see if your Napp is installed and enabled, by running the command:

.. code:: bash

  $ kytos napps list

.. NOTE::
    For this demo, you we don't want any other napp running except those
    created during this tutorial. So if your setup has multiple napps enabled,
    please disable them, with the command:
    ``kytos napps disable <author_name>/<napp_name>``

Testing your NApp
=================

Let's start our controller:

.. code-block:: bash

  $ kytos-kyco start

You will get into the controller terminal, and you can see your NApps outputs.

.. TODO:: Add here the output of the command



.. include:: ../back_to_list.rst

.. |Tutorial_01| replace:: *Tutorial 01*
.. _Tutorial_01: http://tutorials.kytos.io/napps/create_your_napp/

.. |Tutorial_02| replace:: *Tutorial 02*
.. _Tutorial_02: https://tutorials.kytos.io/napps/create_looping_napp/

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: http://docs.kytos.io/kyco/

.. |pydeco| replace:: *decorator*
.. _pydeco: https://wiki.python.org/moin/PythonDecorators#What_is_a_Decorator
