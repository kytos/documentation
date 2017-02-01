:tocdepth: 2
:orphan:

.. _tutorial-napps-create-your-own:

###########################
How to create your own NApp
###########################

********
Overview
********

This tutorial covers the basics on how to create your own Netwok Application
(NApp) for *Kytos Controller* (|kyco|_).

.. TODO:: Set the time

The average time to go throught it is: XX min

What you will learn
====================
* How to Create your NApp
* How your NApp comunicate with the Controller
* How to install, test and debug your NApp
* How to publish your NApp

What you will need
===================
* Your |dev_env|_ already setup
* Basic knowledge about |KycoEvents|_

************
Introduction
************

.. TODO:: Briefly describe what is a NApp

.. TODO:: Talk about its relationship with the Controller

.. TODO:: Recommend it to be as 'atomic' as it can be (solve one specific problem)

Naming your NApp
================
Since your NApp will work as a Python Module, its name must follow the same
naming rules from python modules, defined by
`PEP8 <https://www.python.org/dev/peps/pep-0008/#package-and-module-names>`_,
which states that:

  Modules should have short, all-lowercase names. Underscores can be used in
  the module name if it improves readability. Python packages should also have
  short, all-lowercase names, although the use of underscores is discouraged.

Understanding the NApp structure
================================
- *napps/<author>/<napp_name>*
    - README.rst
    - __init__.py
    - kytos.json
    - main.py
    - settings.py

.. TODO:: Describe the folder structure (napps/<author>/<napp_name>)

.. TODO:: Brief description of the required files (the role of each one, not
    its content)

*************************
Creating your first NApp
*************************

Now that we understand the basic structure of a |kyco|_ NApp, lets start
building our own.

README.rst
==========
Required Sections: **overview** and **requirements**

Suggested Section: **installing**

.. TODO:: Describe the role and importance of each section

kytos.json
==========

.. TODO:: Reinstate the description of this file and its importance

The *kytos.json* file is composed by some mandatory fields:

- name
- long_description
- description
- version
- author
- ofversion
- dependencies
- license
- git
- branch
- tags

.. TODO:: Describe what should go in each field and its 'type'

.. TODO:: Talk about how this informations are used by the *napps-server*

settings.py
===========

.. TODO:: Explain that this is the place to set 'global' variables/constants

.. TODO:: Here comes the *log* too (at least for now)

.. TODO:: Mention that this is the file in which the users are going to look
    for customizeable parameters.

main.py
=======

.. TODO:: Explore the following ideas

This is the main file of your NApp....

It loads the settings...

Contains the Main class that will be called by the controller to instantiate
and represent your NApp...

.. TODO:: Should we talk about it?

Run as a thread on the controller

Main Class
----------

.... inherits from the KycoNapp class ....

.... This is the class that the controller will call to start the napp....

.... contains at least three mandatory methods .....

.... to define other methods that will handle specific events see the section
:ref:`listening_to_events`.

Setup and Shutdown
^^^^^^^^^^^^^^^^^^

.. TODO:: Review this section

The ``setup`` and ``shutdown`` methods are executed only once. Although it is
not mandatory to implement them, you must at least declare them with ``pass``,
as we did in the `Running once`_ section.

Before ``execute``, ``setup`` is called. Besides setting the interval between
``execute`` calls (optional, explained in `active_napp`_), you can also
initialize any attribute just as you would in Python constructor
(``__init__``).

.. important::
   Do not override ``__init__``. Instead, use ``setup``.

If we want to run any code just before our napp is finished, it must be
implemented in the ``shutdown`` method.


Execute
^^^^^^^

.. NOTE:: Do not implement an infinite loop here, this method is supposed to be
    runned only once. If you want it to be runned more than once, then see the
    :ref:`active_napp` section below.

.. _reactive_napp:

Reactive NApp behavior
~~~~~~~~~~~~~~~~~~~~~~

.. TODO:: Talk about creating a new method to listen to a specific KycoEvent.

.. _active_napp:

Active NApp behavior (Running periodically)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO:: Explain about the `self.execute_as_loop(settings.POOLING_TIME)`
    option during the `setup()` and that the `execute()` will be runned
    periodically.

Let's say we want to run the ``execute`` method periodically, e.g. every 10
seconds. For that, we must add one line to the ``setup`` method:

.. code-block:: python

   def setup(self):
       self.execute_as_loop(10)  # seconds

With the line above, the ``execute`` method will be called once when our napp
is loaded and again after 10 seconds. This will keep running indefinitely.


REST endpoints
--------------

.. TODO:: Explain how to register an endpoint on the controller, both for
    `POST` and `GET` methods, and explain the 'callback'.

.. TODO:: Talk about the possibility of communication between NApps by REST,
    instead of by KycoEvents?

******************************
Understanding the Kytos Events
******************************

Events Naming Convention
========================

.. TODO:: How should events be named

.. _listening_to_events:

Listening to events
===================

.. TODO:: Talk about our `listen_to` decorator, both when listening to one
    event and more than one event.

Creating and Triggering events
===============================

.. TODO:: How to create a new KycoEvent.

.. TODO:: How to dispatch the created event.

*****************
Napp Installation
*****************

Now lets install our newly created NApp. There are two ways of installing a
NApp.

Development mode
================
Symbolic link from source to the *.installed* directory. .....

Production mode
===============
Source on the *.installed* directory. .....

*****************
Testing your NAPP
*****************

Enabling and Loading your NApp
==============================
.. TODO:: How to enable and start the napp on the controller

.. TODO:: How to manually enable the NApp (symlink)

.. TODO:: How to enable it using the controller `enable_napp()` method.

.. TODO:: How to disable the napp?

.. TODO:: How to **load** the napp on a running Kyco instance?

*******************
Debugging your NApp
*******************
Instead of writing to a file, you can use the standard Python logging module to
see messages in the output of ``controller.start()``. Check below the complete
napp code using log messages.

.. code-block:: python
   :linenos:
   :emphasize-lines: 1, 4, 10, 14

    import logging
    from kyco.core.napps import KycoNApp

    log = logging.getLogger(__name__)

    class Main(KycoNapp):

        def setup(self):
            self.execute_as_loop(10)  # seconds
            log.info('Setup finished.')

        def execute(self):
            nr_switches = len(self.controller.switches)
            log.info('Hello, world of %s switches!', nr_switches)

        def shutdown(self):
            pass

By just adding lines 1 and 4, we can use ``log.info`` (and also ``log.error``,
``log.debug``, etc) to print messages in Kyco's log. The output will be similar
to (some lines were removed for clarity)::

 2016-12-19 15:46:02,322 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller2016-12-19 15:46:02,322 - INFO [kyco.controller] (MainThread) Starting Kyco - Kytos Controller
 2016-12-19 15:46:02,329 - INFO [my_project/my_napp] (Thread-3) Setup finished.
 2016-12-19 15:46:02,330 - INFO [my_project/my_napp] (Thread-3) Hello, world of 0 switches!
 2016-12-19 15:46:02,562 - INFO [kyco.controller] (RawEvent Handler) Handling KycoEvent:kytos/core.connection.new ...
 2016-12-19 15:46:02,567 - INFO [kyco.controller] (RawEvent Handler) Handling KycoEvent:kytos/core.connection.new ...
 2016-12-19 15:46:12,337 - INFO [my_project/my_napp] (Thread-3) Hello, world of 2 switches!
 2016-12-19 15:46:22,338 - INFO [my_project/my_napp] (Thread-3) Hello, world of 2 switches!

In the output above, our log outputs are identified by *my_project/my_napp*. The
``execute`` method is run right after ``setup`` is finished and prints 0
switches. After a few milliseconds Kyco has started, the switches are added and
we have 2 switches, as expected. After 10 seconds (the interval we defined), the
same message is printed again.

.. tip::
  To see only the output of *my_napp*, run the script of `Running Kyco` with
  a pipe: ``./start_controller.py 2>&1 | grep my_project/my_napp``.

********************
Publishing your NApp
********************

.. TODO:: Explain how to publish a NApp on http://napps.kytos.io

.. include:: ../back_to_list.rst

.. |pyof| replace:: *python3-openflow*
.. _pyof: http://docs.kytos.io/pyof

.. |kyco| replace:: *Kyco*
.. _kyco: http://docs.kytos.io/kyco

.. |dev_env| replace:: *Development Environment*
.. _dev_env: /general/development_environment_setup

.. TODO:: Where does the Kyco Events documentation will be hosted?
    Should we link to the main kyco documentation? Or we will have a Tutorial
    explaining the KycoEvents?

.. |kycoevents| replace:: *KycoEvents*
.. _kycoevents: http://docs.kytos.io/kyco/
